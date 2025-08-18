from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class DomainPreferenceSchema(BaseModel):
    """Schema for domain preferences"""
    name: str
    reason: str

class UserBase(BaseModel):
    """Base user schema"""
    name: str
    email: EmailStr
    phone: int
    fb_id: str
    linkedIn: str
    domains: List[str]

class UserCreate(UserBase):
    """Schema for creating a new user"""
    domain_pref_one: DomainPreferenceSchema
    domain_pref_two: DomainPreferenceSchema

class ShortlistUpdate(BaseModel):
    """Schema for updating shortlist status"""
    status: str
    datetime: datetime
    
class GDUpdate(BaseModel):
    """Schema for updating GD status"""
    status: str
    datetime: datetime
    remarks: str

class PIUpdate(BaseModel):
    """Schema for updating PI status"""
    status: str
    datetime: datetime
    remarks: List[dict]  # List of domain and reason pairs

class TaskUpdate(BaseModel):
    """Schema for updating task status"""
    status: str
    tasks: List[dict]  # List of domain and submission pairs

class UserResponse(UserBase):
    """Schema for user response"""
    id: str
    shortlisted: List[dict]
    gd: Optional[dict]
    pi: Optional[dict]
    task: Optional[dict]

    class Config:
        from_attributes = True
