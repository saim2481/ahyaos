# from datetime import datetime
# from typing import Optional
# from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
from datetime import timedelta,datetime, timezone
from sqlalchemy import select
# from auth.dependencies import get_db
# from auth.services.auth_service import authenticate_user, create_access_token, hash_password, get_user
# from auth.db.models import User
# from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, File, UploadFile, Form
from sqlalchemy.orm import Session
from datetime import datetime
from auth.dependencies import get_db
from auth.services.auth_service import create_access_token, get_current_user, hash_password
from auth.db.models import *
import uuid
import random
import json
import os
import string
import requests
from auth.schemas.schemas import ResendOTPRequestForm, UserCreate,LoginRequest,LoginResponse,Token
from auth.services.email_service import send_approval_email, send_rejection_email
from auth.services.otp_service import send_otp_via_email,send_otp_via_sms,generate_resend_token
from dotenv import load_dotenv

load_dotenv()
# from auth.services.variable_service import SIGNUP_URL_SSO,API_KEY,LOGIN_URL_SSO,CHAGE_PASSWORD_URL_SSO,RESET_PASSWORD_URL_SSO,FORGOT_PASSWORD_URL_SSO,OTP_EXPIRE_MINUTES,ACCESS_TOKEN_EXPIRE_MINUTES


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
OTP_EXPIRE_MINUTES = int(os.getenv("OTP_EXPIRE_MINUTES"))
SIGNUP_URL_SSO = os.getenv("SIGNUP_URL_SSO")#"https://dev-api-app.tawazun.io/register/"
LOGIN_URL_SSO = os.getenv("LOGIN_URL_SSO")#"https://dev-api-app.tawazun.io/auth/login"
FORGOT_PASSWORD_URL_SSO = os.getenv("FORGOT_PASSWORD_URL_SSO")#"https://dev-api-app.tawazun.io/auth/forgot-password"
RESET_PASSWORD_URL_SSO = os.getenv("RESET_PASSWORD_URL_SSO")#"https://dev-api-app.tawazun.io/auth/reset-password"
CHAGE_PASSWORD_URL_SSO = os.getenv("CHAGE_PASSWORD_URL_SSO")#"https://dev-api-app.tawazun.io/auth/change-password"
API_KEY = os.getenv("API_KEY")#"API_KEY_b17c2e02e015b3dcfb8e130bd092872e133c43de"
OTP_MAX_COUNT  = int(os.getenv("otp_max_count"))
OTP_RESEND_TIME = int(os.getenv("otp_resend_time"))
OTP_RESEND_COUNT_RESET_TIME = int(os.getenv("otp_resend_count_reset_time"))


otp_store = {}

router = APIRouter(tags=['SSO Based Authetication'],prefix='/api/v1/auth_sso')

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth_sso/login-sso/")



# # Async function to perform initial database queries
# async def init_db():
#     async with get_db() as db:
#         sso_cred_query = db.execute(select(SettingsSSO))
#         return sso_cred_query.scalars().first()
        
# # Run initial queries

# async def startup_event():
#     await init_db()
      
    

# Configuration

# SECRET_KEY = "1234567"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# RESET_TOKEN_EXPIRE_MINUTES = 10
# OTP_EXPIRE_MINUTES = 10
# SIGNUP_URL_SSO = sso_settings.signup_url#"https://dev-api-app.tawazun.io/register/"
# LOGIN_URL_SSO = sso_settings.login_url#"https://dev-api-app.tawazun.io/auth/login"
# FORGOT_PASSWORD_URL_SSO = sso_settings.forgot_pwd_url#"https://dev-api-app.tawazun.io/auth/forgot-password"
# RESET_PASSWORD_URL_SSO = sso_settings.reset_pwd_url#"https://dev-api-app.tawazun.io/auth/reset-password"
# CHAGE_PASSWORD_URL_SSO = sso_settings.change_pwd_url#"https://dev-api-app.tawazun.io/auth/change-password"
# API_KEY = sso_settings.api_key#"API_KEY_b17c2e02e015b3dcfb8e130bd092872e133c43de"
								
# SMTP_SERVER="sandbox.smtp.mailtrap.io"
# serverusername="a936521d5a6ab3"
# serverpassword="382c94c6cb8c04"									






