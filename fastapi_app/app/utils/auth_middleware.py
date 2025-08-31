from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List

from ..utils.auth import AuthUtils
from ..services.user_service import UserService
from ..services.admin_service import AdminService
from ..utils.enums import UserRole

# Create security scheme
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get current authenticated user from JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify token
        payload = AuthUtils.verify_token(credentials.credentials)
        if payload is None or payload.get("type") != "access":
            raise credentials_exception
        
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
            
        # Get user from database
        user = await UserService.get_user(user_id)
        if user is None:
            raise credentials_exception
            
        return user
        
    except HTTPException:
        raise
    except Exception:
        raise credentials_exception

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get current authenticated admin from JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify token
        payload = AuthUtils.verify_token(credentials.credentials)
        if payload is None or payload.get("type") != "access":
            raise credentials_exception
        
        admin_id: str = payload.get("admin_id")
        admin_email: str = payload.get("email")
        if admin_id is None:
            raise credentials_exception
        
        if admin_email is None:
            raise credentials_exception
            
        # Get admin from database
        admin = await AdminService.get_admin_by_email(admin_email)
        
        if admin is None:
            raise credentials_exception
            
        return admin
        
    except HTTPException:
        raise
    except Exception:
        raise credentials_exception

def require_roles(allowed_roles: List[UserRole]):
    """
    Dependency factory to create role-based authorization
    """
    async def role_checker(current_admin = Depends(get_current_admin)):
        if current_admin.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[role.value for role in allowed_roles]}"
            )
        return current_admin
    return role_checker

async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))):
    """
    Optional dependency to get current user (for endpoints that work with or without auth)
    """
    if credentials is None:
        return None
    
    try:
        payload = AuthUtils.verify_token(credentials.credentials)
        if payload is None or payload.get("type") != "access":
            return None
        
        user_id: str = payload.get("user_id")
        if user_id is None:
            return None
            
        user = await UserService.get_user(user_id)
        return user
        
    except Exception:
        return None
