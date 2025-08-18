from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    
async def connect_to_mongo():
    """Create database connection"""
    Database.client = AsyncIOMotorClient(settings.MONGODB_URL)
    
async def close_mongo_connection():
    """Close database connection"""
    if Database.client:
        Database.client.close()
        
def get_database() -> AsyncIOMotorClient:
    """Get database instance"""
    return Database.client[settings.DATABASE_NAME]
