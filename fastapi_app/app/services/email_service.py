from typing import List, Optional
from datetime import datetime
from ..models.email import Email  # Your ODMantic Email model
from ..schemas.email_schema import EmailCreate, EmailUpdate
from ..core.init_db import get_engine  # Your database engine
from ..utils.enums import EmailStatus
from odmantic import ObjectId

class EmailService:
    """Service for handling email operations"""
    
    @staticmethod
    async def create_email(email: EmailCreate) -> Email:
        """Create a new email in the database"""
        engine = get_engine()
        
        # Convert Pydantic model to dict - use .dict() not .model_dump()
        email_dict = email.dict()
        print("Received email data:", email_dict)
        
        # Set defaults in service layer
        
        
        email_dict['sent_count'] = 0
        email_dict['failed_count'] = 0
        email_dict['error_message'] = ""

        if email.dict().get('date_time') is None:
            email_dict['status'] = EmailStatus.SCHEDULED
            email_dict['date_time'] = datetime.now()
        else:
            email_dict['status'] = EmailStatus.PENDING

        
        # Create ODMantic email instance
        new_email = Email(**email_dict)
        
        # Save using ODMantic engine
        saved_email = await engine.save(new_email)
        
        return saved_email
        
    @staticmethod
    async def get_email(email_id: str) -> Optional[Email]:
        """Get email by ID"""
        engine = get_engine()
        try:
            obj_id = ObjectId(email_id)
            email = await engine.find_one(Email, Email.id == obj_id)
            return email
        except Exception as e:
            print(f"Error getting email: {e}")
            return None
    
    @staticmethod
    async def get_emails() -> List[Email]:
        """Get all emails"""
        engine = get_engine()
        # Use ODMantic's find method, not raw PyMongo
        emails = await engine.find(Email)
        return list(emails)
    
    @staticmethod
    async def update_email_status(email_id: str, update: EmailUpdate) -> Optional[Email]:
        """Update email status"""
        engine = get_engine()
        email = await EmailService.get_email(email_id)
        if not email:
            return None
            
        # Update the status
        email.status = update.status
        
        # Save the updated email
        updated_email = await engine.save(email)
        return updated_email
    
    @staticmethod
    async def delete_email(email_id: str) -> bool:
        """Delete email by ID"""
        engine = get_engine()
        email = await EmailService.get_email(email_id)
        if not email:
            return False
            
        await engine.delete(email)
        return True
    
    @staticmethod
    async def get_emails_by_status(status: EmailStatus) -> List[Email]:
        """Get emails by status"""
        engine = get_engine()
        emails = await engine.find(Email, Email.status == status)
        return list(emails)
    
    @staticmethod
    async def mark_email_sent(email_id: str, sent_count: int = 0, failed_count: int = 0, error_message: str = "") -> Optional[Email]:
        """Mark email as sent and update counts"""
        engine = get_engine()
        email = await EmailService.get_email(email_id)
        if not email:
            return None
            
        # Update email status and counts
        email.status = EmailStatus.SENT if failed_count == 0 else EmailStatus.FAILED
        email.sent_count = sent_count
        email.failed_count = failed_count
        email.error_message = error_message
        
        # Save the updated email
        updated_email = await engine.save(email)
        return updated_email