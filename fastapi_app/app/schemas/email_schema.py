from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime
from ..utils.enums import EmailStatus

class EmailBase(BaseModel):
    """Base email schema"""
    recipients: List[EmailStr]  # Changed from 'email' to 'recipients' and use EmailStr for validation
    message: str
    subject: str

class EmailCreate(EmailBase):
    """Schema for creating a new email"""
    # Remove default values from create schema - let the service handle defaults
    pass

class EmailUpdate(BaseModel):
    """Schema for updating email status"""
    status: EmailStatus

class EmailResponse(EmailBase):
    """Schema for email response"""
    id: str
    status: EmailStatus
    date_time: datetime
    
    sent_count: int = Field(default=0, description="Number of emails successfully sent")
    failed_count: int = Field(default=0, description="Number of emails that failed to send")
    error_message: str = Field(default="", description="Error message if sending failed")

    class Config:
        from_attributes = True