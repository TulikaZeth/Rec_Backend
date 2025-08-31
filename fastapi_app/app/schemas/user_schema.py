# ----------------- Imports -----------------
from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from odmantic import Model, Field as OdmanticField
from ..utils.enums import status, TaskStatus

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
    year: int
    lib_id: str
    branch: str
    why_ecell: str
    linkedIn: Optional[str] = None
    domains: List[str] = Field(default_factory=list)
    groupNumber: Optional[int] = None

class UserCreate(UserBase):
    """Schema for creating a new user"""
    domain_pref_one: DomainPreferenceSchema
    domain_pref_two: DomainPreferenceSchema

class screeningUpdate(BaseModel):
    """Schema for updating screening status"""
    status: str
    datetime: datetime
    remarks: str
    domains: Optional[List[str]] = Field(default=None, description="List of domains to add to user")
    
    @validator('status')
    def validate_status(cls, v):
        """Validate that status is one of the allowed values"""
        if v not in [s.value for s in status]:
            raise ValueError(f'Status must be one of: {[s.value for s in status]}')
        return v
    
    @validator('domains')
    def validate_domains(cls, v):
        """Validate domains list"""
        if v is not None:
            # Check for duplicates within the provided list
            if len(v) != len(set(v)):
                raise ValueError('Duplicate domains are not allowed in the request')
            # Check for empty strings
            if any(not domain.strip() for domain in v):
                raise ValueError('Domain names cannot be empty')
        return v

class GDUpdate(BaseModel):
    """Schema for updating GD status"""
    status: str
    datetime: datetime
    remarks: str
    
    @validator('status')
    def validate_status(cls, v):
        """Validate that status is one of the allowed values"""
        if v not in [s.value for s in status]:
            raise ValueError(f'Status must be one of: {[s.value for s in status]}')
        return v

class PIUpdate(BaseModel):
    """Schema for updating PI status"""
    status: str
    datetime: datetime
    remarks: str
    
    @validator('status')
    def validate_status(cls, v):
        """Validate that status is one of the allowed values"""
        if v not in [s.value for s in status]:
            raise ValueError(f'Status must be one of: {[s.value for s in status]}')
        return v

class TaskUpdate(BaseModel):
    """Schema for updating task status"""
    status: str
    tasks: List[dict] = Field(default_factory=list)
    
    @validator('status')
    def validate_status(cls, v):
        """Validate that status is one of the allowed TaskStatus values"""
        if v not in [ts.value for ts in TaskStatus]:
            raise ValueError(f'Status must be one of: {[ts.value for ts in TaskStatus]}')
        return v

class UserResponse(UserBase):
    """Schema for user response"""
    id: str
    domain_pref_one: Dict[str, Any]
    domain_pref_two: Dict[str, Any]
    screening: Dict[str, Any] = Field(default_factory=dict)
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
    year: int
    lib_id: str
    branch: str
    why_ecell: str
    linkedIn: Optional[str] = OdmanticField(default="")
    domains: List[str] = OdmanticField(default_factory=list)
    domain_pref_one: Dict[str, Any]
    domain_pref_two: Dict[str, Any]
    groupNumber: Optional[int] = OdmanticField(default=None)
    # FIX: Use empty dict as default instead of None
    screening: Dict[str, Any] = OdmanticField(default_factory=dict)
    gd: Dict[str, Any] = OdmanticField(default_factory=dict)
    pi: Dict[str, Any] = OdmanticField(default_factory=dict)
    task: Dict[str, Any] = OdmanticField(default_factory=dict)

    class Config:
        # This is important for ODMantic models
        collection = "users"