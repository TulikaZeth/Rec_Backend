from typing import List, Optional
from ..models.user import User
from ..core.init_db import get_database
from ..schemas.user_schema import UserCreate, ShortlistUpdate, GDUpdate, PIUpdate, TaskUpdate
from odmantic import ObjectId

class UserService:
    """Service for handling user operations"""
    
    @staticmethod
    async def create_user(user: UserCreate) -> User:
        """Create a new user in the database"""
        engine = get_database()
        
        # Convert Pydantic model to dict
        user_dict = user.dict()
        print("Received user data:", user_dict)
        
        # Convert domain preferences to dict format (already in correct format)
        # No need to modify domain_pref_one and domain_pref_two as they're already dicts
        
        # Remove explicit None setting - let ODMantic use default_factory=dict
        # The optional fields will automatically get empty dicts as defaults
        
        # Create ODMantic user instance
        new_user = User(**user_dict)
        
        # Save using ODMantic engine
        saved_user = await engine.save(new_user)
        
        return saved_user
        
    @staticmethod
    async def get_user(user_id: str) -> Optional[User]:
        """Get user by ID"""
        engine = get_database()
        try:
            # Convert string ID to ObjectId if needed
            obj_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
            user = await engine.find_one(User, User.id == obj_id)
            return user
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email ID"""
        engine = get_database()
        try:
            user = await engine.find_one(User, User.email == email)
            return user
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    @staticmethod
    async def get_users() -> List[User]:
        """Get all users"""
        engine = get_database()
        users = await engine.find(User)
        return list(users)
    
    @staticmethod
    async def update_shortlist(user_id: str, update: ShortlistUpdate) -> Optional[User]:
        """Update user's shortlist status"""
        engine = get_database()
        user = await UserService.get_user(user_id)
        if not user:
            return None
            
        # Convert update to dict
        update_dict = update.dict()
        
        # Update the shortlisted field
        user.shortlisted = update_dict
        
        # Save the updated user
        updated_user = await engine.save(user)
        return updated_user
    
    @staticmethod
    async def update_gd(user_id: str, update: GDUpdate) -> Optional[User]:
        """Update user's GD status"""
        engine = get_database()
        user = await UserService.get_user(user_id)
        if not user:
            return None
            
        # Convert update to dict
        update_dict = update.dict()
        
        # Update the gd field
        user.gd = update_dict
        
        # Save the updated user
        updated_user = await engine.save(user)
        return updated_user
    
    @staticmethod
    async def update_pi(user_id: str, update: PIUpdate) -> Optional[User]:
        """Update user's PI status"""
        engine = get_database()
        user = await UserService.get_user(user_id)
        if not user:
            return None
            
        # Convert update to dict
        update_dict = update.dict()
        
        # Update the pi field
        user.pi = update_dict
        
        # Save the updated user
        updated_user = await engine.save(user)
        return updated_user
    
    @staticmethod
    async def update_task(user_id: str, update: TaskUpdate) -> Optional[User]:
        """Update user's task status"""
        engine = get_database()
        user = await UserService.get_user(user_id)
        if not user:
            return None
            
        # Convert update to dict
        update_dict = update.dict()
        
        # Update the task field
        user.task = update_dict
        
        # Save the updated user
        updated_user = await engine.save(user)
        return updated_user