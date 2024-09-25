# from datetime import datetime
# from typing import Optional
# from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
from datetime import timedelta
from sqlalchemy import and_, select
# from auth.dependencies import get_db
from auth.services.auth_service import authenticate_user, create_access_token, get_current_user, hash_password, get_user
# from auth.db.models import User
# from pydantic import BaseModel
from jose import JWTError, jwt
import shutil
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, File, UploadFile, Form
from sqlalchemy.orm import Session
from datetime import datetime
from auth.dependencies import get_db
from auth.services.auth_service import hash_password
from auth.db.models import *
from pydantic import BaseModel, EmailStr, validator, UUID4
from typing import List, Optional
import uuid
import random
import json
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import traceback
import requests
from twilio.rest import Client
from auth.schemas.schemas import BankInformationResp, CompanyTaxRegistrationResp, PersonalInformationResp, UserGoalsTargetResp, UserRespMsg,Users,UserSettingsAssignmentCreate,SettingsSession,UserBusinessDetailsResp,UserGoalsTargetsCreate,UserGoalsTargets,UserBusinessDetailsCreate,UserBusinessDetails,LoginResponse,UserSettings,BankInformation
from auth.services.email_service import send_approval_email,send_profile_not_accepted_email,send_profile_under_verification_email,send_profile_verified_email,send_rejection_email
from auth.services.file_service import validate_file,save_file



otp_store = {}

router = APIRouter(tags=['Profile Verification'],prefix='/api/v1/profile-verfication')




# Configuration

# mailtrap_username = os.getenv("MAILTRAP_USERNAME")
# mailtrap_password = os.getenv("MAILTRAP_PASSWORD")
# SMTP_SERVER="email-smtp.eu-central-1.amazonaws.com"
# serverusername="AKIARZL4X6FTMDTXXRYI"
# serverpassword="BJXnGzShMJZ+xZFfefaaQlcBBHNoZ+IhrOrr/YRBf8O3"								
# SMTP_SERVER="sandbox.smtp.mailtrap.io"
# serverusername="a936521d5a6ab3"
# serverpassword="382c94c6cb8c04"									

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth_sso/login-sso/")


# @router.post("/user-goals-targets", response_model=UserGoalsTargetsCreate)
# async def create_user_goals_targets(
#     goals_targets: UserGoalsTargetsCreate,
#     settings: UserSettings,
#     user_id: int = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     # Check if the user exists
#     user = db.execute(select(Users).filter(Users.id == user_id).first())
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Create user goals and targets record
#     db_goals_targets = UserGoalsTargets(
#         user_id=user_id,
#         members_range=goals_targets.members_range,
#         accomplish_goal=goals_targets.accomplish_goal,
#         scope3_subcategories=goals_targets.scope3_subcategories,
#         measured_emissions_before=goals_targets.measured_emissions_before,
#         last_year_emissions_year=goals_targets.last_year_emissions_year,
#         last_year_emissions_value=goals_targets.last_year_emissions_value,
#         emission_reduction_target=goals_targets.emission_reduction_target,
#         base_year_emissions_year=goals_targets.base_year_emissions_year,
#         base_year_emissions_value=goals_targets.base_year_emissions_value,
#         enterprise_emission_reduction_target_year=goals_targets.enterprise_emission_reduction_target_year,
#         enterprise_emission_reduction_target_value=goals_targets.enterprise_emission_reduction_target_value,
#         sbti_committed=goals_targets.sbti_committed,
#         sbti_scope12_near_term_year=goals_targets.sbti_scope12_near_term_year,
#         sbti_scope12_near_term_target=goals_targets.sbti_scope12_near_term_target,
#         sbti_scope12_long_term_year=goals_targets.sbti_scope12_long_term_year,
#         sbti_scope12_long_term_target=goals_targets.sbti_scope12_long_term_target,
#         sbti_scope3_near_term_year=goals_targets.sbti_scope3_near_term_year,
#         sbti_scope3_near_term_emissions=goals_targets.sbti_scope3_near_term_emissions,
#         sbti_scope3_long_term_year=goals_targets.sbti_scope3_long_term_year,
#         sbti_scope3_long_term_emissions=goals_targets.sbti_scope3_long_term_emissions,
#         sustainability_standard=goals_targets.sustainability_standard,
#         additional_support=goals_targets.additional_support,
#         ai_enabled_measurement=goals_targets.ai_enabled_measurement,
#         created_at=datetime.utcnow(),
#         updated_at=datetime.utcnow()
#     )
#     db.add(db_goals_targets)
#     db.commit()
#     db.refresh(db_goals_targets)
    
