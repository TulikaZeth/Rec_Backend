from typing import Optional, Tuple
from datetime import datetime
from ..models.admin import Admin, AdminCreate, AdminLogin
from ..utils.auth import AuthUtils
from ..core.init_db import get_database

class AdminService:
    """Service class for admin operations"""
    
    @staticmethod
    async def create_admin(admin_data: AdminCreate) -> Admin:
        """Create a new admin user"""
        engine = get_database()
        
        # Check if admin with email already exists
        existing_admin = await engine.find_one(Admin, Admin.email == admin_data.email)
        if existing_admin:
            raise ValueError("Admin with this email already exists")
        
        # Hash the password
        password_hash = AuthUtils.hash_password(admin_data.password)
        
        # Create admin
        admin = Admin(
            name=admin_data.name,
            email=admin_data.email,
            password_hash=password_hash,
            role=admin_data.role
        )
        
        return await engine.save(admin)
    
    @staticmethod
    async def authenticate_admin(login_data: AdminLogin) -> Tuple[bool, Optional[Admin], str]:
        """Authenticate admin user"""
        try:
            engine = get_database()
            
            # Find admin by email
            admin = await engine.find_one(Admin, Admin.email == login_data.email)
            if not admin:
                return False, None, "Invalid email or password"
            
            # Check if admin is active
            if not admin.is_active:
                return False, None, "Account is deactivated"
            
            # Verify password
            if not AuthUtils.verify_password(login_data.password, admin.password_hash):
                return False, None, "Invalid email or password"
            
            # Update last login
            admin.last_login = datetime.utcnow()
            await engine.save(admin)
            
            return True, admin, "Login successful"
            
        except Exception as e:
            return False, None, f"Authentication failed: {str(e)}"
    
    @staticmethod
    async def get_admin(admin_id: str) -> Optional[Admin]:
        """Get admin by ID"""
        try:
            engine = get_database()
            return await engine.find_one(Admin, Admin.id == admin_id)
        except Exception:
            return None
    
    @staticmethod
    async def get_admin_by_email(email: str) -> Optional[Admin]:
        """Get admin by email"""
        try:
            engine = get_database()
            return await engine.find_one(Admin, Admin.email == email)
        except Exception:
            return None
        
    
