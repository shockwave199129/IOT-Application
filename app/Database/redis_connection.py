import aioredis
from Core.config import setting


class RedisDB:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(setting.REDIS_URL, decode_responses=True)

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def __call__(self):
        return self


redis_db = RedisDB()
