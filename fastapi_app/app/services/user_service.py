from typing import List, Optional
from ..models.user import User
from ..core.init_db import get_database
from ..schemas.user_schema import UserCreate, ShortlistUpdate, GDUpdate, PIUpdate, TaskUpdate

class UserService:
    """Service for handling user operations"""
    
    @staticmethod
    async def create_user(user: UserCreate) -> User:
        """Create a new user"""
        db = get_database()
        user_dict = user.model_dump()
        new_user = User(**user_dict)
        await db.users.insert_one(new_user.model_dump())
        return new_user
    
    @staticmethod
    async def get_user(user_id: str) -> Optional[User]:
        """Get user by ID"""
        db = get_database()
        user_data = await db.users.find_one({"_id": user_id})
        return User(**user_data) if user_data else None
    
    @staticmethod
    async def get_users() -> List[User]:
        """Get all users"""
        db = get_database()
        users = []
        cursor = db.users.find({})
        async for user_data in cursor:
            users.append(User(**user_data))
        return users
    
    @staticmethod
    async def update_shortlist(user_id: str, update: ShortlistUpdate) -> Optional[User]:
        """Update user's shortlist status"""
        db = get_database()
        update_dict = update.model_dump()
        await db.users.update_one(
            {"_id": user_id},
            {"$push": {"shortlisted": update_dict}}
        )
        return await UserService.get_user(user_id)
    
    @staticmethod
    async def update_gd(user_id: str, update: GDUpdate) -> Optional[User]:
        """Update user's GD status"""
        db = get_database()
        update_dict = update.model_dump()
        await db.users.update_one(
            {"_id": user_id},
            {"$set": {"gd": update_dict}}
        )
        return await UserService.get_user(user_id)
    
    @staticmethod
    async def update_pi(user_id: str, update: PIUpdate) -> Optional[User]:
        """Update user's PI status"""
        db = get_database()
        update_dict = update.model_dump()
        await db.users.update_one(
            {"_id": user_id},
            {"$set": {"pi": update_dict}}
        )
        return await UserService.get_user(user_id)
    
    @staticmethod
    async def update_task(user_id: str, update: TaskUpdate) -> Optional[User]:
        """Update user's task status"""
        db = get_database()
        update_dict = update.model_dump()
        await db.users.update_one(
            {"_id": user_id},
            {"$set": {"task": update_dict}}
        )
        return await UserService.get_user(user_id)
