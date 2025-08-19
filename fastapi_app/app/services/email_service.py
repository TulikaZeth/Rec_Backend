from typing import List, Optional
from datetime import datetime
from odmantic import ObjectId
from ..models.email import Email
from ..schemas.email_schema import EmailCreate, EmailUpdate, EmailResponse
from ..core.init_db import get_engine
from ..utils.enums import EmailStatus

class EmailService:
    """Service for handling email operations"""

    @staticmethod
    async def create_email(email: EmailCreate) -> EmailResponse:
        engine = get_engine()

        email_dict = email.dict()
        email_dict['sent_count'] = 0
        email_dict['failed_count'] = 0
        email_dict['error_message'] = ""

        if email_dict.get('date_time') is None:
            email_dict['status'] = EmailStatus.SCHEDULED
            email_dict['date_time'] = datetime.utcnow()
        else:
            email_dict['status'] = EmailStatus.PENDING

        new_email = Email(**email_dict)
        saved_email = await engine.save(new_email)

        return EmailService._to_response(saved_email)

    @staticmethod
    async def get_email(email_id: str) -> Optional[EmailResponse]:
        engine = get_engine()
        try:
            obj_id = ObjectId(email_id)
            email = await engine.find_one(Email, Email.id == obj_id)
            if email:
                return EmailService._to_response(email)
            return None
        except Exception as e:
            print(f"Error getting email: {e}")
            return None

    @staticmethod
    async def get_emails() -> List[EmailResponse]:
        engine = get_engine()
        emails = await engine.find(Email)
        return [EmailService._to_response(email) for email in emails]

    @staticmethod
    async def update_email_status(email_id: str, update: EmailUpdate) -> Optional[EmailResponse]:
        engine = get_engine()
        email_response = await EmailService.get_email(email_id)
        if not email_response:
            return None

        obj_id = ObjectId(email_id)
        raw_email = await engine.find_one(Email, Email.id == obj_id)

        # Case-insensitive enum conversion
        status_str = str(update.status).strip().lower()
        if status_str not in {s.value for s in EmailStatus}:
            raise ValueError(f"Invalid status value: {update.status}")
        raw_email.status = EmailStatus(status_str)

        updated_email = await engine.save(raw_email)
        return EmailService._to_response(updated_email)

    @staticmethod
    async def delete_email(email_id: str) -> bool:
        engine = get_engine()
        email = await EmailService.get_email(email_id)
        if not email:
            return False

        obj_id = ObjectId(email_id)
        raw_email = await engine.find_one(Email, Email.id == obj_id)
        await engine.delete(raw_email)
        return True

    @staticmethod
    async def get_emails_by_status(status: str) -> List[EmailResponse]:
        """Case-insensitive status filtering"""
        engine = get_engine()
        status_str = status.strip().lower()
        if status_str not in {s.value for s in EmailStatus}:
            return []
        emails = await engine.find(Email, Email.status == EmailStatus(status_str))
        return [EmailService._to_response(email) for email in emails]

    @staticmethod
    async def mark_email_sent(email_id: str, sent_count: int = 0, failed_count: int = 0, error_message: str = "") -> Optional[EmailResponse]:
        engine = get_engine()
        email_response = await EmailService.get_email(email_id)
        if not email_response:
            return None

        obj_id = ObjectId(email_id)
        raw_email = await engine.find_one(Email, Email.id == obj_id)

        raw_email.status = EmailStatus.SENT if failed_count == 0 else EmailStatus.FAILED
        raw_email.sent_count = sent_count
        raw_email.failed_count = failed_count
        raw_email.error_message = error_message

        updated_email = await engine.save(raw_email)
        return EmailService._to_response(updated_email)

    @staticmethod
    def _to_response(email: Email) -> EmailResponse:
        return EmailResponse(
            id=str(email.id),
            recipients=email.recipients,
            message=email.message,
            subject=email.subject,
            status=email.status,
            date_time=email.date_time,
            sent_count=getattr(email, 'sent_count', 0),
            failed_count=getattr(email, 'failed_count', 0),
            error_message=getattr(email, 'error_message', "")
        )
