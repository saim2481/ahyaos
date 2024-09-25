
from auth.db.models import *
from pydantic import BaseModel, EmailStr, validator, UUID4
from typing import List, Optional
import uuid


class UserBase(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    companyName: Optional[str] = None
    companyEmail: Optional[str] = None
    country_id: Optional[int] = None
    state_id: Optional[int] = None
    city_id: Optional[int] = None
    # password: str
    userTypeId: Optional[uuid.UUID]= None
    isReset: Optional[bool] = False
    ipAddress: Optional[str] = None
    thirdPartySubscriptionId: Optional[str] = None
    status: Optional[int] = 4
    remarks: Optional[str] = None

class PersonalInformationBase(BaseModel):
    firstName: str
    lastName: str
    email: str
    job_title: str
    contactNumber: str
    residentialAddressLine1: Optional[str] = None
    residentialAddressLine2: Optional[str] = None
    country_id: int
    state_id: int
    city_id: int
    postalCode: Optional[str] = None
    salutation_id: int
    createdAt: datetime
    createdBy: uuid.UUID

    class Config:
        orm_mode = True

class PersonalInformationResp(BaseModel):
    msg: str
    personal_information: PersonalInformationBase

    
    

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    job_title: Optional[str]
    organization_name: Optional[str]
    corporate_email: EmailStr
    password: str
    confirm_password: str
    # country: Optional[str] 7/15/2024
    country: int
    user_settings: List[uuid.UUID]  # Assuming support_preferences are UUIDs of User_Settings

    @validator('password')
    def passwords_match(cls, v, values, **kwargs):
        if 'confirm_password' in values and v != values['confirm_password']:
            raise ValueError('Passwords do not match')
        return v

class UserResp(UserBase):
    id: uuid.UUID
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None
    createdBy: Optional[uuid.UUID] = None
    updatedBy: Optional[uuid.UUID] = None
    deletedBy: Optional[uuid.UUID] = None
    image: Optional[str] = None
    signupverifiedby: Optional[uuid.UUID] = None
    profileverifiedby: Optional[uuid.UUID] = None

    # class Config:
    #     orm_mode = True
class UserRespMsg(BaseModel):
    msg:str
    user:UserResp
    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class OTPRequestForm(BaseModel):
    corporate_email: EmailStr
    otp: str

class ResendOTPRequestForm(BaseModel):
    reset_token: str

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    # token: str             # resend_token_logic
    access_token: str
    user: UserResp							   

class SimpleMsgTokenResponse(BaseModel):
    message: str
    reset_token: str

class OnlyEmailRequestForm(BaseModel):
    corporate_email: EmailStr

class UserResetPassword(BaseModel):
    token: str
    new_password: str

class UpdatePassword(BaseModel):
    user_id:uuid.UUID
    old_passsword:str
    new_password:str





# Utility function to send Reset password Link via email



class UserCreateOTP(UserCreate):

    otp: Optional[str]
    # first_name: str
    # last_name: str
    # job_title: Optional[str]
    # organization_name: Optional[str]
    # corporate_email: EmailStr
    # password: str
    # confirm_password: str
    # # country: Optional[str] 7/15/2024
    # country: int
    # user_settings: List[uuid.UUID]  # Assuming support_preferences are UUIDs of User_Settings

    # @validator('password')
    # def passwords_match(cls, v, values, **kwargs):
    #     if 'confirm_password' in values and v != values['confirm_password']:
    #         raise ValueError('Passwords do not match')
    #     return v
    
class UserSettingsAssignmentCreate(BaseModel):
    setting_ids: List[uuid.UUID]


class Token(BaseModel):
    message: str

class TokenData(BaseModel):
    id: Optional[uuid.UUID] = None





#@router.post("/login", response_model=LoginResponse) # specify response model
#async def login(form_data: LoginRequest, db: Session = Depends(get_db)):

# Endpoint to verify OTP and provide access token



#@router.post("/resend-otp")
#def resend_otp(form_data: ResendOTPRequestForm = Depends()):



# commented out only for the meeting 7/11/2024 
# Need amendments as well
# @router.post("/verify-token")
# def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#     user = get_user(db, username=token_data.username)
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#     return {"username": user.username}






# @router.post("/update-password-sso/", response_model=SimpleMsgTokenResponse)
# async def reset_password_ss0(form_data: OnlyEmailRequestForm, db: AsyncSession = Depends(get_db)):
#     payload = json.dumps({
#                 "email": "saim.rao@codelabs.inc"
#                 })
#     headers = {
#             'Content-Type': 'application/json'
#             }

#     response = requests.request("POST", FORGOT_PASSWORD_URL_SSO, headers=headers, data=payload)
    







class UserBusinessDetailsCreate(BaseModel):
    companyLegalName: str
    industry_id: int
    corporateWebsite: Optional[str]
    contactNumber: Optional[str]
    businessAddressLine1: str
    businessAddressLine2: Optional[str]
    country_id: int
    postalCode: str
    state_id: int
    city_id: int

class UserBusinessDetailsResp(BaseModel):
    msg: str
    details:UserBusinessDetailsCreate


    # class Config:
    #     from_attributes = True


# @router.post("/business-details", response_model=UserBusinessDetailsCreate)
# async def create_user_business_details(details: UserBusinessDetailsCreate, db: Session = Depends(get_db)):
#     # Check if the user ID exists
#     existing_user = await db.query(select(Users).filter(Users.id == details.userId).first())
#     if not existing_user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Create business details record
#     db_business_details = UserBusinessDetails(
#         userId=details.userId,
#         companyLegalName=details.companyLegalName,
#         industry=details.industry,
#         corporateWebsite=details.corporateWebsite,
#         contactNumber=details.contactNumber,
#         businessAddressLine1=details.businessAddressLine1,
#         businessAddressLine2=details.businessAddressLine2,
#         # country_id=details.country_id,
#         postalCode=details.postalCode,
#         state_id=details.state_id,
#         city_id=details.city_id,
#         createdAt=datetime.utcnow(),
#         createdBy=details.userId,  # Assuming createdBy is the user's UUID
#         updatedBy=details.userId   # Assuming updatedBy is the user's UUID
#     )
#     await db.add(db_business_details)
#     await db.commit()
#     await db.refresh(db_business_details)
    
#     return db_business_details        




class UserGoalsTargetsCreate(BaseModel):
    members_range: str
    accomplish_goal: str
    scope3_subcategories: Optional[List[str]] = []
    measured_emissions_before: bool
    last_year_emissions_year: Optional[int] = None
    last_year_emissions_value: Optional[float] = None
    emission_reduction_target: bool
    base_year_emissions_year: Optional[int] = None
    base_year_emissions_value: Optional[float] = None
    enterprise_emission_reduction_target_year: Optional[int] = None
    enterprise_emission_reduction_target_value: Optional[float] = None
    sbti_committed: bool
    sbti_scope12_near_term_year: Optional[int] = None
    sbti_scope12_near_term_target: Optional[float] = None
    sbti_scope12_long_term_year: Optional[int] = None
    sbti_scope12_long_term_target: Optional[float] = None
    sbti_scope3_near_term_year: Optional[int] = None
    sbti_scope3_near_term_emissions: Optional[float] = None
    sbti_scope3_long_term_year: Optional[int] = None
    sbti_scope3_long_term_emissions: Optional[float] = None
    sustainability_standard: str
    additional_support: str
    ai_enabled_measurement: str

class UserSettings(BaseModel):
    scope_selections: List[str] = []
    support_selection: str


class BankInformation(BaseModel):
    iban: str
    bankName: str
    accountTitle:str
    branch_location:str
    country_id:int
    city_id:int

class BankInformationResp(BaseModel):
    msg:str
    bank_information:BankInformation

class CompanyTaxRegistrationBase(BaseModel):

    id:uuid.UUID
    taxNo: str

    class Config:
        orm_mode = True

class CompanyTaxRegistrationResp(BaseModel):
    msg:str
    tax_info:CompanyTaxRegistrationBase

class UserGoalsTargetBase(BaseModel):
    id:uuid.UUID
    user_id:uuid.UUID
    setting_id:uuid.UUID
    createdAt:datetime

    class Config:
        orm_mode = True

class UserGoalsTargetResp(BaseModel):
    msg:str
    goals_and_targets: List[UserGoalsTargetBase]





# class BankImformationResp(BankInformation):

    