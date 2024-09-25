# # from passlib.context import CryptContext
# # from jose import JWTError, jwt
# # from datetime import datetime, timedelta
# # from sqlalchemy.orm import Session
# # from fastapi import Depends, HTTPException, status
# # from ..db.models import User
# # from ..dependencies import get_db

# # SECRET_KEY = "your_secret_key"
# # ALGORITHM = "HS256"
# # ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # def hash_password(password: str):
# #     return pwd_context.hash(password)

# # def verify_password(plain_password, hashed_password):
# #     return pwd_context.verify(plain_password, hashed_password)

# # def create_access_token(data: dict, expires_delta: timedelta = None):
# #     to_encode = data.copy()
# #     if expires_delta:
# #         expire = datetime.utcnow() + expires_delta
# #     else:
# #         expire = datetime.utcnow() + timedelta(minutes=15)
# #     to_encode.update({"exp": expire})
# #     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
# #     return encoded_jwt

# # def authenticate_user(db: Session, username: str, password: str):
# #     user = db.query(User).filter(User.username == username).first()
# #     if not user or not verify_password(password, user.hashed_password):
# #         return False
# #     return user


# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# from sqlalchemy.orm import Session
# from fastapi import Depends, HTTPException, status
# from ..db.models import User
# from ..dependencies import get_db

# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def get_user(db: Session, username: str):
#     return db.query(User).filter(User.username == username).first()

# def authenticate_user(db: Session, username: str, password: str):
#     user = get_user(db, username)
#     if not user or not verify_password(password, user.hashed_password):
#         return False
#     return user

import os
import uuid
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from auth.schemas.schemas import TokenData
from ..db.models import Users
from ..dependencies import get_db
from typing import List, Optional
from dotenv import load_dotenv
# from variable_service import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,RESET_TOKEN_EXPIRE_MINUTES
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth_sso_otp/login-sso/")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
RESET_TOKEN_EXPIRE_MINUTES = int(os.getenv("RESET_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    print(expires_delta)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str, credential_exception):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        print(payload)
        # print(type(id))
        if id is None:
            raise credential_exception
        token_data = TokenData(id=uuid.UUID(id))
    except JWTError:
        raise credential_exception
    except ValueError:
        raise credential_exception
    print(token_data)
    return token_data.id

def get_current_user(token:str = Depends(oauth2_scheme)):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate':'Bearer'}
    )

    return verify_access_token(token,credential_exception)

async def authenticate_user(db: AsyncSession, corporate_email: str, password: str):
    result = await db.execute(select(Users).filter(Users.companyEmail == corporate_email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(password, user.password):
        return None
    
    return user

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_reset_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Utility function to verify reset token
def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise JWTError
        return email
    except JWTError:
        return None
