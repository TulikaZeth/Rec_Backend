from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from ..utils.enums import EmailStatus

class EmailBase(BaseModel):
    """Base email schema"""
    email: List[str]
    message: str
    subject: str

class EmailCreate(EmailBase):
    """Schema for creating a new email"""
    status: EmailStatus = EmailStatus.PENDING
    date_time: datetime = datetime.now()

class EmailUpdate(BaseModel):
    """Schema for updating email status"""
    status: EmailStatus

class EmailResponse(EmailBase):
    """Schema for email response"""
    id: str
    status: EmailStatus
    date_time: datetime

    class Config:
        from_attributes = True