#     # Handle multi-selection settings
#     for scope_selection in settings.scope_selections:
#         db_user_setting = UserSettingsAssignment(
#             user_id=db_goals_targets.user_id,
#             setting_name="scope_selection",
#             setting_value=scope_selection,
#             created_at=datetime.utcnow()
#         )
#         db.add(db_user_setting)
    
#     db_user_support = UserSettingsAssignment(
#         user_id=db_goals_targets.user_id,
#         setting_name="support_selection",
#         setting_value=settings.support_selection,
#         created_at=datetime.utcnow()
#     )
    
#     db.add(db_user_support)

#     db.commit()

#     return db_goals_targets


@router.post("/business-details", response_model=UserBusinessDetailsResp)
async def create_user_business_details(details: UserBusinessDetailsCreate, db: AsyncSession = Depends(get_db),user_id: uuid.UUID = Depends(get_current_user)):
    try:
        # Check if the user ID exists
        existing_user_result = await db.execute(select(Users).filter(Users.id == user_id))
        existing_user = existing_user_result.scalar_one_or_none()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Create business details record
        db_business_details = UserBusinessDetails(
            userId=existing_user.id,
            companyLegalName=details.companyLegalName,
            industry_id=details.industry_id,
            corporateWebsite=details.corporateWebsite,
            contactNumber=details.contactNumber,
            businessAddressLine1=details.businessAddressLine1,
            businessAddressLine2=details.businessAddressLine2,
            postalCode=details.postalCode,
            state_id=details.state_id,
            country_id=details.country_id,
            city_id=details.city_id,
            createdAt=datetime.utcnow(),
            createdBy=existing_user.id,  # Assuming createdBy is the user's UUID
            updatedBy=existing_user.id   # Assuming updatedBy is the user's UUID
        )
        db.add(db_business_details)
        await db.commit()
        await db.refresh(db_business_details)
        
        return {"msg":"Business details saved successfully","details":db_business_details}
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )  



