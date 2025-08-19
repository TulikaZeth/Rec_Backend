# ----------------- Imports -----------------
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from odmantic import Model, Field as OdmanticField

# ----------------- Pydantic Schemas -----------------

class DomainPreferenceSchema(BaseModel):
    """Schema for domain preferences"""
    name: str
    reason: str

class UserBase(BaseModel):
    """Base user schema"""
    name: str
    email: EmailStr
    phone: int
    linkedIn: Optional[str] = None
    domains: List[str] = Field(default_factory=list)

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
    remarks: List[dict] = Field(default_factory=list)

class TaskUpdate(BaseModel):
    """Schema for updating task status"""
    status: str
    tasks: List[dict] = Field(default_factory=list)

class UserResponse(UserBase):
    """Schema for user response"""
    id: str
    domain_pref_one: Dict[str, Any]
    domain_pref_two: Dict[str, Any]
    shortlisted: Dict[str, Any] = Field(default_factory=dict)
    gd: Dict[str, Any] = Field(default_factory=dict)
    pi: Dict[str, Any] = Field(default_factory=dict)
    task: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True

# ----------------- Odmantic Model -----------------

class User(Model):
    """Odmantic model for MongoDB"""
    name: str
    email: str
    phone: int
    linkedIn: Optional[str] = OdmanticField(default="")
    domains: List[str] = OdmanticField(default_factory=list)
    domain_pref_one: Dict[str, Any]
    domain_pref_two: Dict[str, Any]
    # FIX: Use empty dict as default instead of None
    shortlisted: Dict[str, Any] = OdmanticField(default_factory=dict)
    gd: Dict[str, Any] = OdmanticField(default_factory=dict)
    pi: Dict[str, Any] = OdmanticField(default_factory=dict)
    task: Dict[str, Any] = OdmanticField(default_factory=dict)

    class Config:
        # This is important for ODMantic models
        collection = "users"