@router.post("/signup-sso/",response_model=UserCreate)
async def signup_sso(user: UserCreate, db: AsyncSession = Depends(get_db)):

    # """commented to avoid local db check for user"""
    # existing_user_result = await db.execute(select(Users).filter(Users.companyEmail == user.corporate_email))
    # existing_user = existing_user_result.scalar_one_or_none()
    
    # if existing_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email is already registered"
    #     )
    
    payload = json.dumps({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.corporate_email,
                "password": user.password,
                "organization_name": user.organization_name
                })
    
    headers = {
                'x-api-key': API_KEY,
                'Content-Type': 'application/json'
                }
    
    response = requests.request("POST", SIGNUP_URL_SSO, headers=headers, data=payload)

    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    
    response_data = json.loads(response.text)
    
    
    # Ensure integer conversion for certain fields
    country_id = int(user.country) if user.country else None
    # state_id = int(user.state) if user.state else None
    # city_id = int(user.city) if user.city else None

   # hashed_password = hash_password(user.password) (this line is commited so password is not saved)
    db_user = Users(
        sso_id=response_data['id'],
        firstName=user.first_name,
        lastName=user.last_name,
        companyName=user.organization_name,
        companyEmail=user.corporate_email,
        # password=hashed_password (this line is commited so password is not saved)
        country_id=user.country,  # Example value, replace with actual
        userTypeId=uuid.UUID('508a21b3-87df-416e-ad6e-9f01e927246b'),  # Admin role UUID, replace with actual
        status=4,  # Assuming 4 is for active status
        createdAt=datetime.utcnow(),
    )
    db.add(db_user)
    await db.flush()
    
    # Handle multiple settings assignments
    for setting_id in user.user_settings:
        db_user_setting = UserSettingsAssignment(
            user_id=db_user.id,
            setting_id=setting_id,
            createdAt=datetime.utcnow(),
        )
        db.add(db_user_setting)
    

    if db_user:
        #Handle user history
        user_history = UserHistory(
            Type="Sign up SSO",
            statusName="Verified",
            status = db_user.status,
            remarks = "Account created successfully",
            createdBy = db_user.id
        )
        db.add(user_history)
    await db.commit()
           
    return user

@router.post("/login-sso/", response_model=LoginResponse) # specify response model
async def login_sso(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    

    payload = json.dumps({
        "email": form_data.username,
        "password": form_data.password
        })
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
        }
    print(LOGIN_URL_SSO)
    response = requests.request("POST", LOGIN_URL_SSO, headers=headers, data=payload)

    

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    # resend_token = generate_resend_token()
    user_result = await db.execute(select(Users).filter(Users.sso_id == response.json()["data"]["id"],Users.companyEmail==form_data.username))
    user = user_result.scalar_one_or_none()
    if not user:
        user_type = await db.execute(select(UserRole).filter(UserRole.typeName=="User"))
        user_type_res = user_type.scalar_one_or_none()
        user = Users(
            firstName = response.json()["data"]["first_name"],
            lastName = response.json()["data"]["last_name"],
            companyName = response.json()["data"]["organization"]["name"],
            companyEmail = response.json()["data"]["email"],
            userTypeId = user_type_res.id,
            sso_id = response.json()["data"]["id"],
            status = 1,
            # resend_token_logic
            # reset_token = resend_token,
            # reset_token_expiration = datetime.now()     

        )
        db.add(user)
        await db.flush()
    otp_records = await db.execute(select(SystemOTPSessions).filter(SystemOTPSessions.userId == user.id))
    otp_records_result = otp_records.scalars().first() 

    if otp_records_result:
        otp_records_result.last_resend_count = 0
        otp_records_result.createdAt = datetime.now()
    else:
        otp_record = SystemOTPSessions(
            userId = user.id,
            last_resend_count = 0,
            createdAt = datetime.now()
        )
        db.add(otp_record)
    
    # resend_token_logic
    # user.reset_token = resend_token
    # user.reset_token_expiration = datetime.now()
    user_details_result = await db.execute(select(UserBusinessDetails).filter(UserBusinessDetails.userId == user.id))
    user_details = user_details_result.scalar_one_or_none()

    user_country_result = await db.execute(select(GeneralCountries).filter(GeneralCountries.id == user.country_id))
    user_country = user_country_result.scalar_one_or_none()    



    #Handle user history
    user_history = UserHistory(
        Type="Sign In",
        statusName="Attempted",
        status = user.status,
        remarks = "Sign In Attempted",
        createdBy = user.id
    )
    db.add(user_history)
    access_token = create_access_token({'sub':str(user.id)})
    print(access_token)
    # Generate OTP
    otp = ''.join(random.choices(string.digits, k=6))

    
    print(otp)
    otp_store[user.companyEmail] = {
        'otp': otp,
        'expires': datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)
    }
    print(otp_store)
    # Send OTP via email
    _status=send_otp_via_email(user.companyEmail, otp)
    # status = send_otp_via_email(user.companyEmail, otp)
    otp_storage = UserCodes(
        userId = user.id,
        code = otp,
        identityName = user.companyEmail,
        type = "OTP",
        status = 1,
        createdAt = datetime.now()
    )
    db.add(otp_storage)
    # Email OTP failed
    if not _status:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP via email",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Send OTP via SMS if details are present
    await db.commit()
    if not user_details or not user_country:
        return {"message": _status,'access_token':access_token}
    else:
        send_otp_via_sms("+" + user_country.phonecode + user_details.contactNumber, otp)

    return {"message": _status,'access_token':access_token,'user':user}