@router.post("/personal-info", response_model=PersonalInformationResp)
async def personal_info(files: List[UploadFile],
    salutation: int = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    corporate_email: str = Form(...),
    job_title: str = Form(...),
    company_id_number: str = Form(...),
    phone_number: str = Form(...),
    address_line_1: str = Form(None),
    address_line_2: str = Form(None),
    country: str = Form(None),
    state: str = Form(None),
    city: str = Form(None),
    postal_code: str = Form(None),
    user_id: uuid.UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    try:
        # Check if user already exists or not
        user_result = await db.execute(select(Users).filter(Users.companyEmail == corporate_email,Users.id == user_id))
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Corporate Email not found!"
            )

        user_id = user.id

        user_country_result = await db.execute(select(GeneralCountries).filter(GeneralCountries.name == country))
        user_country = user_country_result.unique().scalar_one_or_none()

        if not user_country:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Country not found!"
            )

        user_country_id = user_country.id

        user_state_result = await db.execute(select(GeneralStates).filter(GeneralStates.name == state))
        user_state = user_state_result.scalar_one_or_none()

        if not user_state:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="State not found!"
            )

        user_state_id = user_state.id

        user_city_result = await db.execute(select(GeneralCities).filter(GeneralCities.name == city))
        user_city = user_city_result.scalar_one_or_none()

        if not user_city:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="City not found!"
            )

        user_city_id = user_city.id

        user_company = UserCompanyRegistrationTax(userId=user.id, company_id=company_id_number, createdAt=datetime.utcnow(), createdBy=user.id,)

        db.add(user_company)
        # await db.commit()
        # await db.refresh(user_company)

        user_company_id = user_company.id

        if not user_company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company not found!"
            )    
        
        db_user_personal_info = UserPersonalInformation(
            userId=user_id,
            company_id=user_company_id,
            salutation_id=salutation,
            firstName=first_name,
            lastName=last_name,
            email=corporate_email,
            job_title=job_title,
            contactNumber=phone_number,
            residentialAddressLine1=address_line_1,
            residentialAddressLine2=address_line_2,
            country_id=user_country_id,
            postalCode=postal_code,
            state_id=user_state_id,
            city_id=user_city_id,
            createdAt=datetime.utcnow(),
            createdBy=user_id,
        )
        db.add(db_user_personal_info)
        

        db_user_personal_info_id = db_user_personal_info.id


        # # Get the directory of the current file (auth.py)
        # current_dir = os.path.dirname(__file__)

        # # Move up two levels to the 'auth' directory
        # auth_dir = os.path.dirname(os.path.dirname(current_dir))


        # static_dir = os.path.join(auth_dir, 'static')

        # # Ensure the logs directory exists
        # if not os.path.exists(static_dir):
        #     os.makedirs(static_dir)
        # image_filename = f"User_Personal_Information_image_{corporate_email}_{image.filename}"
        # image_file = await validate_file(image)
        # image_path = await save_file(image_file, filename)
        # # file_path = f"static/{file.filename}"
        # with open(image_path, "wb") as buffer:
        #     shutil.copyfileobj(image_file.file, buffer)
        
        # imaeg_db_file = UserPersonalFiles(
        #     user_id=user_id,
        #     screen_name = "User_Personal_Information",
        #     screen_uuid = db_user_personal_info_id,
        #     file_name=image_filename,
        #     file_path=image_path
        # )
        # db.add(imaeg_db_file)
        

        # Save the files
        for file in files:
            filename = f"User_Personal_Information_{corporate_email}_{file.filename}"
            file = await validate_file(file)
            path = await save_file(file, filename)
            # file_path = f"static/{file.filename}"
            # with open(path, "wb") as buffer:
                # shutil.copyfileobj(file.file, buffer)
            
            db_file = UserPersonalFiles(
                user_id=user_id,
                screen_name = "User_Personal_Information",
                screen_uuid = db_user_personal_info_id,
                file_name=filename,
                file_path=path
            )
            db.add(db_file)
        
        await db.flush()
        
        await db.commit()
        await db.refresh(db_user_personal_info)
        return {"msg": "Personal information saved successfully","personal_information":db_user_personal_info}

    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )      
    

