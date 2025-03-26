import os
import asyncio
import asyncmy
import uvicorn
import json

from fastapi import FastAPI
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../env/.env")

load_dotenv(dotenv_path=dotenv_path)

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_SCHEMA = os.getenv("MYSQL_SCHEMA")
PORT = int(os.getenv("PYTHON_PORT"))

pool: asyncmy.Pool | None = None

async def init_db():
    """Connect to database"""
    global pool
    if pool is None:
        try:
    
            pool = await asyncmy.create_pool(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_SCHEMA,
                minsize=5,
                maxsize=20
            )
            print("MySQL pool connected")
        except Exception as e:
            print(f"Database connect error: {e}")
            pool = None

async def get_data():
    """Return data from database"""
    if pool is None:
        print("Database pool error.")
        return None

    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT * FROM test WHERE name = %s LIMIT 1", ('amount',))
            result = await cursor.fetchone()
    return result

async def update_amount(amount):
    """Update amount in database"""
    if pool is None:
        print("Database pool error.")
        return

    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("UPDATE test SET code = %s WHERE name = %s", (amount, 'amount'))
            await connection.commit()


amount = 1
async def app(scope, receive, send):
    """Start http-server app"""
    global amount

    if scope["type"] == "lifespan":
        event = await receive()
        if event["type"] == "lifespan.startup":
            await init_db()
            await update_amount(0)
            await send({"type": "lifespan.startup.complete"})
        return

    if scope["type"] == "http":
        path = scope['path']
        amount += 1

        if path == "/endpoint_slow":
            result = await get_data()
            await update_amount(amount)
            response_body = json.dumps({"amount": amount, "result": result})

        elif path == "/endpoint_fast":
            response_body = json.dumps({"amount": amount})

        else:
            response_body = json.dumps({"error": "Not Found"})
            status = 404
            headers = [(b"content-type", b"application/json")]
            await send({"type": "http.response.start", "status": status, "headers": headers})
            await send({"type": "http.response.body", "body": response_body.encode("utf-8")})
            return

        headers = [(b"content-type", b"application/json")]
        await send({"type": "http.response.start", "status": 200, "headers": headers})
        await send({"type": "http.response.body", "body": response_body.encode("utf-8")})
