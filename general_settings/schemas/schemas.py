from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel


class GrossAreaBase(BaseModel):
    area:int

class GrossAreaRead(GrossAreaBase):
    
    id: int
    created_at: Optional[datetime] = None
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None



class GrossAreaResp(BaseModel):
    msg:str
    gross_area:GrossAreaRead


class UnitBase(BaseModel):
    name:str
    type:str

class UnitRead(UnitBase):
    
    id: int
    created_at: Optional[datetime] = None
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None



class UnitResp(BaseModel):
    msg:str
    unit:UnitRead

class UserSettingsBase(BaseModel):
    headerName: str
    sectionName: str
    value: str
    subValue: Optional[str]
    description: Optional[str]
    isOtherFields: bool
    sortOrder: int
    status: int

class UserSettingsCreate(UserSettingsBase):
    pass

class UserSettingsRead(UserSettingsBase):
    id: uuid.UUID
    createdAt: Optional[datetime]
    createdBy: Optional[uuid.UUID]
    updatedAt: Optional[datetime]
    updatedBy: Optional[uuid.UUID]
    deletedAt: Optional[datetime]
    deletedBy: Optional[uuid.UUID]

class UserSettingsResp(BaseModel):
    msg: str
    user_setting: UserSettingsRead

class TokenData(BaseModel):
    id: Optional[uuid.UUID] = None