from redis.asyncio import ConnectionPool, Redis
from app.config import settings
pool: ConnectionPool | None=None
redis_client:Redis | None=None

# connect
async def init_redis()->None:
    global pool,redis_client
    pool=ConnectionPool.from_url(settings.redis_url,decode_responses=True)
    redis_client=Redis(connection_pool=pool)
    await redis_client.ping()

# Disconnect when application shut down
async def close_redis()-> None:
    global pool,redis_client
    if redis_client:
        await redis_client.aclose()
        redis_client=None
    if pool:
        await pool.disconnect()
        pool=None
# Use
def get_redis()->Redis:
    if redis_client is None:
        raise RuntimeError("Redis is not Initialized")
    return redis_client