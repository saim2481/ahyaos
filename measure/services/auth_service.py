import os
import uuid

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError
import jwt
from scipy import stats

from auth.schemas.schemas import TokenData

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://api-ahyaos.codelabs.inc/api/v1/auth_sso_otp/login-sso/")

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
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail='session has expired'
        )
   
    print(token_data)
    return token_data.id

def get_current_user(token:str = Depends(oauth2_scheme)):

    try:
        credential_exception = HTTPException(
            status_code=401,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate':'Bearer'}
        )

        return verify_access_token(token,credential_exception)
    except HTTPException as e:
        raise e