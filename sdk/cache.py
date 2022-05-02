import redis
from decouple import config

r = redis.Redis(
    host=config("REDIS_HOST", default="localhost"),
    port=config("REDIS_PORT", default=6379, cast=int),
    db=config("REDIS_DB", default=0, cast=int),
    password=config("REDIS_PASSWORD", default=None)
)


def get(key):
    return r.get(key);

def set(key, value):
    return r.set(key, value);
