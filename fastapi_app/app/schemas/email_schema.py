from pydantic import BaseModel, EmailStr, Field
from typing import List,Optional
from datetime import datetime
from ..utils.enums import EmailStatus

class EmailBase(BaseModel):
    """Base email schema"""
    recipients: List[EmailStr]  
    message: str
    subject: str

class EmailCreate(EmailBase):
    """Schema for creating a new email"""
    email: str
    status: EmailStatus
    date_time: Optional[datetime] = None
    
    

class EmailUpdate(BaseModel):
    """Schema for updating email status"""
    status: EmailStatus

class EmailResponse(EmailBase):
    """Schema for email response"""
    id: str
    status: EmailStatus
    date_time: datetime
    message: str = Field(..., description="Email message content")
    subject: str = Field(..., description="Email subject")

    sent_count: int = Field(default=0, description="Number of emails successfully sent")
    failed_count: int = Field(default=0, description="Number of emails that failed to send")
    error_message: str = Field(default="", description="Error message if sending failed")

    class Config:
        from_attributes = True
        orm_mode = True
        