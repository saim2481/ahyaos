# from datetime import datetime
# from typing import Optional
# from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
from datetime import timedelta

from sqlalchemy import select
# from auth.dependencies import get_db
from auth.services.auth_service import authenticate_user, create_access_token, hash_password, get_user, create_reset_token, verify_reset_token
# from auth.db.models import User
# from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from auth.dependencies import get_db
from auth.services.auth_service import hash_password
from auth.db.models import *
import uuid
import os
import random
import string
from auth.schemas.schemas import UserCreate, LoginRequest, LoginResponse, SimpleMsgTokenResponse, OnlyEmailRequestForm, UserResetPassword, ResendOTPRequestForm, Token
from auth.services.otp_service import send_otp_via_email, send_otp_via_sms
from auth.services.email_service import send_approval_email, send_rejection_email, send_reset_password_email
from dotenv import load_dotenv


load_dotenv()

otp_store = {}

router = APIRouter(tags=['Local Authetication'], prefix='/api/v1/auth_local')


# Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
RESET_TOKEN_EXPIRE_MINUTES = int(os.getenv("RESET_TOKEN_EXPIRE_MINUTES"))
OTP_EXPIRE_MINUTES = int(os.getenv("OTP_EXPIRE_MINUTES"))

# SMTP_SERVER="sandbox.smtp.mailtrap.io"
# serverusername="a936521d5a6ab3"
# serverpassword="382c94c6cb8c04"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth_local/login-sso/")


@router.post("/reset-password", response_model=SimpleMsgTokenResponse)
async def reset_password(form_data: OnlyEmailRequestForm, db: AsyncSession = Depends(get_db)):

    user_result = await db.execute(select(Users).filter(Users.companyEmail == form_data.corporate_email))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    reset_token = create_reset_token({"sub": form_data.corporate_email})
    user.reset_token = reset_token
    user.reset_token_expiration = datetime.utcnow(
    ) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    await db.commit()

    # Send Reset Password Link via email
    status_ = send_reset_password_email(form_data.corporate_email, reset_token)

    if not status_:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send Reset password link via email",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"message": "Password reset email sent!", "reset_token": reset_token}


@router.post("/password-reset/", status_code=status.HTTP_200_OK)
async def reset_password(user_reset: UserResetPassword, db: AsyncSession = Depends(get_db)):
    email = verify_reset_token(user_reset.token)
    if email is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    # Query user
    user_result = await db.execute(select(Users).filter(Users.companyEmail == email))
    user = user_result.scalar_one_or_none()
    if not user or user.reset_token != user_reset.token or user.reset_token_expiration < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user.password = hash_password(user_reset.new_password)
    user.reset_token = None
    user.reset_token_expiration = None
    await db.commit()
    return {"msg": "Password reset successful"}


@router.post("/resend-otp", response_model=LoginResponse)
async def resend_otp(form_data: ResendOTPRequestForm, db: AsyncSession = Depends(get_db)):

    user_result = await db.execute(select(Users).filter(Users.companyEmail == form_data.corporate_email))
    user = user_result.scalar_one_or_none()
    user_details_result = await db.execute(select(UserBusinessDetails).filter(UserBusinessDetails.userId == user.id))
    user_details = user_details_result.scalar_one_or_none()

    user_country_result = await db.execute(select(GeneralCountries).filter(GeneralCountries.id == user.country_id))
    user_country = user_country_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate OTP
    otp = ''.join(random.choices(string.digits, k=6))
    otp_store[form_data.corporate_email] = {
        'otp': otp,
        'expires': datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)
    }
    print("otp----------------")

    # Send OTP via email
    status = send_otp_via_email(form_data.corporate_email, otp)

# Send OTP via SMS
    # if userDetails:
    #    send_otp_via_sms("+" + userCountry.phonecode + userDetails.contactNumber, otp)

    return {"message": status}


