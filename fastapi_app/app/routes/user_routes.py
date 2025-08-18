from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas.user_schema import (
    UserCreate, UserResponse, ShortlistUpdate,
    GDUpdate, PIUpdate, TaskUpdate
)
from ..services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user"""
    return await UserService.create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get user by ID"""
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
async def get_users():
    """Get all users"""
    return await UserService.get_users()

@router.put("/{user_id}/shortlist", response_model=UserResponse)
async def update_shortlist(user_id: str, update: ShortlistUpdate):
    """Update user's shortlist status"""
    user = await UserService.update_shortlist(user_id, update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}/gd", response_model=UserResponse)
async def update_gd(user_id: str, update: GDUpdate):
    """Update user's GD status"""
    user = await UserService.update_gd(user_id, update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}/pi", response_model=UserResponse)
async def update_pi(user_id: str, update: PIUpdate):
    """Update user's PI status"""
    user = await UserService.update_pi(user_id, update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}/task", response_model=UserResponse)
async def update_task(user_id: str, update: TaskUpdate):
    """Update user's task status"""
    user = await UserService.update_task(user_id, update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
