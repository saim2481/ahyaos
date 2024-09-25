from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel
from measure.db import models



class UnitsCategory(BaseModel):
    
    id: int
    name:str
    created_at: Optional[datetime] = None
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None

class SubCategoryBase(BaseModel):
    name:str
    category_id: int

class SubCategoryMany(SubCategoryBase):
    
    id: int
    category_id:int
    created_at: Optional[datetime] = None
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None




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



class LocationBase(BaseModel):

    name:str 
    address:str 
    aptsuite:str 
    country_id:int
    state_id:int 
    city_id:int 
    zip_code:str 
    description:str

class LocationRead(LocationBase):

    id: uuid.UUID
    created_at: datetime
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None

class LocationResp(BaseModel):

    msg: str
    location: LocationRead

    class Config:
        orm_mode = True

class LocationRespBulk(BaseModel):
    msg: str
    locations: list[LocationRead]

    class Config:
        orm_mode = True

class FacilitiesBase(BaseModel):

    name:str
    internal_id:str
    description:str
    refrigrant_remaining_at_disposal:float
    occupancy:float

class FacilitiesCreate(FacilitiesBase):
    category_id:int
    sub_category_id:int
    location_id:uuid.UUID
    gross_area_id: int
    gross_area_unit_id: int
    

class FacilitiesRead(FacilitiesBase):
    id: uuid.UUID
    category_id: int
    sub_category_id: int
    location_id:uuid.UUID
    gross_area_id:int
    gross_area_unit_id:int
    created_at: datetime
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None

class FacilitiesReadRel(FacilitiesBase):
    id: uuid.UUID
    category: UnitsCategory
    sub_category: SubCategoryMany
    location:LocationRead
    gross_area:GrossAreaRead
    gross_area_unit:UnitsCategory
    created_at: datetime
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None

class FacilitiesResp(BaseModel):
    msg: str
    facility: FacilitiesRead

    class Config:
        orm_mode = True

class FacilitiesRespBulk(BaseModel):
    msg: str
    facilities: list[FacilitiesRead]

    class Config:
        orm_mode = True

#Financed Enitites


class FinancedEntitiesBase(BaseModel):

    name:str
    listed:bool
    description:str
    ticker:str
    contact_name:str
    contact_email:str
    internal_id:str
    

class FinancedEntitiesCreate(FinancedEntitiesBase):
    country_id:int
    state_id:int
    city_id:int
    industry_sector_id:int
    industry_id:int
    sub_industry_id:int
    

class FinancedEntitiesRead(FinancedEntitiesBase):
    id: uuid.UUID
    country_id:int
    state_id:int
    city_id:int
    industry_sector_id:int
    industry_id:int
    sub_industry_id:int
    created_at: datetime
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None

# class FinancedEntitiesReadRel(FinancedEntitiesBase):
#     id: uuid.UUID
#     category: UnitsCategory
#     sub_category: SubCategoryMany
#     location:LocationRead
#     gross_area:GrossAreaRead
#     gross_area_unit:UnitsCategory
#     created_at: datetime
#     created_by: Optional[uuid.UUID] = None
#     updated_at: Optional[datetime] = None
#     updated_by: Optional[uuid.UUID] = None
#     deleted_at: Optional[datetime] = None
#     deleted_by: Optional[uuid.UUID] = None

class FinancedEntitiesResp(BaseModel):
    msg: str
    financed_entity: FinancedEntitiesRead

    class Config:
        orm_mode = True

class FinancedEntitiesRespBulk(BaseModel):
    msg: str
    financed_entities: list[FinancedEntitiesRead]

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class EquipmentTypeBase(BaseModel):

    name:str
    installation_emission:int
    operation_emission_per_year:int
    refrigrant_remaining_at_disposal:int
    refrigrant_remaining_at_disposal_percentage:float
    



class EquipmentTypeCreate(EquipmentTypeBase):
    category_id:int
  
    

class EquipmentTypeRead(EquipmentTypeBase):
    id: uuid.UUID
    category_id:int
    created_at: datetime
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None

