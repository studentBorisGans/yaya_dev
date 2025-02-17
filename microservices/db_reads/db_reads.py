from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, JSONResponse
import asyncpg
import asyncio
import json
from contextlib import asynccontextmanager


db_pool = None


# APP DEFINITION
@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool
    db_pool = await asyncpg.create_pool(
        database="postgres",
        user="user",
        password="password",
        host="localhost",
        port=5433,
        min_size=3,
        max_size=10
    )
    print("✅ Database pool created")
    
    yield  # This is where the app runs

    await db_pool.close()
    print("🛑 Database pool closed")

app = FastAPI(lifespan=lifespan)


# async def init_db():
#     global db_pool
#     db_pool = await asyncpg.create_pool(
#         database="postgres",
#         user="user",
#         password="password",
#         host="localhost",
#         port=5433,
#         min_size=1,
#         max_size=5
#     )
#     print("✅ Database pool created")

# async def close_db():
#     global db_pool
#     if db_pool:
#         await db_pool.close()
#         print("🛑 Database pool closed")

# @app.on_event("startup")
# async def startup():
#     await init_db()

# @app.on_event("shutdown")
# async def shutdown():
#     await close_db()



# --------------- Streaming Endpoints ----------------

async def stream_query(query: str, *params):
    """Helper function to stream query results as JSON."""
    async with db_pool.acquire() as conn:
        async with conn.transaction():
            async for record in conn.cursor(query, *params):
                yield json.dumps(dict(record)) + "\n"

@app.get("/events", response_class=StreamingResponse)
async def get_events():
    """Stream all events from event_data & published_events."""

    query = """
    SELECT * FROM event_data
    UNION ALL
    SELECT * FROM published_events;
    """
    return StreamingResponse(stream_query(query), media_type="application/json")

@app.get("/djs", response_class=StreamingResponse)
async def get_djs():
    """Stream all DJs with their socials."""
    query = """
    SELECT dj.*, dj_socials.*
    FROM dj
    LEFT JOIN dj_socials ON dj.id = dj_socials.dj_id;
    """
    return StreamingResponse(stream_query(query), media_type="application/json")

# --------------- Direct Proxy Endpoints ----------------
@app.get("/event/{event_id}")
async def get_event_details(event_id: int):
    """Fetch detailed event info including venue & organizer."""
    
    query = """
    SELECT pe.*, v.*, o.*
    FROM published_events pe
    LEFT JOIN venues v ON pe.venue_id = v.id
    LEFT JOIN organizers o ON pe.organizer_id = o.id
    WHERE pe.id = $1
    """
    async with db_pool.acquire() as conn:
        result = await conn.fetchrow(query, event_id)
        if not result:
            return JSONResponse({"error": "Event not found"}, status_code=404)
        return dict(result)

