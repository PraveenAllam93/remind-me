import json
import time
import traceback
from typing import Dict

import redis

from config.redis_config import get_redis_pool, pool
from config.settings import settings
from exceptions import RedisServiceException
from logs import get_app_logger, get_error_logger

app_logger = get_app_logger()
error_logger = get_error_logger()


def get_redis_hash_values(
    key: str,
    hash_value: str = None,
    db: int = settings.REDIS_DB,
    all_tasks: bool = False,
) -> bool:
    try:
        redis_client = get_redis_pool(pool)
        if hash_value is None:
            all_tasks = True
        if not redis_client.exists(key):
            app_logger.info(f"Key: '{key}', does not exist in Redis")
            return False
        values = (
            redis_client.hgetall(key)
            if all_tasks
            else redis_client.hget(key, hash_value)
        )
        if values is not None:
            values = (
                {
                    k.decode("utf-8"): json.loads(v.decode("utf-8"))
                    for k, v in values.items()
                }
                if all_tasks
                else json.loads(values.decode("utf-8"))
            )
            app_logger.info(
                f"Successfully retrieved value for key: '{key}' and hash: '{hash_value}' from Redis DB: {db}"
            )
            return values
        app_logger.info(
            f"No values found for key: '{key}' and hash: '{hash_value}' from Redis DB: {db}"
        )
        return False
    except redis.RedisError as e:
        error_logger.error(
            f"Failed to get value for key: '{key}' from Redis DB: {db} => {str(e)}\n\n{traceback.format_exc()}"
        )
        return False


def set_redis_hash_values(
    key: str,
    values: Dict[str, dict],
):
    """
    Store multiple hashes under a single Redis key.

    :param key: The main Redis key (e.g., "test")
    :param hashes: Dictionary where keys are hash names (e.g., "test1") and values are lists of dicts
    """

    redis_client = get_redis_pool(pool)

    try:
        formatted_hashes = {
            hash_name: json.dumps(value) for hash_name, value in values.items()
        }
        redis_client.hset(key, mapping=formatted_hashes)
        app_logger.info(f"Successfully stored multiple hashes in Redis key ''{key}''")
        return True

    except Exception as e:

        error_logger.error(f"Error while storing hashes into redis, key: ''{key}''.")
        raise RedisServiceException(
            message=f"Error while storing hashes into redis, key: '{key}'",
            original_exception=e,
        )


def delete_redis_key(key: str):
    try:
        redis_client = get_redis_pool(pool)

        if not redis_client.exists(key):
            app_logger.warning(f"Key: '{key}', does not exist in Redis to flush")
            return True

        redis_client.delete(key)
        app_logger.info(f"key: '{key}' deleted.")
        return True
    except redis.RedisError as e:
        error_logger.error(
            f"Error while deleting redis key, key: ''{key}''. Error: {str(e)}", e
        )
        raise RedisServiceException(
            message=f"Error while deleting redis key, key: '{key}'",
            original_exception=e,
        )


def delete_redis_hash(key: str, hash_value: str):
    try:
        redis_client = get_redis_pool(pool)

        if not redis_client.exists(key):
            app_logger.warning(f"Key: '{key}', does not exist in Redis to flush")
            return True

        redis_client.hdel(key, hash_value)
        app_logger.info(f"key: '{key}' for hash: '{hash_value}' deleted.")
        return True
    except redis.RedisError as e:
        error_logger.error(
            f"Error while deleting redis key, key: '{key}' for hash: '{hash_value}'. Error: {str(e)}",
            e,
        )
        return False


def push_redis_value(
    key: str, hash_value: str, value: str, max_retries: int = settings.REDIS_MAX_RETRIES
):
    lock = f"lock:{key}:{hash_value}"
    redis_client = get_redis_pool(pool)
    retry_delay = 0.1

    for _ in range(max_retries):
        if redis_client.set(lock, "1", nx=True, ex=2):
            try:
                current_values = redis_client.hget(key, hash_value)
                current_list = json.loads(current_values) if current_values else []

                current_list.append(value)

                redis_client.hset(key, hash_value, json.dumps(current_list))
                return True
            finally:
                redis_client.delete(lock)
        else:
            time.sleep(retry_delay)

    raise RedisServiceException(
        f"Not able to set values for {hash_value}, not able to accquire lock."
    )
