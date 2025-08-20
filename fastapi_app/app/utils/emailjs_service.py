import requests
import os
from typing import Dict, Any, Optional
from loguru import logger

class EmailJSService:
    """
    EmailJS service for sending different types of emails
    Supports multiple templates for different purposes
    """
    
    def __init__(self):
        # EmailJS configuration from environment variables
        self.service_id = "service_l5a7995"
        self.public_key = "YD4XjAKhdoB8MRxWk"
        self.private_key = "92bW7150EeXJ42REAnDNa"
        self.api_url = "https://api.emailjs.com/api/v1.0/email/send"
        
        # Template IDs for different email types
        self.templates = {
            "otp": "template_irawkt8",
            "welcome": os.getenv("EMAILJS_WELCOME_TEMPLATE_ID", "template_welcome"),
            "notification": os.getenv("EMAILJS_NOTIFICATION_TEMPLATE_ID", "template_notification"),
            "reminder": os.getenv("EMAILJS_REMINDER_TEMPLATE_ID", "template_reminder"),
            "status_update": os.getenv("EMAILJS_STATUS_UPDATE_TEMPLATE_ID", "template_status")
        }
    
    async def _send_email(self, template_id: str, template_params: Dict[str, Any]) -> bool:
        """
        Private method to send email via EmailJS
        """
        try:
            payload = {
                "service_id": self.service_id,
                "template_id": template_id,
                "user_id": self.public_key,
                "template_params": template_params
            }
            
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(self.api_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                logger.info(f"EmailJS: Email sent successfully to {template_params.get('to_email', 'unknown')}")
                return True
            elif response.status_code == 403:
                logger.warning("EmailJS: API calls are disabled for non-browser applications (403). Consider upgrading your EmailJS plan.")
                return False
            else:
                logger.error(f"EmailJS: Failed to send email. Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"EmailJS: Error sending email: {str(e)}")
            return False
    
    async def send_otp_email(self, to_email: str, to_name: str, otp: str) -> bool:
        """
        Send OTP email for login verification
        """
        template_params = {
            "to_email": to_email,
            "to_name": to_name,
            "otp": otp,
            "from_name": "Recruitment Portal",
            "subject": "Your Login OTP",
            "reply_to": "noreply@recruitmentportal.com",
            "company_name": "Recruitment Portal",
            "expiry_time": "5 minutes"
        }
        
        return await self._send_email(self.templates["otp"], template_params)
    
    async def send_welcome_email(self, to_email: str, to_name: str) -> bool:
        """
        Send welcome email for new users
        """
        template_params = {
            "to_email": to_email,
            "to_name": to_name,
            "from_name": "Recruitment Portal Team",
            "subject": "Welcome to Recruitment Portal",
            "reply_to": "support@recruitmentportal.com",
            "company_name": "Recruitment Portal",
            "dashboard_link": "https://your-portal.com/dashboard"
        }
        
        return await self._send_email(self.templates["welcome"], template_params)
    
    async def send_status_update_email(
        self, 
        to_email: str, 
        to_name: str, 
        status_type: str, 
        status: str, 
        next_steps: str = ""
    ) -> bool:
        """
        Send status update emails (shortlist, GD, PI, etc.)
        """
        template_params = {
            "to_email": to_email,
            "to_name": to_name,
            "status_type": status_type,  # "Shortlist", "Group Discussion", "Personal Interview"
            "status": status,  # "Selected", "Rejected", "Pending"
            "next_steps": next_steps,
            "from_name": "Recruitment Portal Team",
            "subject": f"Update on your {status_type} Status",
            "reply_to": "hr@recruitmentportal.com",
            "company_name": "Recruitment Portal",
            "contact_email": "hr@recruitmentportal.com"
        }
        
        return await self._send_email(self.templates["status_update"], template_params)
    
    async def send_reminder_email(
        self, 
        to_email: str, 
        to_name: str, 
        reminder_type: str, 
        event_date: str, 
        event_time: str,
        location: str = ""
    ) -> bool:
        """
        Send reminder emails for interviews, GD, etc.
        """
        template_params = {
            "to_email": to_email,
            "to_name": to_name,
            "reminder_type": reminder_type,  # "Interview", "Group Discussion", "Task Submission"
            "event_date": event_date,
            "event_time": event_time,
            "location": location,
            "from_name": "Recruitment Portal Team",
            "subject": f"Reminder: {reminder_type} Scheduled",
            "reply_to": "hr@recruitmentportal.com",
            "company_name": "Recruitment Portal",
            "contact_phone": "+1-234-567-8900"
        }
        
        return await self._send_email(self.templates["reminder"], template_params)
    
    async def send_notification_email(
        self, 
        to_email: str, 
        to_name: str, 
        notification_type: str, 
        message: str,
        action_required: bool = False,
        action_link: str = ""
    ) -> bool:
        """
        Send general notification emails
        """
        template_params = {
            "to_email": to_email,
            "to_name": to_name,
            "notification_type": notification_type,
            "message": message,
            "action_required": "Yes" if action_required else "No",
            "action_link": action_link,
            "from_name": "Recruitment Portal Team",
            "subject": f"Notification: {notification_type}",
            "reply_to": "notifications@recruitmentportal.com",
            "company_name": "Recruitment Portal"
        }
        
        return await self._send_email(self.templates["notification"], template_params)
    
    async def send_custom_email(
        self, 
        template_type: str, 
        template_params: Dict[str, Any]
    ) -> bool:
        """
        Send custom email with specified template and parameters
        """
        if template_type not in self.templates:
            logger.error(f"Template type '{template_type}' not found")
            return False
        
        return await self._send_email(self.templates[template_type], template_params)

# Create a singleton instance
emailjs_service = EmailJSService()
