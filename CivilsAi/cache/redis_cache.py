import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis_cache")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

class RedisCache:
    def __init__(self):
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value, expiry=300):
        self.client.setex(key, expiry, value)

    def delete(self, key):
        self.client.delete(key)

cache = RedisCache()
