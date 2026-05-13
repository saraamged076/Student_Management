import redis

redis_client = redis.Redis(
    host="redis_cache",
    port=6379,
    db=0,
    decode_responses=True
)