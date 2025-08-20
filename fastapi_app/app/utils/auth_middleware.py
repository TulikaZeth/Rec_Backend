from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from ..utils.auth import AuthUtils
from ..services.user_service import UserService

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
