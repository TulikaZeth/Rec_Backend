import os
import requests
import asyncio
from typing import Dict, Any
from loguru import logger

class ResendService:
    """
    Resend service for sending different types of emails
    Supports multiple templates for different purposes
    """

    def __init__(self):
        self.api_key = "re_BS2Ln4oj_4p3dVtSWZMCXNNL3FSNKdCgG"
        self.api_url = "https://api.resend.com/emails"

    async def _send_email(self, to_email: str, subject: str, html: str, from_email: str = None) -> bool:
        """
        Private method to send email via Resend
        """
        try:
            payload = {
                "from": "onboarding@resend.dev",
                "to": "delivered@resend.dev",
                "subject": subject,
                "html": html
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.post(self.api_url, json=payload, headers=headers))

            if response.status_code == 200:
                logger.info(f"Resend: Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Resend: Failed to send email. Status: {response.status_code}, Response: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Resend: Error sending email: {str(e)}")
            return False

    # === Email methods ===
    async def send_otp_email(self, to_email: str, to_name: str, otp: str) -> bool:
        subject = "Your Login OTP"
        html = f"""
        <h2>Hello {to_name},</h2>
        <p>Your OTP for login is: <b>{otp}</b></p>
        <p>This OTP will expire in <b>5 minutes</b>.</p>
        <p>Best regards,<br>Recruitment Portal</p>
        """
        return await self._send_email(to_email, subject, html)

    async def send_welcome_email(self, to_email: str, to_name: str) -> bool:
        subject = "Welcome to Recruitment Portal"
        html = f"""
        <h2>Welcome {to_name}!</h2>
        <p>We're excited to have you onboard our recruitment portal.</p>
        <p>You can now access your dashboard and track your application status.</p>
        <p>Best regards,<br>Recruitment Team</p>
        """
        return await self._send_email(to_email, subject, html)

    async def send_status_update_email(self, to_email: str, to_name: str, status_type: str, status: str, next_steps: str = "") -> bool:
        subject = f"Application Status Update - {status_type}"
        html = f"""
        <h2>Hello {to_name},</h2>
        <p>Your application status has been updated:</p>
        <p><b>Status:</b> {status}</p>
        {f"<p><b>Next Steps:</b> {next_steps}</p>" if next_steps else ""}
        <p>Best regards,<br>Recruitment Team</p>
        """
        return await self._send_email(to_email, subject, html)

    async def send_reminder_email(self, to_email: str, to_name: str, reminder_type: str, event_date: str, event_time: str, location: str = "") -> bool:
        subject = f"Reminder: {reminder_type}"
        html = f"""
        <h2>Hello {to_name},</h2>
        <p>This is a reminder for your upcoming {reminder_type}:</p>
        <p><b>Date:</b> {event_date}</p>
        <p><b>Time:</b> {event_time}</p>
        {f"<p><b>Location:</b> {location}</p>" if location else ""}
        <p>Please be on time. Good luck!</p>
        <p>Best regards,<br>Recruitment Team</p>
        """
        return await self._send_email(to_email, subject, html)

    async def send_notification_email(self, to_email: str, to_name: str, notification_type: str, message: str, action_required: bool = False, action_link: str = "") -> bool:
        subject = f"Notification: {notification_type}"
        html = f"""
        <h2>Hello {to_name},</h2>
        <p>{message}</p>
        {f'<p><a href="{action_link}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Take Action</a></p>' if action_required and action_link else ""}
        <p>Best regards,<br>Recruitment Team</p>
        """
        return await self._send_email(to_email, subject, html)

    async def send_custom_email(self, template_type: str, template_data: Dict[str, Any]) -> bool:
        """Send a custom email based on template type and data"""
        to_email = template_data.get("email")
        to_name = template_data.get("name", "Candidate")
        
        if not to_email:
            logger.error("Email address is required for custom email")
            return False
            
        # You can extend this with more template types
        if template_type == "custom":
            subject = template_data.get("subject", "Custom Notification")
            message = template_data.get("message", "")
            html = f"""
            <h2>Hello {to_name},</h2>
            <p>{message}</p>
            <p>Best regards,<br>Recruitment Team</p>
            """
            return await self._send_email(to_email, subject, html)
        
        logger.error(f"Unknown template type: {template_type}")
        return False

# Create instance
resend_service = ResendService()
