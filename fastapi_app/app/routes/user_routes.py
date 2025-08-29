from fastapi import APIRouter, HTTPException, status, Depends, Body
from typing import List
from ..schemas.user_schema import (
    UserCreate, UserResponse, screeningUpdate,
    GDUpdate, PIUpdate, TaskUpdate
)
from ..services.user_service import UserService

# Inline schema for bulk round update (no extra packages)
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class BulkRoundUpdateRequest(BaseModel):
    emails: List[EmailStr]
    screening: Optional[dict] = None  # {"status": str, "datetime": datetime}
    gd: Optional[dict] = None         # {"status": str, "datetime": datetime, "remarks": str}
    pi: Optional[dict] = None         # {"status": str, "datetime": datetime, "remarks": list}



# ...existing code...

from ..utils.auth_middleware import get_current_user, get_current_user_optional
from ..models.user import User

router = APIRouter(prefix="/users", tags=["users"])

# ...existing route definitions...

from fastapi.responses import JSONResponse

class BulkUpdateResponse(BaseModel):
    updated: List[EmailStr]
    failed: List[dict]


from ..utils.auth_middleware import get_current_user, get_current_user_optional
from ..models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user"""
    try:
        created_user = await UserService.create_user(user)
        # Convert ODMantic model to dict and convert ObjectId to string
        user_dict = created_user.dict()
        user_dict['id'] = str(created_user.id)  # Convert ObjectId to string
        return UserResponse(**user_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create user: {str(e)}"
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    """Get user by ID (requires authentication)"""
    try:
        user = await UserService.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        # Convert ODMantic model to response schema
        user_dict = user.dict()
        user_dict['id'] = str(user.id)  # Convert ObjectId to string
        return UserResponse(**user_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get user: {str(e)}"
        )

@router.get("/", response_model=List[UserResponse])
async def get_users():
    """Get all users (requires authentication)"""
    try:
        users = await UserService.get_users()
        # Convert each ODMantic model to response schema
        response_users = []
        for user in users:
            user_dict = user.dict()
            user_dict['id'] = str(user.id)  # Convert ObjectId to string
            response_users.append(UserResponse(**user_dict))
        return response_users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get users: {str(e)}"
        )

@router.get("/email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, current_user: User = Depends(get_current_user)):
    """Get user by email ID (requires authentication)"""
    try:
        user = await UserService.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found with this email"
            )
        # Convert ODMantic model to response schema
        user_dict = user.dict()
        user_dict['id'] = str(user.id)  # Convert ObjectId to string
        return UserResponse(**user_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get user by email: {str(e)}"
        )

@router.put("/{user_id}/screening", response_model=UserResponse)
async def update_screening(user_id: str, update: screeningUpdate):
    """Update user's screening status"""
    try:
        user = await UserService.update_screening(user_id, update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user_dict = user.dict()
        user_dict['id'] = str(user.id)
        return UserResponse(**user_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update screening: {str(e)}"
        )

@router.put("/{user_id}/gd", response_model=UserResponse)
async def update_gd(user_id: str, update: GDUpdate):
    """Update user's GD status"""
    try:
        user = await UserService.update_gd(user_id, update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user_dict = user.dict()
        user_dict['id'] = str(user.id)
        return UserResponse(**user_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update GD status: {str(e)}"
        )

@router.put("/{user_id}/pi", response_model=UserResponse)
async def update_pi(user_id: str, update: PIUpdate):
    """Update user's PI status"""
    try:
        user = await UserService.update_pi(user_id, update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user_dict = user.dict()
        user_dict['id'] = str(user.id)
        return UserResponse(**user_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update PI status: {str(e)}"
        )

@router.put("/{user_id}/task", response_model=UserResponse)
async def update_task(user_id: str, update: TaskUpdate):
    """Update user's task status"""
    try:
        user = await UserService.update_task(user_id, update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user_dict = user.dict()
        user_dict['id'] = str(user.id)
        return UserResponse(**user_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update task status: {str(e)}"
        )

@router.put(
    "/bulk/update-rounds",
    response_model=BulkUpdateResponse,
)
async def bulk_update_rounds(
    payload: BulkRoundUpdateRequest = Body(
        ...,
        example={
            "emails": ["user1@example.com", "user2@example.com"],
            "screening": {"status": "passed", "datetime": "2025-08-24T10:00:00", "remarks": "To be scheduled"},
            "gd": {"status": "pending", "datetime": "2025-08-25T14:00:00", "remarks": "To be scheduled"},
            "pi": {"status": "not started", "datetime": "2025-08-26T16:00:00", "remarks": "To be scheduled"}
        }
    )
):
    """
    Bulk update screening, gd, and pi rounds for multiple users by email.
    - **emails**: List of user emails to update
    - **screening**: Dict with status and datetime (optional)
    - **gd**: Dict with status, datetime, remarks (optional)
    - **pi**: Dict with status, datetime, remarks (optional)
    """
    updated = []
    failed = []
    for email in payload.emails:
        user = await UserService.get_user_by_email(email)
        if not user:
            failed.append({"email": email, "reason": "User not found"})
            continue
        try:
            if payload.screening:
                user.screening = payload.screening
            if payload.gd:
                user.gd = payload.gd
            if payload.pi:
                user.pi = payload.pi
            engine = UserService.get_engine()
            await engine.save(user)
            updated.append(email)
        except Exception as e:
            failed.append({"email": email, "reason": str(e)})
    return BulkUpdateResponse(updated=updated, failed=failed)