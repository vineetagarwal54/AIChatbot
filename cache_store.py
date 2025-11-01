# cache store logic

from typing import Optional
import os
import logging
import redis

USE_REDIS = False

try:
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    _client = redis.Redis.from_url(REDIS_URL)
    _client.ping()  # Check if Redis is available
    USE_REDIS = True
    logging.info(f"Redis is available and will be used for caching. {REDIS_URL}")

except Exception as e:
    logging.warning(f"Redis is not available: {e}. Caching will not be used.")
    USE_REDIS = False
    _client = {}

logging.info(f"Cache Backend: {'Redis' if USE_REDIS else 'In-Memory'}")

def _key(key: str) -> str:
    """Generate a cache key."""
    return f"genai:cache:{key}"

def get(key: str) -> Optional[str]:
    """Get a value from the cache."""
    if USE_REDIS:
        value = _client.get(_key(key))
        return value.decode('utf-8') if value else None
    else:
        value, expiry = _client.get(_key(key), (None, None))
        if time.time() < expiry:
            return value
        return None
    
def set(key: str, value: str, ttl: int = 3600) -> None:
    """Set a value in the cache with an optional TTL."""
    if USE_REDIS:
        _client.setex(_key(key), ttl, value)
    else:
        _client[_key(key)] = (value, time.time() + ttl)  # Store value with expiry time