@router.post("/resend-otp", response_model=dict)
async def resend_otp(db: AsyncSession = Depends(get_db),user_id: uuid.UUID = Depends(get_current_user)):

    user_result = await db.execute(select(Users).filter(Users.id == user_id))
    user = user_result.scalar_one_or_none()
    # resend_token_logic
    # if (not user) or (not otp_record_result):
    #     raise HTTPException(status_code=400, detail="Invalid or expired resend token")
    otp_record = await db.execute(select(SystemOTPSessions).filter(SystemOTPSessions.userId == user_id))
    otp_record_result = otp_record.scalars().first() 

    
    # resend_token_logic
    # Check if the token is not older than 10 minutes
    # if datetime.now() - user.reset_token_expiration > timedelta(minutes=10):
        # raise HTTPException(status_code=400, detail="Resend token has expired")
    
     # Reset resend count if last OTP was sent more than 30 minutes ago
    if otp_record_result.createdAt < datetime.now(timezone.utc) - timedelta(minutes=OTP_RESEND_COUNT_RESET_TIME):
        otp_record_result.last_resend_count = 0
    
    # Check if the last OTP was sent less than 1 minute ago
    if (otp_record_result.last_resend_at) and (datetime.now(timezone.utc) - otp_record_result.last_resend_at < timedelta(minutes=OTP_RESEND_TIME)):
        raise HTTPException(status_code=429, detail="Please wait before requesting another OTP")
    
     # Check if more than 5 resends have been requested
    if otp_record_result.last_resend_count >= OTP_MAX_COUNT:
        raise HTTPException(status_code=429, detail="Maximum resend limit reached. Please request a new OTP.")

    

    user_details_result = await db.execute(select(UserBusinessDetails).filter(UserBusinessDetails.userId == user_id))
    user_details = user_details_result.scalar_one_or_none()
    
    user_country_result = await db.execute(select(GeneralCountries).filter(GeneralCountries.id == user.country_id))
    user_country = user_country_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # resend_token = generate_resend_token()																								   

    # Update resend token
    # user.reset_token = resend_token
    # user.reset_token_expiration = datetime.now()

    otp_record_result.last_resend_count += 1
    otp_record_result.last_resend_at = datetime.now()
    
    # Generate OTP
    otp = ''.join(random.choices(string.digits, k=6))
    otp_store[user.companyEmail] = {
        'otp': otp,
        'expires': datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)
    }
    print("otp----------------")
    
    # Send OTP via email
    status=send_otp_via_email(user.companyEmail, otp)

    user_codes_result = await db.execute(select(UserCodes).filter(UserCodes.userId == user_id,UserCodes.status == 1))
    user_codes = user_codes_result.scalars().all()
    for i in user_codes:
        i.status = 3

    otp_storage = UserCodes(
        userId = user.id,
        code = otp,
        identityName = user.companyEmail,
        type = "OTP",
        status = 1,
        createdAt = datetime.now()
    )
    db.add(otp_storage)
    await db.commit()	
# Send OTP via SMS
    #if userDetails:
    #    send_otp_via_sms("+" + userCountry.phonecode + userDetails.contactNumber, otp)
			     
    return {"message": status}

@router.post("/forgot-password-sso/", status_code=status.HTTP_200_OK)
async def forgot_password_sso(email: str = Form(...)):
    payload = json.dumps({
            "email": email
            })
    headers = {
            'x-api-key':API_KEY,
            'Content-Type': 'application/json'
            }

    response = requests.request("POST", FORGOT_PASSWORD_URL_SSO, headers=headers, data=payload)
    

    return response.json()

