from typing import List, Optional
from odmantic import Model
from datetime import datetime
from ..utils.enums import EmailStatus

class Email(Model):
    """Email model for tracking communication"""
    email: List[str]  # List of recipient email addresses
    status: EmailStatus
    message: str
    subject: str
    date_time: datetime
    
    class Config:
        collection = "emails"