@router.post("/login", response_model=LoginResponse)  # specify response model
async def login(form_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.corporate_email, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_details_result = await db.execute(select(UserBusinessDetails).filter(UserBusinessDetails.userId == user.id))
    user_details = user_details_result.scalar_one_or_none()

    user_country_result = await db.execute(select(GeneralCountries).filter(GeneralCountries.id == user.country_id))
    user_country = user_country_result.scalar_one_or_none()

    # Generate OTP
    otp = ''.join(random.choices(string.digits, k=6))
    print(otp)
    otp_store[user.companyEmail] = {
        'otp': otp,
        'expires': datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)
    }
    print(otp_store)
    # Send OTP via email
    _status = send_otp_via_email(user.companyEmail, otp)
    # status = send_otp_via_email(user.companyEmail, otp)

    # Email OTP failed
    # if not status:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="Failed to send OTP via email",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    # Send OTP via SMS if details are present
    if not user_details or not user_country:
        return {"message": _status}
    else:
        send_otp_via_sms("+" + user_country.phonecode +
                         user_details.contactNumber, otp)

    return {"message": _status}


@router.post("/signup", response_model=UserCreate)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check for existing email
    existing_user_result = await db.execute(select(Users).filter(Users.companyEmail == user.corporate_email))
    existing_user = existing_user_result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    # Ensure integer conversion for certain fields
    country_id = int(user.country) if user.country else None
    # state_id = int(user.state) if user.state else None
    # city_id = int(user.city) if user.city else None

    # hashed_password = hash_password(user.password) (this line is commited so password is not saved)
    db_user = Users(
        firstName=user.first_name,
        lastName=user.last_name,
        companyName=user.organization_name,
        companyEmail=user.corporate_email,
        # password=hashed_password (this line is commited so password is not saved)
        country_id=user.country,  # Example value, replace with actual
        # Admin role UUID, replace with actual
        userTypeId=uuid.UUID('508a21b3-87df-416e-ad6e-9f01e927246b'),
        status=4,  # Assuming 4 is for active status
        createdAt=datetime.utcnow(),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # Handle multiple settings assignments
    for setting_id in user.user_settings:
        db_user_setting = UserSettingsAssignment(
            user_id=db_user.id,
            setting_id=setting_id,
            createdAt=datetime.utcnow(),
        )
        db.add(db_user_setting)

    await db.commit()

    return user


@router.post("/verify-otp", response_model=Token)
# async def verify_otp(username: str = Form(...),
#                     password: str = Form(...),
#                     db: Session = Depends(get_db)):
async def verify_otp(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    otp_entry = otp_store.get(form_data.username)
    print(otp_entry)

    # if not otp_entry or otp_entry['otp'] != form_data.password or datetime.utcnow() > otp_entry['expires']:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid or expired OTP",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    if not otp_entry or otp_entry['otp'] != form_data.password or datetime.utcnow() > otp_entry['expires']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create access token
    user_result = await db.execute(select(Users).filter(Users.companyEmail == form_data.username))
    user = user_result.scalar_one_or_none()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.companyEmail}, expires_delta=access_token_expires
    )

    # Create a new UserHistory entry
    user_history_entry = UserHistory(
        Type="OTP Verification",
        statusName="Verified",
        # status=1, #it will remain same an previous status
        remarks="OTP successfully verified",
        createdAt=datetime.utcnow(),
        createdBy=user.id
    )
    db.add(user_history_entry)
    await db.commit()

    # Clean up OTP entry after successful verification
    del otp_store[form_data.username]

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/send-rejection-email/")
def send_rejection_email_endpoint(email: str, token: str = Depends(oauth2_scheme),
                                  db: AsyncSession = Depends(get_db)):
    result = send_rejection_email(email)
    if result:
        return {"message": "Rejection email sent successfully"}
    else:
        raise HTTPException(
            status_code=500, detail="Failed to send rejection email")


@router.post("/send-approval-email/")
def send_approval_email_endpoint(email: str, token: str = Depends(oauth2_scheme),
                                 db: AsyncSession = Depends(get_db)):
    result = send_approval_email(email)
    if result:
        return {"message": "Approval email sent successfully"}
    else:
        raise HTTPException(
            status_code=500, detail="Failed to send approval email")