@router.post("/send-profile-under-verification-email/")
def send_under_verification_email_endpoint(email: str,user_id: uuid.UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    result = send_profile_under_verification_email(email)
    if result:
        return {"message": "Profile under verification email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send profile under verification email")
    

@router.post("/send-profile-not-accepted-email/")
def send_not_accepted_email_endpoint(email: str,user_id: uuid.UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    result = send_profile_not_accepted_email(email)
    if result:
        return {"message": "Profile not accepted email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send profile not accepted email")

@router.post("/send-profile-verified-email/")
def send_verified_email_endpoint(email: str,user_id: uuid.UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    result = send_profile_verified_email(email)
    if result:
        return {"message": "Verification email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send verification email")
    

@router.post("/bank-information",response_model=BankInformationResp)
async def create_bank_details(bank_info:BankInformation,user_id: uuid.UUID = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
        
    try:
        user_query = await db.execute(select(Users).filter(Users.id == user_id))
        user = user_query.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        tax_reg = await db.execute(select(UserCompanyRegistrationTax).filter(UserCompanyRegistrationTax.userId == user_id))
        tax_reg_res = tax_reg.scalars().first()

        bank_account = UserBankAccountInformation(
            userId = user_id,
            bankName = bank_info.bankName,
            iban = bank_info.iban,
            accountName = bank_info.accountTitle,
            bankBranch = bank_info.branch_location,
            country_id = bank_info.country_id,
            city_id = bank_info.city_id,
            company_id = tax_reg_res.id
        )
        db.add(bank_account)
        await db.commit()
        db.refresh(bank_account)
        return {"msg":"Bank account information saved successfully","bank_information":bank_info}
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )      
        

@router.post("/registration-tax/",response_model = CompanyTaxRegistrationResp)
async def create_registration_tax(
    certificate_or_license: UploadFile = File(...),
    tax_document: UploadFile = File(...),
    others: UploadFile = File(...),
    tax_number: str = Form(...),
    user_id: uuid.UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):

    try:

        files = [certificate_or_license,tax_document,others]

        # async with db.begin():
        company_tax_query = await db.execute(select(UserCompanyRegistrationTax).where(UserCompanyRegistrationTax.userId == user_id))
        result = company_tax_query.scalars().first()
        user = await db.execute(select(Users).where(Users.id == user_id))
        user_result = user.scalar_one_or_none()


        if result:
            result.taxNo = tax_number
            print(result.taxNo)
            for file in files:
                file = await validate_file(file)
                path = await save_file(file, f"User_Personal_Information_{user_result.companyEmail}_{file.filename}")
                userfiles = UserPersonalFiles(
                    user_id=user_id,
                    file_path=path,
                    screen_name = "User_Company_Registration_Tax",
                    screen_uuid = result.id,
                    file_name=os.path.basename(path)
                )
                db.add(userfiles)
            
            # await db.flush()
            
            
        else:
            raise HTTPException(status_code=404, detail='User not found')
        
        
        await db.commit()
        await db.refresh(result)

        return {"msg":"Tax Registration saved successfully","tax_info":result}
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )     

    
    

@router.post("/goals-and-targets/",response_model=UserGoalsTargetResp)
async def create_goals_and_targets(
    settings_assignment: UserSettingsAssignmentCreate,
    user_id: uuid.UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):

    try:

        print(user_id)
        
        # Handle multiple settings assignments
        created_settings = []
        for setting_id in settings_assignment.setting_ids:
            # Check if the assignment already exists
            existing_assignment = await db.execute(
                select(UserSettingsAssignment).filter(
                    and_(
                        UserSettingsAssignment.user_id == user_id,
                        UserSettingsAssignment.setting_id == setting_id
                    )
                )
            )
            if existing_assignment.scalar_one_or_none() is None:
                db_user_setting = UserSettingsAssignment(
                    user_id=user_id,
                    setting_id=setting_id,
                    createdAt=datetime.utcnow(),
                )
                db.add(db_user_setting)
                created_settings.append(db_user_setting)
            else:
                raise HTTPException(status_code=409)

        if created_settings:
            await db.commit()
            for setting in created_settings:
                await db.refresh(setting)
        created_settings
        return {"msg":"user goals and targets saved successfully","goals_and_targets":created_settings}
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )     
    

@router.put('/business-profile-image/',response_model=UserRespMsg)
async def change_user_profile_image(image:UploadFile=File(...),db: AsyncSession = Depends(get_db),user_id: uuid.UUID = Depends(get_current_user)):
    try:
        user = await db.execute(select(Users).where(Users.id == user_id))
        user_result = user.scalar_one_or_none()
        # print(user_result.companyEmail)

        if not user_result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        image_filename = f"{user_id}_{user_result.companyEmail}_{image.filename}"
        image_file = await validate_file(image)
        image_path = await save_file(image_file, image_filename,True)
        # file_path = f"static/{file.filename}"
        # with open(image_path, "wb") as buffer:
        #     shutil.copyfileobj(image_file.file, buffer)
        user_result.image = image_path
        # await db.flush()
        await db.commit()
        await db.refresh(user_result)
        # print(user_result.image)
        return{
            "msg":"Profile image saved successfully",
            "user": user_result
        }
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error changing profile picture"
        )     