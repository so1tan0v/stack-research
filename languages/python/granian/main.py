import asyncio
import logging
import os
import sys

import asyncmy
import orjson
from dotenv import load_dotenv
from granian import Granian
from granian.constants import Interfaces, Loops
from granian.rsgi import HTTPProtocol, Scope


dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../env/.env")

load_dotenv(dotenv_path=dotenv_path)

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "testuser")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "testpassword")
MYSQL_SCHEMA = os.getenv("MYSQL_SCHEMA", "research")
MYSQL_AUTH_PLUGIN = os.getenv("MYSQL_AUTH_PLUGIN", "mysql_native_password")
PORT = int(os.getenv("PYTHON_PORT", 3001))

ALLOWED_CONTENT_TYPE = "application/json"
NOT_FOUND_ERR_BODY_RESPONSE = b"Not Found"
HEADERS = [("content-type", ALLOWED_CONTENT_TYPE)]
TEXT_HEADERS = [("content-type", "text/plain")]

DB_CONNECTION_POOL: asyncmy.Pool | None = None
TEST_AMOUNT = 0

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

app = Granian(
    "main:main",
    factory=True,  # use factory mode for initialization setup (see `initial_startup()`)
    interface=Interfaces.RSGI,
    loop=Loops.uvloop,
    address="0.0.0.0",
    port=PORT,
)


async def init_db():
    """Connect to database"""
    global DB_CONNECTION_POOL

    if DB_CONNECTION_POOL is None:
        try:

            DB_CONNECTION_POOL = await asyncmy.create_pool(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_SCHEMA,
                minsize=5,
                maxsize=20,

            )
            logger.info("MySQL pool connected")
        except Exception as e:
            logger.error(f"Database connect error: {e!r}")
            DB_CONNECTION_POOL = None


async def get_data():
    """Return data from database"""
    if DB_CONNECTION_POOL is None:
        logger.error("Database pool error.")
        return None

    async with DB_CONNECTION_POOL.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT * FROM test WHERE name = %s LIMIT 1", ('amount',))
            result = await cursor.fetchone()

    return result


async def update_amount(amount):
    """Update amount in database"""
    if DB_CONNECTION_POOL is None:
        logger.error("Database pool error.")
        return

    async with DB_CONNECTION_POOL.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("UPDATE test SET code = %s WHERE name = %s", (amount, 'amount'))
            await connection.commit()


async def handle_request(scope: Scope, protocol: HTTPProtocol):
    """Start http-server app"""
    global TEST_AMOUNT

    TEST_AMOUNT += 1

    path = scope.path
    if path == "/endpoint_slow":
        result = await get_data()
        await update_amount(TEST_AMOUNT)
        response_body = {"amount": TEST_AMOUNT, "result": result}

    elif path == "/endpoint_fast":
        response_body = {"amount": TEST_AMOUNT}

    else:
        protocol.response_bytes(404, HEADERS, NOT_FOUND_ERR_BODY_RESPONSE)
        return

    protocol.response_bytes(200, HEADERS, orjson.dumps(response_body))


async def handle_404(_: Scope, protocol: HTTPProtocol):
    protocol.response_bytes(404, TEXT_HEADERS, NOT_FOUND_ERR_BODY_RESPONSE)


async def initial_startup():
    await init_db()
    await update_amount(0)


def controller(scope, proto):
    if scope.proto == "http":
        return handle_request(scope, proto)

    return handle_404(scope, proto)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initial_startup())

    return controller


if __name__ == "__main__":
    try:
        app.serve()
    except KeyboardInterrupt:
        pass
