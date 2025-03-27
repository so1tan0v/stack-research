# python3 main.py

import os
import asyncio
import asyncmy
import uvicorn
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

amount = 0
app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()
    if pool is not None:
        await update_amount(0)

@app.get("/endpoint_slo ")
async def endpoint_slow():
    global amount
    amount += 1

    result = await get_data()
    await update_amount(amount)

    response = {"amount": amount}
    if result:
        response["result"] = result

    return response


@app.get("/endpoint_fast")
async def endpoint_slow():
    global amount
    amount += 1
    response = {"amount": amount}

    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
