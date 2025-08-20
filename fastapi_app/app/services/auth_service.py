from typing import Optional, Tuple
from datetime import datetime, timedelta
from ..models.user import User
from ..models.auth import OTP, RefreshToken, LoginRequest, OTPVerifyRequest, TokenResponse
from ..core.init_db import get_database
from ..utils.auth import AuthUtils
from ..services.recruitment_email_service import recruitment_email_service
from ..services.user_service import UserService
from odmantic import ObjectId

class AuthService:
    """Service for handling authentication operations"""
    
    @staticmethod
    async def login(login_request: LoginRequest) -> Tuple[bool, str]:
        """
        Login user by email and send OTP
        Returns: (success, message)
        """
        try:
            # Check if user exists
            user = await UserService.get_user_by_email(login_request.email)
            if not user:
                return False, "User not found"
            
            # Generate OTP
            otp = AuthUtils.generate_otp()
            expires_at = AuthUtils.get_otp_expiry()
            
            # Save OTP to database
            engine = get_database()
            
            # Delete any existing OTPs for this email
            await engine.remove(OTP, OTP.email == login_request.email)
            
            # Create new OTP record
            otp_record = OTP(
                email=login_request.email,
                otp=otp,
                expires_at=expires_at
            )
            await engine.save(otp_record)
            
            # Send OTP via EmailJS
            email_sent = await recruitment_email_service.send_login_otp(
                email=login_request.email,
                name=user.name,
                otp=otp
            )
            
            if email_sent:
                return True, "OTP sent successfully to your email"
            else:
                return False, "Failed to send OTP. Please try again."
                
        except Exception as e:
            print(f"Error in login: {e}")
            return False, "Login failed. Please try again."
    
    @staticmethod
    async def verify_otp(verify_request: OTPVerifyRequest) -> Tuple[bool, Optional[TokenResponse], str]:
        """
        Verify OTP and return tokens
        Returns: (success, token_response, message)
        """
        try:
            engine = get_database()
            
            # Find OTP record
            otp_record = await engine.find_one(
                OTP, 
                OTP.email == verify_request.email,
                OTP.is_used == False
            )
            
            if not otp_record:
                return False, None, "Invalid or expired OTP"
            
            # Check if OTP is expired
            if AuthUtils.is_otp_expired(otp_record.expires_at):
                return False, None, "OTP has expired"
            
            # Check attempts
            if otp_record.attempts >= 3:
                return False, None, "Too many invalid attempts. Please request a new OTP."
            
            # Verify OTP
            if otp_record.otp != verify_request.otp:
                # Increment attempts
                otp_record.attempts += 1
                await engine.save(otp_record)
                return False, None, f"Invalid OTP. {3 - otp_record.attempts} attempts remaining."
            
            # OTP is valid, mark as used
            otp_record.is_used = True
            await engine.save(otp_record)
            
            # Get user details
            user = await UserService.get_user_by_email(verify_request.email)
            if not user:
                return False, None, "User not found"
            
            # Generate tokens
            user_data = {
                "user_id": str(user.id),
                "email": user.email,
                "name": user.name
            }
            
            access_token = AuthUtils.create_access_token(user_data)
            refresh_token = AuthUtils.create_refresh_token(user_data)
            
            # Save refresh token to database
            refresh_token_record = RefreshToken(
                user_id=str(user.id),
                token=refresh_token,
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
            await engine.save(refresh_token_record)
            
            token_response = TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token
            )
            
            return True, token_response, "Login successful"
            
        except Exception as e:
            print(f"Error in verify_otp: {e}")
            return False, None, "OTP verification failed"
    
    @staticmethod
    async def refresh_access_token(refresh_token: str) -> Tuple[bool, Optional[str], str]:
        """
        Refresh access token using refresh token
        Returns: (success, new_access_token, message)
        """
        try:
            # Verify refresh token
            payload = AuthUtils.verify_token(refresh_token)
            if not payload or payload.get("type") != "refresh":
                return False, None, "Invalid refresh token"
            
            engine = get_database()
            
            # Check if refresh token exists in database and is not revoked
            token_record = await engine.find_one(
                RefreshToken,
                RefreshToken.token == refresh_token,
                RefreshToken.is_revoked == False
            )
            
            if not token_record:
                return False, None, "Refresh token not found or revoked"
            
            # Check if refresh token is expired
            if datetime.utcnow() > token_record.expires_at:
                return False, None, "Refresh token has expired"
            
            # Generate new access token
            user_data = {
                "user_id": payload["user_id"],
                "email": payload["email"],
                "name": payload["name"]
            }
            
            new_access_token = AuthUtils.create_access_token(user_data)
            
            return True, new_access_token, "Token refreshed successfully"
            
        except Exception as e:
            print(f"Error in refresh_access_token: {e}")
            return False, None, "Token refresh failed"
    
    @staticmethod
    async def revoke_refresh_token(refresh_token: str) -> bool:
        """Revoke a refresh token"""
        try:
            engine = get_database()
            
            token_record = await engine.find_one(
                RefreshToken,
                RefreshToken.token == refresh_token
            )
            
            if token_record:
                token_record.is_revoked = True
                await engine.save(token_record)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error in revoke_refresh_token: {e}")
            return False
