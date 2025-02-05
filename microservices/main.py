from fastapi import FastAPI, Request, HTTPException, Depends, Body
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
import mysql.connector
import grpc
import os
import asyncio
import aiomysql
# switch to pyodbc or asyncodbc for azure SQL

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
SECRET_KEYS = {
    "current": "new_secret_key",
    "previous": "old_secret_key"
}
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10 #per half minute
REFRESH_TOKEN_EXPIRE_DAYS = 7
user_data = {}
sensitive_data = {}
body_data = {}

app = FastAPI()

def rotate_keys():
    SECRET_KEYS["previous"] = SECRET_KEYS["current"]  # Move current to previous
    SECRET_KEYS["current"] = os.urandom(32).hex()  # Generate new key
    print(f"New secret key: {SECRET_KEYS['current']}")

def create_jwt(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        to_encode["exp"] = int((datetime.now(timezone.utc) + expires_delta).timestamp())
    else:
        to_encode["exp"] = int((datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    print(f"Data: {to_encode}")
    return jwt.encode(to_encode, SECRET_KEYS["current"], algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = int((datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)).timestamp())
    to_encode = {"exp": expire, **data}
    return jwt.encode(to_encode, SECRET_KEYS["current"], algorithm=ALGORITHM)

def decode_jwt(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEYS["current"], algorithms=[ALGORITHM])
        exp = payload.get("exp")
        current_time = int(datetime.now(timezone.utc).timestamp())
        print(f"Time to expiration: {exp - current_time}")
        if current_time > exp:
            raise HTTPException(status_code=401, detail="Token has expired")
        print(f"Payload at decoding: {payload}")
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        try:
            payload = jwt.decode(token, SECRET_KEYS["previous"], algorithms=[ALGORITHM])
            print(f"Payload at decoding: {payload}")
            return payload
        except:
            raise HTTPException(status_code=401, detail="Invalid token")
    
def verify_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEYS["current"], algorithms=[ALGORITHM])
        print(f"\nPayload: {payload}")
        return payload
    except JWTError as err:
        print(f"\nError: {err}")
        try:
            payload = jwt.decode(refresh_token, SECRET_KEYS["previous"], algorithms=[ALGORITHM])
            return payload
        except:
            raise HTTPException(status_code=401, detail="Invalid token")
        # Do I need to check the previous key for refresh tokens?? 

# def encode_jwt(data: Dict) -> str:
#     expiry = (datetime.now(timezone.utc) + expires_delta).timestamp()
#     data["exp"] = expiry
#     return jwt.encode(data, SECRET_KEYS, algorithm=ALGORITHM)
# should have same expiry as user's token

async def create_pool():
    try:
        pool = await aiomysql.create_pool(
            host="localhost",
            user="root",
            password="Root1234",
            db="yaya_dev",
            autocommit=True,
            minsize=1,
            maxsize=10
        )
        return pool
    except aiomysql.Error as e:
        print(f"Database connection error: {e}")
        return None

async def get_current_user(username: str, pw: str):
    pool = await create_pool()
    if not pool:
        raise HTTPException(status_code=503, detail="Database connection failed")

    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT user_id, username, first_name, last_name, email, location, language, gender, age, spend_class, notifications, music_service, established FROM user_data WHERE username = %s AND pw = %s;", (username, pw))
                response_data = await cursor.fetchone()
                if not response_data:
                    raise HTTPException(status_code=401, detail="User not found")
                columns = [desc[0] for desc in cursor.description]
                user_data = dict(zip(columns, response_data))
                return user_data
    except aiomysql.Error as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
    finally:
        pool.close()
        await pool.wait_closed()
        print("\nPool closed")

@app.post("/login")
async def login(creds: dict = Body(...)):
    username = creds.get("username")
    pw = creds.get("pw")
    if not username or not pw:
        raise HTTPException(status_code=401, detail="Missing credentials")
    
    user_data = await get_current_user(username, pw)
    sensitive_data['username'] = username
    sensitive_data['pw'] = pw
    print(f"\nUser data: {user_data}")
    print(f"\nSenitive data: {sensitive_data}")

    token = create_jwt(user_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(user_data)
    return {"access_token": token, "refresh_token": refresh_token}

@app.post("/refresh")
def refresh_access_token(body: dict=Body(...)):
    refresh_token = body.get("refresh_token")
    print(f"Refresh token: {refresh_token}")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = verify_refresh_token(refresh_token)
    new_access_token = create_jwt(payload)
    return {"access_token": new_access_token}


@app.get("/protected")
def protected(token: str):
    user = decode_jwt(token)
    return {"message": f"Hello, User {user['user_id']}!", "other_data": user}

@app.get("/new_key")
def refresh_key_manual():
    rotate_keys()


@app.get("/")
async def route_to_service(user: Dict = Depends(get_current_user)):
    """
    Example route that authenticates user and forwards the request to another microservice via gRPC.
    """
    try:
        # Example of calling a gRPC service (pseudo-code, replace with actual gRPC client call)
        # async with grpc.aio.insecure_channel('localhost:50051') as channel:
        #     stub = SomeServiceStub(channel)
        #     response = await stub.SomeMethod(SomeRequest(user_id=user["id"]))

        response_data = {"message": "Data from gRPC service", "user": user}
        
        # Encrypt response
        encrypted_response = encode_jwt(response_data)
        return {"data": encrypted_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")