class EquipmentTypeResp(BaseModel):
    msg: str
    equipment_type: EquipmentTypeRead

    class Config:
        orm_mode = True

class EquipmentTypeRespBulk(BaseModel):
    msg: str
    equipment_types: list[EquipmentTypeRead]

    class Config:
        orm_mode = True

class FactorUnits(BaseModel):

    name:str


class FactorUnitsRead(FactorUnits):
    id: int
    created_at: datetime
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None

class PackageDetails(BaseModel):
    subscription_type: str  # e.g digital / manual
    package_name: Optional[str] = None  # e.g basic
    team: Optional[str] = None  # e.g 0-50
    state: str  # e.g active / non active
    recommended: str  # e.g yes / no
    price_monthly: float  # e.g 90
    discount_monthly: Optional[float] = None  # e.g 10
    price_yearly: float  # e.g 90
    discount_yearly: Optional[float] = None  # e.g 20
    feature_title: str  # e.g measure– your scope 1
    feature_caption: str  # e.g your scope description
    recommended_feature: str  # e.g yes / no

# # Pydantic models for request body
class Feature(BaseModel):
    title: str
    caption: str

class PackageCreate(BaseModel):
    subscription_type: str
    package_name: str = None
    team: str = None
    state: str
    recommended: bool
    price_monthly: int
    discount_monthly: int = None
    price_yearly: int
    discount_yearly: int = None
    features: list[Feature]

class ProductBase(BaseModel):

    name:str
    weight:int
    internal_id:str
    



class ProductCreate(ProductBase):
    
    category_id:int
    sub_category_id:int
    weight_unit_id:int
  
    

class ProductRead(ProductBase):
    id: uuid.UUID
    category_id:int
    sub_category_id:int
    weight_unit_id:int
    created_at: datetime
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None

class ProductResp(BaseModel):
    msg: str
    product: ProductRead

    class Config:
        orm_mode = True

class ProductRespBulk(BaseModel):
    msg: str
    products: list[ProductRead]

    class Config:
        orm_mode = True

class SupplierBase(BaseModel):

    name:str
    contact_name:str
    contact_email:str
    notes:str
    



class SupplierCreate(SupplierBase):
    
    industry_sector_id:int
    industry_id:int
    sub_industry_id:int
  
    

class SupplierRead(SupplierBase):
    id: uuid.UUID
    industry_sector_id:int
    industry_id:int
    sub_industry_id:int
    created_at: datetime
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None

class SupplierResp(BaseModel):
    msg: str
    supplier: SupplierRead

    class Config:
        orm_mode = True

class SupplierRespBulk(BaseModel):
    msg: str
    suppliers: list[SupplierRead]

    class Config:
        orm_mode = True

class CustomerBase(BaseModel):

    name:str
    contact_name:str
    contact_email:str
    notes:str
    



class CustomerCreate(CustomerBase):
    
    industry_sector_id:int
    industry_id:int
    sub_industry_id:int
  
    

class CustomerRead(CustomerBase):
    id: uuid.UUID
    industry_sector_id:int
    industry_id:int
    sub_industry_id:int
    created_at: datetime
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None

class CustomerResp(BaseModel):
    msg: str
    customer: CustomerRead

    class Config:
        orm_mode = True

class CustomerRespBulk(BaseModel):
    msg: str
    customers: list[CustomerRead]

    class Config:
        orm_mode = True


class UserCompanyAssignmentBase(BaseModel):

    user_id:uuid.UUID
    financed_entity_id:uuid.UUID

class UserCompanyAssignmentCreate(UserCompanyAssignmentBase):
    
    pass
    

class UserCompanyAssignmentRead(UserCompanyAssignmentBase):
    id: uuid.UUID
    financed_entity: FinancedEntitiesRead
    created_at: datetime
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None

class UserCompanyAssignmentResp(BaseModel):
    msg: str
    user_company_assignment: UserCompanyAssignmentRead

    class Config:
        orm_mode = True