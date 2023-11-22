from motor.motor_asyncio import AsyncIOMotorClient
from Core.config import setting

class MongoDB:
    def __init__(self):
        self.client = None

    async def connect(self):
        self.client = AsyncIOMotorClient(setting.DB_URL)

    async def close(self):
        if self.client:
            self.client.close()

mongo_db = MongoDB()
