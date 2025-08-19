from fastapi import APIRouter, HTTPException, status
from typing import List
from ..schemas.user_schema import (
    UserCreate, UserResponse, ShortlistUpdate,
    GDUpdate, PIUpdate, TaskUpdate
)
from ..services.user_service import UserService

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
async def get_user(user_id: str):
    """Get user by ID"""
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
    """Get all users"""
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

@router.put("/{user_id}/shortlist", response_model=UserResponse)
async def update_shortlist(user_id: str, update: ShortlistUpdate):
    """Update user's shortlist status"""
    try:
        user = await UserService.update_shortlist(user_id, update)
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
            detail=f"Failed to update shortlist: {str(e)}"
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