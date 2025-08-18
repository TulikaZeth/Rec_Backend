from typing import List, Optional
from ..models.email import Email
from ..core.init_db import get_database
from ..schemas.email_schema import EmailCreate, EmailUpdate

class EmailService:
    """Service for handling email operations"""
    
    @staticmethod
    async def create_email(email: EmailCreate) -> Email:
        """Create a new email"""
        db = get_database()
        email_dict = email.model_dump()
        new_email = Email(**email_dict)
        await db.emails.insert_one(new_email.model_dump())
        return new_email
    
    @staticmethod
    async def get_email(email_id: str) -> Optional[Email]:
        """Get email by ID"""
        db = get_database()
        email_data = await db.emails.find_one({"_id": email_id})
        return Email(**email_data) if email_data else None
    
    @staticmethod
    async def get_emails() -> List[Email]:
        """Get all emails"""
        db = get_database()
        emails = []
        cursor = db.emails.find({})
        async for email_data in cursor:
            emails.append(Email(**email_data))
        return emails
    
    @staticmethod
    async def update_email_status(email_id: str, update: EmailUpdate) -> Optional[Email]:
        """Update email status"""
        db = get_database()
        update_dict = update.model_dump()
        await db.emails.update_one(
            {"_id": email_id},
            {"$set": {"status": update_dict["status"]}}
        )
        return await EmailService.get_email(email_id)
