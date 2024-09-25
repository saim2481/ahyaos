from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import select
from auth.dependencies import SessionLocal,engine, get_db
from auth.db.models import SettingsSession,SettingsSMTP,SettingsSSO,SettingsStripe
from dotenv import load_dotenv, set_key
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from .limiter import limiter
from auth.api.v1.routers import auth_sso_otp,auth_local,auth_sso,profile_verfication,stripe
import os
import traceback





# @asynccontextmanager
# async def lifespan(app: FastAPI):

#     async with get_db() as db:
#         sso_cred_query = db.execute(select(SettingsSSO))
#         sso_result = sso_cred_query.scalars().first()
#         session_cred_query = db.execute(select(SettingsSession))
#         session_result = session_cred_query.scalars().first()
#         smtp_cred_query = db.execute(select(SettingsSMTP))
#         smtp_result = smtp_cred_query.scalars().first()
#         print(sso_result)
#     yield


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load settings at startup
    # global sso_settings, session_settings, smtp_settings
    
    async with SessionLocal() as db:
        try:
            # Fetch SSO settings
            sso_result = await db.execute(select(SettingsSSO))
            sso_settings = sso_result.scalars().first()

            # Fetch Session settings
            session_result = await db.execute(select(SettingsSession))
            session_settings = session_result.scalars().first()

            # Fetch SMTP settings
            smtp_result = await db.execute(select(SettingsSMTP))
            smtp_settings = smtp_result.scalars().first()

            # Fetch Stripe settings
            stripe_result = await db.execute(select(SettingsStripe))
            stripe_settings = stripe_result.scalars().first()

            print("Settings loaded successfully")
            print(f"SSO Settings: {sso_settings}")
            print(f"Session Settings: {session_settings}")
            print(f"SMTP Settings: {smtp_settings}")
            print(f"Stripe Settings: {stripe_settings}")
            set_key('.env','SECRET_KEY',session_settings.secret_key)
            os.environ['SECRET_KEY'] = session_settings.secret_key
            set_key('.env','ALGORITHM',session_settings.algorithm)
            os.environ['ALGORITHM'] = session_settings.algorithm
            set_key('.env','ACCESS_TOKEN_EXPIRE_MINUTES',str(session_settings.acs_tkn_expire))
            os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'] = str(session_settings.acs_tkn_expire)
            set_key('.env','RESET_TOKEN_EXPIRE_MINUTES', str(session_settings.rst_tkn_expire))
            os.environ['RESET_TOKEN_EXPIRE_MINUTES'] = str(session_settings.rst_tkn_expire)
            set_key('.env','OTP_EXPIRE_MINUTES',str(session_settings.otp_expire))
            os.environ['OTP_EXPIRE_MINUTES'] = str(session_settings.otp_expire)
            set_key('.env','SIGNUP_URL_SSO',sso_settings.signup_url)#"https://dev-api-app.tawazun.io/register/"
            os.environ['SIGNUP_URL_SSO'] = sso_settings.signup_url
            set_key('.env','LOGIN_URL_SSO',sso_settings.login_url)#"https://dev-api-app.tawazun.io/auth/login"
            os.environ['LOGIN_URL_SSO'] = sso_settings.login_url
            set_key('.env','FORGOT_PASSWORD_URL_SSO',sso_settings.forgot_pwd_url)#"https://dev-api-app.tawazun.io/auth/forgot-password"
            os.environ['FORGOT_PASSWORD_URL_SSO'] = sso_settings.forgot_pwd_url
            set_key('.env','RESET_PASSWORD_URL_SSO',sso_settings.reset_pwd_url)#"https://dev-api-app.tawazun.io/auth/reset-password"
            os.environ['RESET_PASSWORD_URL_SSO'] = sso_settings.reset_pwd_url
            set_key('.env','CHAGE_PASSWORD_URL_SSO',sso_settings.change_pwd_url)#"https://dev-api-app.tawazun.io/auth/change-password"
            os.environ['CHAGE_PASSWORD_URL_SSO'] = sso_settings.change_pwd_url
            set_key('.env','API_KEY', sso_settings.api_key)#"API_KEY_b17c2e02e015b3dcfb8e130bd092872e133c43de"
            os.environ['API_KEY'] = sso_settings.api_key
            set_key('.env','SMTP_SERVER',smtp_settings.server) #"email-smtp.eu-central-1.amazonaws.com"
            os.environ['SMTP_SERVER'] = smtp_settings.server
            set_key('.env','serverusername', smtp_settings.server_username) #"AKIARZL4X6FTMDTXXRYI"
            os.environ['serverusername'] = smtp_settings.server_username
            set_key('.env','serverpassword',smtp_settings.server_password) #"BJXnGzShMJZ+xZFfefaaQlcBBHNoZ+IhrOrr/YRBf8O3"
            os.environ['serverpassword'] = smtp_settings.server_password
            set_key('.env','otp_max_count',str(session_settings.otp_max_count)) #"BJXnGzShMJZ+xZFfefaaQlcBBHNoZ+IhrOrr/YRBf8O3"
            os.environ['otp_max_count'] = str(session_settings.otp_max_count)
            set_key('.env','otp_resend_time',str(session_settings.otp_resend_time)) #"BJXnGzShMJZ+xZFfefaaQlcBBHNoZ+IhrOrr/YRBf8O3"
            os.environ['otp_resend_time'] = str(session_settings.otp_resend_time)
            set_key('.env','otp_resend_count_reset_time',str(session_settings.otp_resend_count_reset_time)) #"BJXnGzShMJZ+xZFfefaaQlcBBHNoZ+IhrOrr/YRBf8O3"
            os.environ['otp_resend_count_reset_time'] = str(session_settings.otp_resend_count_reset_time)

            set_key('.env','STRIPE_API',stripe_settings.api_key) #"sk_test_51POKYm2MPf6Tg7eRlc19aKXQHKkYMABseM3ZovvX7WAEloOby8uBPnjw7v97gKtxqqMdjGaVigBwD3BmtSkownCP00bpdPnLtN"
            os.environ['STRIPE_API'] = stripe_settings.api_key
            set_key('.env','stripe_version', stripe_settings.version) #"2024-06-20"
            os.environ['stripe_version'] = stripe_settings.version
            set_key('.env','success_url', stripe_settings.success_url) #http://yoursite.com/order/success
            os.environ['success_url'] = stripe_settings.success_url #http://yoursite.com/order/cancel
            set_key('.env','cancel_url', stripe_settings.cancel_url) #http://yoursite.com/order/success
            os.environ['cancel_url'] = stripe_settings.cancel_url #http://yoursite.com/order/cancel

    

        except Exception as e:
            traceback.print_exc()
            print(f"Error loading settings: {e}")
            # You might want to raise an exception here if the app can't start without these settings

    yield

    # Clean up resources at shutdown
    await engine.dispose()
app = FastAPI(lifespan=lifespan)



# Add limiter middleware to the app
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Add the rate limit exceeded handler
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# app.include_router(auth_router, prefix="/api/v1/auth")
# app.include_router(auth_sso.router)
# app.include_router(auth_local.router)
app.include_router(auth_sso_otp.router)
app.include_router(profile_verfication.router)
app.include_router(stripe.router)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8001)
