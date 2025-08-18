from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas.email_schema import EmailCreate, EmailResponse, EmailUpdate
from ..services.email_service import EmailService

router = APIRouter(prefix="/emails", tags=["emails"])

@router.post("/", response_model=EmailResponse)
async def create_email(email: EmailCreate):
    """Create a new email"""
    return await EmailService.create_email(email)

@router.get("/{email_id}", response_model=EmailResponse)
async def get_email(email_id: str):
    """Get email by ID"""
    email = await EmailService.get_email(email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

@router.get("/", response_model=List[EmailResponse])
async def get_emails():
    """Get all emails"""
    return await EmailService.get_emails()

@router.put("/{email_id}/status", response_model=EmailResponse)
async def update_email_status(email_id: str, update: EmailUpdate):
    """Update email status"""
    email = await EmailService.update_email_status(email_id, update)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email
