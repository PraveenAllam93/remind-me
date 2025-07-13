import redis

from config.settings import settings
from logs import get_app_logger

app_logger = get_app_logger()

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT


def setup_redis(db=settings.REDIS_DB) -> redis.ConnectionPool:
    # create the connection once and reuse that pool
    return redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=db)


pool = setup_redis()


def get_redis_pool(redis_pool):
    if redis_pool is None:
        app_logger.warning(
            "🚨 Redis not initialized. Make sure to call setup_redis() during app startup"
        )
    return redis.Redis(connection_pool=redis_pool)
