from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas.email_schema import EmailCreate, EmailResponse, EmailUpdate
from ..services.recruitment_email_service import recruitment_email_service

router = APIRouter(prefix="/emails", tags=["emails"])

@router.post("/send-otp", response_model=dict)
async def send_otp_email(email: str, otp: str):
    """Send OTP email to user"""
    try:
        result = await recruitment_email_service.send_login_otp(email, otp)
        if result["success"]:
            return {"message": "OTP sent successfully", "email": email}
        else:
            raise HTTPException(status_code=500, detail="Failed to send OTP")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-welcome", response_model=dict)
async def send_welcome_email(email: str, name: str):
    """Send welcome email to new user"""
    try:
        result = await recruitment_email_service.send_welcome_email(email, name)
        if result["success"]:
            return {"message": "Welcome email sent successfully", "email": email}
        else:
            raise HTTPException(status_code=500, detail="Failed to send welcome email")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-interview-reminder", response_model=dict)
async def send_interview_reminder(email: str, candidate_name: str, interview_date: str, interview_time: str, position: str):
    """Send interview reminder email"""
    try:
        result = await recruitment_email_service.send_interview_reminder(
            email, candidate_name, interview_date, interview_time, position
        )
        if result["success"]:
            return {"message": "Interview reminder sent successfully", "email": email}
        else:
            raise HTTPException(status_code=500, detail="Failed to send interview reminder")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
