from contextlib import asynccontextmanager
from fastapi import Depends
from auth.db.models import SettingsSession,SettingsSMTP,SettingsSSO
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependencies import SessionLocal, get_db
from sqlalchemy import select
# from auth.main import sso_settings,smtp_settings,session_settings


# @asynccontextmanager
# async def lifespan():
#     # Load settings at startup
#     global sso_settings, session_settings, smtp_settings
    
#     async with SessionLocal() as db:
#         try:
#             # Fetch SSO settings
#             sso_result = await db.execute(select(SettingsSSO))
#             sso_settings = sso_result.scalars().first()

#             # Fetch Session settings
#             session_result = await db.execute(select(SettingsSession))
#             session_settings = session_result.scalars().first()

#             # Fetch SMTP settings
#             smtp_result = await db.execute(select(SettingsSMTP))
#             smtp_settings = smtp_result.scalars().first()

#             print("Settings loaded successfully")
#             print(f"SSO Settings: {sso_settings}")
#             print(f"Session Settings: {session_settings}")
#             print(f"SMTP Settings: {smtp_settings}")

#         except Exception as e:
#             print(f"Error loading settings: {e}")
#             # You might want to raise an exception here if the app can't start without these settings

# with lifespan as get_creds:
#     get_creds()

# SECRET_KEY = session_settings.secret_key
# ALGORITHM = session_settings.algorithm
# ACCESS_TOKEN_EXPIRE_MINUTES = session_settings.acs_tkn_expire
# RESET_TOKEN_EXPIRE_MINUTES = session_settings.rst_tkn_expire
# OTP_EXPIRE_MINUTES = session_settings.otp_expire
# SIGNUP_URL_SSO = sso_settings.signup_url#"https://dev-api-app.tawazun.io/register/"
# LOGIN_URL_SSO = sso_settings.login_url#"https://dev-api-app.tawazun.io/auth/login"
# FORGOT_PASSWORD_URL_SSO = sso_settings.forgot_pwd_url#"https://dev-api-app.tawazun.io/auth/forgot-password"
# RESET_PASSWORD_URL_SSO = sso_settings.reset_pwd_url#"https://dev-api-app.tawazun.io/auth/reset-password"
# CHAGE_PASSWORD_URL_SSO = sso_settings.change_pwd_url#"https://dev-api-app.tawazun.io/auth/change-password"
# API_KEY = sso_settings.api_key#"API_KEY_b17c2e02e015b3dcfb8e130bd092872e133c43de"
# SMTP_SERVER= smtp_settings.server #"email-smtp.eu-central-1.amazonaws.com"
# serverusername= smtp_settings.server_username #"AKIARZL4X6FTMDTXXRYI"
# serverpassword= smtp_settings.server_password #"BJXnGzShMJZ+xZFfefaaQlcBBHNoZ+IhrOrr/YRBf8O3"
    
