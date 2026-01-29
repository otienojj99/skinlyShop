import redis
from app.core.config import settings


redis_clent = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_response = True
)