from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, JSONResponse
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import asyncpg
import asyncio
import json
import os

load_dotenv()

POSTGRE_DB = os.getenv("POSTGRE_DB")
POSTGRE_USER = os.getenv("POSTGRE_USER")
POSTGRE_PW = os.getenv("POSTGRE_PW")
POSTGRE_HOST = os.getenv("POSTGRE_HOST")
POSTGRE_READ_PORT = os.getenv("POSTGRE_READ_PORT")

db_pool = None


# APP DEFINITION
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating pool...")

    global db_pool
    db_pool = await asyncpg.create_pool(
        database=POSTGRE_DB,
        user=POSTGRE_USER,
        password=POSTGRE_PW,
        host=POSTGRE_HOST,
        port=POSTGRE_READ_PORT,
        min_size=3,
        max_size=5
    )
    print("✅ Database pool created")
    
    yield  # This is where the app runs

    await db_pool.close()
    print("🛑 Database pool closed")

app = FastAPI(lifespan=lifespan)


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
    FROM event_data pe
    LEFT JOIN venues v ON pe.venue_id = v.id
    LEFT JOIN organizer o ON pe.organizer_id = o.id
    WHERE pe.id = $1
    """
    async with db_pool.acquire() as conn:
        result = await conn.fetchrow(query, event_id)
        if not result:
            return JSONResponse({"error": "Event not found"}, status_code=404)
        return dict(result)

