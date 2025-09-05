# ----------------- Imports -----------------
from pydantic import BaseModel, EmailStr, Field, validator, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from odmantic import Model, Field as OdmanticField
from ..utils.enums import status, TaskStatus, DomainEnum

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

class TaskItem(BaseModel):
    """Schema for individual task item"""
    domain: str = Field(..., description="Domain for the task")
    url: HttpUrl = Field(..., description="URL for the task submission")
    
    @validator('domain')
    def validate_domain(cls, v):
        """Validate that domain is one of the allowed DomainEnum values"""
        if v not in [d.value for d in DomainEnum]:
            raise ValueError(f'Domain must be one of: {[d.value for d in DomainEnum]}')
        return v

class TaskUpdate(BaseModel):
    """Schema for updating task status"""
    status: str
    tasks: List[TaskItem] = Field(default_factory=list, description="List of tasks with domain and URL")
    
    @validator('status')
    def validate_status(cls, v):
        """Validate that status is one of the allowed TaskStatus values"""
        if v not in [ts.value for ts in TaskStatus]:
            raise ValueError(f'Status must be one of: {[ts.value for ts in TaskStatus]}')
        return v

class ShortlistRequest(BaseModel):
    """Schema for shortlisting users"""
    emails: List[EmailStr] = Field(..., description="List of user emails to shortlist/unshortlist")
    
    class Config:
        schema_extra = {
            "example": {
                "emails": ["user1@example.com", "user2@example.com"]
            }
        }

class TaskStatusUpdate(BaseModel):
    """Schema for updating specific task status and URL"""
    domain: str = Field(..., description="Domain of the task to update")
    url: HttpUrl = Field(..., description="URL for the completed task")
    
    @validator('domain')
    def validate_domain(cls, v):
        """Validate that domain is one of the allowed DomainEnum values"""
        if v not in [d.value for d in DomainEnum]:
            raise ValueError(f'Domain must be one of: {[d.value for d in DomainEnum]}')
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
    shortlisted: bool = Field(default=False)

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
    shortlisted: bool = OdmanticField(default=False)

    class Config:
        # This is important for ODMantic models
        collection = "users"