@router.post("/reset-password-sso/", status_code=status.HTTP_200_OK)
async def reset_password_sso(token: str = Form(...),new_password: str = Form(...)):
    payload = json.dumps({
            "new_password": new_password
            })
    headers = {
            'x-api-key':API_KEY,
            'Content-Type': 'application/json'
            }

    response = requests.request("POST", RESET_PASSWORD_URL_SSO + f'?token={token}', headers=headers, data=payload)

    return response.json()




@router.put("/update-password-sso/", status_code=status.HTTP_200_OK)
async def update_password_sso(
    old_password: str = Form(...),
    new_password: str = Form(...),
    user_id: uuid.UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    user_result = await db.execute(select(Users).filter(Users.id == user_id))
    user = user_result.scalar_one_or_none()
    payload = json.dumps({
            "old_password": old_password,
            "new_password": new_password
            })
    headers = {
            'x-api-key':API_KEY,
            'Content-Type': 'application/json'
            }

    response = requests.request("PUT", CHAGE_PASSWORD_URL_SSO + f'?user_id={user.sso_id}', headers=headers, data=payload)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    """"commited so that passwords is not pdated in db"""
    # user.password = hash_password(new_password)
    # await db.commit()
    return {"msg": "Password reset successful"}

@router.post("/verify-otp", response_model=Token)
# async def verify_otp(username: str = Form(...),
#                     password: str = Form(...),
#                     db: Session = Depends(get_db)):
async def verify_otp(otp:str = Query(None,description="OTP"),db: AsyncSession = Depends(get_db),user_id: uuid.UUID = Depends(get_current_user)):
   
    # if not otp_entry or otp_entry['otp'] != form_data.password or datetime.utcnow() > otp_entry['expires']:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid or expired OTP",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    user_codes_result = await db.execute(select(UserCodes).filter(UserCodes.userId == user_id,UserCodes.code == otp))
    user_codes = user_codes_result.scalar_one_or_none()

    if not user_codes:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OTP",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif datetime.now(timezone.utc) - user_codes.createdAt > timedelta(minutes=OTP_EXPIRE_MINUTES):
           user_codes.status = 3
           raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired OTP",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

    user_codes.status = 2

    # Create a new UserHistory entry
    user_history_entry = UserHistory(
        Type="OTP Verification",
        statusName="Verified",
        # status=1, #it will remain same an previous status
        remarks="OTP successfully verified",
        createdAt=datetime.utcnow(),
        createdBy=user_id
    )
    db.add(user_history_entry)
    await db.commit()

    

    
    return {"message": "OTP verified successfully" }


# @router.post("/verify-otp", response_model=Token,tags=['Local Authetication'])
# # async def verify_otp(username: str = Form(...),
# #                     password: str = Form(...),
# #                     db: Session = Depends(get_db)):
# async def verify_otp(db: AsyncSession = Depends(get_db),user_id: uuid.UUID = Depends(get_current_user)):
#     otp_entry = otp_store.get(form_data.username)
#     print(otp_entry)
    
#     # if not otp_entry or otp_entry['otp'] != form_data.password or datetime.utcnow() > otp_entry['expires']:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_401_UNAUTHORIZED,
#     #         detail="Invalid or expired OTP",
#     #         headers={"WWW-Authenticate": "Bearer"},
#     #     )
#     if not otp_entry or otp_entry['otp'] != form_data.password or datetime.utcnow() > otp_entry['expires']:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired OTP",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     # Create access token
#     user_result = await db.execute(select(Users).filter(Users.companyEmail == form_data.username))
#     user = user_result.scalar_one_or_none()
    

#     # Create a new UserHistory entry
#     user_history_entry = UserHistory(
#         Type="OTP Verification",
#         statusName="Verified",
#         # status=1, #it will remain same an previous status
#         remarks="OTP successfully verified",
#         createdAt=datetime.utcnow(),
#         createdBy=user.id
#     )
#     db.add(user_history_entry)
#     await db.commit()

    
#     # Clean up OTP entry after successful verification
#     del otp_store[form_data.username]
    
#     return {"message": "OTP verified successfully" }

@router.post("/send-rejection-email/")
def send_rejection_email_endpoint(email: str,user_id: uuid.UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    result = send_rejection_email(email)
    if result:
        return {"message": "Rejection email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send rejection email")
    
@router.post("/send-approval-email/")
def send_approval_email_endpoint(email: str,user_id: uuid.UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    result = send_approval_email(email)
    if result:
        return {"message": "Approval email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send approval email")
    
