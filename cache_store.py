# cache store logic

from typing import Optional
import os
import logging
import time
try:
    import redis
except Exception:
    redis = None

USE_REDIS = False

try:
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    if redis:
        _client = redis.Redis.from_url(REDIS_URL)
        _client.ping()  # Check if Redis is available
        USE_REDIS = True
        logging.info(f"Redis is available and will be used for caching. {REDIS_URL}")
    else:
        raise RuntimeError("redis library not installed")
except Exception as e:
    logging.warning(f"Redis is not available: {e}. Falling back to in-memory cache.")
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
        entry = _client.get(_key(key))
        if not entry:
            return None
        value, expiry = entry
        # If expiry is None or invalid, treat as expired
        try:
            if time.time() < expiry:
                return value
        except Exception:
            return None
        # expired - remove and return None
        _client.pop(_key(key), None)
        return None
    
def set(key: str, value: str, ttl: int = 3600) -> None:
    """Set a value in the cache with an optional TTL."""
    if USE_REDIS:
        _client.setex(_key(key), ttl, value)
    else:
        _client[_key(key)] = (value, time.time() + ttl)  # Store value with expiry time