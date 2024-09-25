import traceback
import uuid
from fastapi import APIRouter, Depends, Form, HTTPException, Query
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from datetime import datetime
from typing import List, Optional
from auth.db.models import UserSalutation
from general_settings.db.models import Category, Industry, IndustrySector, SubCategory, UserSalutation,UserBankAccountInformation,UserSettings,GeneralCountries, GeneralCities, GeneralStates, UserRole, Users
from pydantic import BaseModel
from general_settings.dependencies_async import get_async_db
from general_settings.services.auth_service import get_current_user
from uuid import UUID as UUIDType
from general_settings.db.crud.crude_gross_area import crud_gross_area,crud_unit,crud_user_settings
from general_settings.schemas import schemas



router = APIRouter()

# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/AhyaOS"

# # Async engine and session setup
# async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# async_session_factory = sessionmaker(
#     async_engine, expire_on_commit=False, class_=AsyncSession
# )

# # Dependency to get the async database session
# async def get_async_db():
#     async with async_session_factory() as session:
#         yield session

# Base = declarative_base()

# Country models
class CountryBase(BaseModel):
    name: str
    iso3: Optional[str] = None
    numeric_code: Optional[str] = None
    iso2: Optional[str] = None
    phonecode: Optional[str] = None
    capital: Optional[str] = None
    currency: Optional[str] = None
    currency_name: Optional[str] = None
    currency_symbol: Optional[str] = None
    tld: Optional[str] = None
    native: Optional[str] = None
    region: Optional[str] = None
    # region_id: Optional[int] = None
    subregion: Optional[str] = None
    # subregion_id: Optional[int] = None
    nationality: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    emoji: Optional[str] = None
    emojiU: Optional[str] = None
    # flage: Optional[int] = None

class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    id: int
    flag: int
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    deletedAt: Optional[datetime]
    

# City models
class CityBase(BaseModel):
    name: str
    state_id: int
    state_code: str
    country_id: int
    country_code: str
    latitude: float
    longitude: float
    wikiDataId: Optional[str] = None
    
class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    flag: int

# State models
class StateBase(BaseModel):
    name: str
    country_id: int
    country_code: str
    fips_code: Optional[str] = None
    iso2: Optional[str] = None
    type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    flag: int = 1
    wikiDataId: Optional[str] = None
 

class StateCreate(StateBase):
    pass

class State(StateBase):
    id: int

# # Country endpoints
# @router.post("/countries/", response_model=Country, tags=["Country"])
# async def create_country(country: CountryCreate, db: AsyncSession = Depends(get_async_db)):
#     db_country = GeneralCountries(**country.dict(), created_at=datetime.utcnow())
#     db.add(db_country)
#     await db.commit()
#     await db.refresh(db_country)
#     return db_country

@router.post("/countries/", response_model=Country, tags=["Country"])
async def create_country(country: CountryCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        db_country = GeneralCountries(**country.dict(), createdAt=datetime.utcnow())
        db.add(db_country)
        await db.commit()
        await db.refresh(db_country)
        return db_country
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create country: {str(e)}")
    

@router.get("/countries/", response_model=List[Country], tags=["Country"])
async def read_countries(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to retrieve"),
    name: Optional[str] = Query(None, description="Name of the country"),
    iso3: Optional[str] = Query(None, description="ISO3 code of the country"),
    numeric_code: Optional[str] = Query(None, description="Numeric code of the country"),
    iso2: Optional[str] = Query(None, description="ISO2 code of the country"),
    phonecode: Optional[str] = Query(None, description="Phone code of the country e.g. 93"),
    capital: Optional[str] = Query(None, description="Capital city of the country"),
    currency: Optional[str] = Query(None, description="Currency code of the country"),
    currency_name: Optional[str] = Query(None, description="Currency name of the country"),
    currency_symbol: Optional[str] = Query(None, description="Currency symbol of the country e.g. ؋"),
    tld: Optional[str] = Query(None, description="Top-level domain of the country e.g. .af"),
    native: Optional[str] = Query(None, description="Native name of the country"),
    region: Optional[str] = Query(None, description="Region of the country"),
    region_id: Optional[int] = Query(None, description="Region ID of the country"),
    subregion: Optional[str] = Query(None, description="Subregion of the country"),
    subregion_id: Optional[int] = Query(None, description="Subregion ID of the country"),
    nationality: Optional[str] = Query(None, description="Nationality of the country"),
    latitude: Optional[float] = Query(None, description="Latitude of the country"),
    longitude: Optional[float] = Query(None, description="Longitude of the country"),
    flag: Optional[float] = Query(None, description="flage of the country"),
    db: AsyncSession = Depends(get_async_db)
):
    filters = {}
    if name:
        filters['name'] = name
    if iso3:
        filters['iso3'] = iso3
    if numeric_code:
        filters['numeric_code'] = numeric_code
    if iso2:
        filters['iso2'] = iso2
    if phonecode:
        filters['phonecode'] = phonecode
    if capital:
        filters['capital'] = capital
    if currency:
        filters['currency'] = currency
    if currency_name:
        filters['currency_name'] = currency_name
    if currency_symbol:
        filters['currency_symbol'] = currency_symbol
    if tld:
        filters['tld'] = tld
    if native:
        filters['native'] = native
    if region:
        filters['region'] = region
    if region_id:
        filters['region_id'] = region_id
    if subregion:
        filters['subregion'] = subregion
    if subregion_id:
        filters['subregion_id'] = subregion_id
    if nationality:
        filters['nationality'] = nationality
    if latitude:
        filters['latitude'] = latitude
    if longitude:
        filters['longitude'] = longitude
    if flag:
        filters['flage'] = flag


    stmt = select(GeneralCountries).filter_by(**filters).offset(skip).limit(limit).order_by(GeneralCountries.id)
    countries = await db.execute(stmt)
    return countries.scalars().all()

# @router.get("/countries/{country_id}", response_model=Country, tags=["Country"])
# async def read_country(country_id: int, db: AsyncSession = Depends(get_async_db)):
#     country = await db.query(GeneralCountries).filter(GeneralCountries.id == country_id).first()
#     if country is None:
#         raise HTTPException(status_code=404, detail="Country not found")
#     return country
# @router.get("/countries/{country_id}", response_model=Country, tags=["Country"])
# async def read_country(country_id: int):
#     async with get_async_db() as session:
#         statement = select(GeneralCountries).where(GeneralCountries.id == country_id)
#         result = await session.execute(statement)
#         country = result.scalars().first()
#         return country
@router.get("/countries/{country_id}", response_model=Country, tags=["Country"])
async def read_country(country_id: int, db: AsyncSession = Depends(get_async_db)):
    statement = select(GeneralCountries).where(GeneralCountries.id == country_id)
    result = await db.execute(statement)
    country = result.scalars().first()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country
@router.put("/countries/{country_id}", response_model=Country, tags=["Country"])
async def update_country(country_id: int, country: CountryCreate, db: AsyncSession = Depends(get_async_db)):
    db_country = await db.execute(select(GeneralCountries).where(GeneralCountries.id == country_id))
    result = db_country.scalars().first()
    if result:
        for key, value in country.dict(exclude_unset=True).items():
            setattr(result, key, value)
        result.updatedAt = datetime.utcnow()
        await db.commit()
        await db.refresh(result)
        return result
    raise HTTPException(status_code=404, detail="Country not found")

@router.delete("/countries/{country_id}", response_model=dict, tags=["Country"])
async def delete_country(country_id: int, db: AsyncSession = Depends(get_async_db)):
    db_country = await db.execute(select(GeneralCountries).where(GeneralCountries.id == country_id))
    result = db_country.scalars().first()
    print(result.name)
    if result:
        result.deletedAt = datetime.utcnow()
        await db.commit()
        await db.refresh(result)
        return {"message": "Country deleted successfully"}
    raise HTTPException(status_code=404, detail="Country not found")

# City endpoints
@router.post("/cities/", response_model=City, tags=["City"])
async def create_city(city: CityCreate, db: AsyncSession = Depends(get_async_db)):
    db_city = GeneralCities(**city.dict(),createdAt=datetime.utcnow())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city

@router.get("/cities/", response_model=List[City], tags=["City"])
async def read_cities(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to retrieve"),
    name: Optional[str] = Query(None, description="Name of the city"),
    state_id: Optional[int] = Query(None, description="ID of the state to filter by"),
    state_code: Optional[str] = Query(None, description="Code of the state to filter by"),
    country_id: Optional[int] = Query(None, description="ID of the country to filter by"),
    country_code: Optional[str] = Query(None, description="Code of the country to filter by"),
    latitude: Optional[float] = Query(None, description="Latitude of the city"),
    longitude: Optional[float] = Query(None, description="Longitude of the city"),
    db: AsyncSession = Depends(get_async_db)
):
    filters = {}
    if name:
        filters['name'] = name
    if state_id:
        filters['state_id'] = state_id
    if state_code:
        filters['state_code'] = state_code
    if country_id:
        filters['country_id'] = country_id
    if country_code:
        filters['country_code'] = country_code
    if latitude:
        filters['latitude'] = latitude
    if longitude:
        filters['longitude'] = longitude

    stmt = select(GeneralCities).filter_by(**filters).offset(skip).limit(limit)
    cities = await db.execute(stmt)
    return cities.scalars().all()

@router.get("/cities/{city_id}", response_model=City, tags=["City"])
async def read_city(city_id: int, db: AsyncSession = Depends(get_async_db)):
    city = await db.execute(select(GeneralCities).filter(GeneralCities.id == city_id))
    city_results = city.scalars().first()
    if city_results is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city_results

@router.put("/cities/{city_id}", response_model=City, tags=["City"])
async def update_city(city_id: int, city: CityCreate, db: AsyncSession = Depends(get_async_db)):
    city_db = await db.execute(select(GeneralCities).filter(GeneralCities.id == city_id))
    city_results = city_db.scalars().first()
    if city_results:
        for key, value in city.dict(exclude_unset=True).items():
            setattr(city_results, key, value)
        city_results.updatedAt = datetime.utcnow()
        await db.commit()
        await db.refresh(city_results)
        return city_results
    raise HTTPException(status_code=404, detail="City not found")

@router.delete("/cities/{city_id}", response_model=dict, tags=["City"])
async def delete_city(city_id: int, db: AsyncSession = Depends(get_async_db)):
    city_db = await db.execute(select(GeneralCities).filter(GeneralCities.id == city_id))
    city_results = city_db.scalars().first()
    if city_results:
        city_results.deletedAt = datetime.utcnow()
        await db.commit()
        await db.refresh(city_results)
        return {"message": "City deleted successfully"}
    raise HTTPException(status_code=404, detail="City not found")

# State endpoints
@router.post("/states/", response_model=State, tags=["State"])
async def create_state(state: StateCreate, db: AsyncSession = Depends(get_async_db)):
    db_state = GeneralStates(**state.dict(), createdAt=datetime.utcnow())
    db.add(db_state)
    await db.commit()
    await db.refresh(db_state)
    return db_state

@router.get("/states/", response_model=List[State], tags=["State"])
async def read_states(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to retrieve"),
    name: Optional[str] = Query(None, description="Name of the state"),
    country_id: Optional[int] = Query(None, description="ID of the country to filter by"),
    country_code: Optional[str] = Query(None, description="Code of the country to filter by"),
    fips_code: Optional[str] = Query(None, description="FIPS code of the state"),
    iso2: Optional[str] = Query(None, description="ISO2 code of the state"),
    type: Optional[str] = Query(None, description="Type of the state"),
    latitude: Optional[float] = Query(None, description="Latitude of the state"),
    longitude: Optional[float] = Query(None, description="Longitude of the state"),
    db: AsyncSession = Depends(get_async_db)
):
    filters = {}
    if name:
        filters['name'] = name
    if country_id:
        filters['country_id'] = country_id
    if country_code:
        filters['country_code'] = country_code
    if fips_code:
        filters['fips_code'] = fips_code
    if iso2:
        filters['iso2'] = iso2
    if type:
        filters['type'] = type
    if latitude:
        filters['latitude'] = latitude
    if longitude:
        filters['longitude'] = longitude

    stmt = select(GeneralStates).filter_by(**filters).offset(skip).limit(limit)
    states = await db.execute(stmt)
    return states.scalars().all()

@router.get("/states/{state_id}", response_model=State, tags=["State"])
async def read_state(state_id: int, db: AsyncSession = Depends(get_async_db)):
    state = await db.execute(select(GeneralStates).filter(GeneralStates.id == state_id))
    state_result = state.scalars().first()
    if state_result is None:
        raise HTTPException(status_code=404, detail="State not found")
    return state_result

@router.put("/states/{state_id}", response_model=State, tags=["State"])
async def update_state(state_id: int, state: StateCreate, db: AsyncSession = Depends(get_async_db)):
    state_db = await db.execute(select(GeneralStates).filter(GeneralStates.id == state_id))
    state_result = state_db.scalars().first()
    if state_result:
        for key, value in state.dict(exclude_unset=True).items():
            setattr(state_result, key, value)
        state_result.updatedAt = datetime.utcnow()
        await db.commit()
        await db.refresh(state_result)
        return state_result
    raise HTTPException(status_code=404, detail="State not found")

@router.delete("/states/{state_id}", response_model=dict, tags=["State"])
async def delete_state(state_id: int, db: AsyncSession = Depends(get_async_db)):
    state = await db.execute(select(GeneralStates).filter(GeneralStates.id == state_id))
    state_result = state.scalars().first()
    if state_result:
        db.delete(state_result)
        state_result.deletedAt = datetime.utcnow()
        await db.commit()
        await db.refresh(state_result)
        return {"message": "State deleted successfully"}
    raise HTTPException(status_code=404, detail="State not found")

#role model
class UserRoleBase(BaseModel):

    typeName : str
    description : str

class UserRoleCreate(UserRoleBase):
    pass

class userRoleResp(UserRoleBase):
    id: UUIDType




@router.post("/user-roles/",response_model=userRoleResp,tags=["Roles"])
async def create_user_role(role:UserRoleCreate,
    db: AsyncSession = Depends(get_async_db)):
    userRole = UserRole(**role.model_dump(),)
    db.add(userRole)
    await db.commit()
    await db.refresh(userRole)
    return userRole
@router.get("/users-roles/{user_role_id}", response_model=userRoleResp, tags=["Roles"])
async def get_user_role(user_role_id: uuid.UUID, db: AsyncSession = Depends(get_async_db)):
    user_query = await db.execute(select(UserRole).filter(UserRole.id == user_role_id))
    user_result = user_query.scalars().first()
    if user_result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_result

@router.put("/user-roles/{id}",tags=["Roles"])
async def update_user_role(
    id:UUIDType,
    Type_name: str = Query(None, description="Type of user role like (Admin,SuperAdmin,User)"),
    Description: str = Query(None, description="Description of user role"),
    db: AsyncSession = Depends(get_async_db)):
    userRoleQeury = await db.execute(select(UserRole).filter(UserRole.id == id))
    role_instance = userRoleQeury.scalars().first()
    if role_instance:
        role_instance.TypeName = Type_name
        role_instance.description = Description
        await db.commit()
        await db.refresh(role_instance)
        return role_instance
    raise HTTPException(status_code=404, detail="Role not found")
@router.delete("/user-roles/{id}",response_model=dict,tags=["Roles"])
async def delete_user_role(id:UUIDType,db: AsyncSession = Depends(get_async_db)):
    userRoleQeury = await db.execute(select(UserRole).filter(UserRole.id == id))
    role_instance = userRoleQeury.scalars().first()
    if role_instance:
        await db.delete(role_instance)
        await db.commit()
        return {"message": "Role deleted successfully"}
    raise HTTPException(status_code=404, detail="Role not found")

@router.get("/user-roles/",response_model=List[userRoleResp],tags=["Roles"])
async def create_user_role(db: AsyncSession = Depends(get_async_db),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to retrieve"),
    Type_name: str = Query(None, description="Type of user role like (Admin,SuperAdmin,User)"),
    Description: str = Query(None, description="Description of user role")
                           ):
    
    filters = {}
    if Type_name:
        filters['typeName'] = Type_name
    if Description:
        filters['description'] = Description
    userRolesAll = await db.execute(select(UserRole).filter_by(**filters).offset(skip).limit(limit)) 
    return userRolesAll.scalars().all()

async def get_unique_values():
    async with AsyncSession() as session:
        async with session.begin():
            result = await session.execute(select(UserSettings.headerName.distinct()))
            unique_values = [row[0] for row in result.fetchall()]
            return unique_values


@router.post("/user-settings/",response_model=schemas.UserSettingsResp,tags=['User Settings'])
async def create_user_setting(
        header_name:str = Form(...),
        section_name:str = Form(...),
        sub_value:str = Form(...),
        value:str = Form(...),
        description:str = Form(...),
        is_other_fields:bool = Form(...),
        sort_order:int = Form(...),
        status:int = Form(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    data = {
        "headerName":header_name,
        "sectionName":section_name,
        "subValue":sub_value,
        "value":value,
        "description":description,
        "isOtherFields":is_other_fields,
        "sortOrder":sort_order,
        "status":status,
        "createdBy": user_id
    }

    user_setting = await crud_user_settings.create(db=db,obj_in=data)

    return{
        "msg": "User setting created successfully",
        "user_setting":user_setting
    }
    



@router.get("/user-settings/",response_model=List[schemas.UserSettingsRead],tags=['User Settings'])
async def get_user_settings(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to retrieve"),
    header_name: str = Query(None, description="Name of Header refers to the screen name (Signup, Goals & targets)"),
    section_name: str = Query(None, description="""Name of section refers to the fields present in Screen(
\nScope 3 sub-categories 
\nAI enabled measurement interest 
\nAhyaOS Support
\nEmissions measurement history 
\nAccomplishments with AhyaOS 
\nNumber of AhyaOS Account members
\nEmission reduction target
\nAdditional support with AhyaOS
\nSustainability standard)"""),
    sub_value: str = Query(None, description="Name of subvalue"),
    value: str = Query(None, description="""Value of setting refers to the selectable options available in figma design(
\nPart time climate science/data science teams
\nPartnership for Carbon Accounting Financials
\nCDP
\nGHG Protocol
\nSupply chain
\nGlobal Reporting Initiative
\nPeople activity
\nYes - require AhyaAI predictive analytics
\nNo additional support needed
\nYes
\nNo
\nOther
\nRequire analysis of emissions, such as emissions intensity, facilities, sectoral comparison et al
\nAlready calculating Scope 1 and 2, need to do Scope 3
\nMeasure scope 1 & 2 emissions
\nReporting requirement - financial disclosure (IFRS, GRI)
\nReporting requirement - internal (GHG Protocol)
\nReport emissions
\nReduction plan - internal or group level targets
\nReduce emissions
\nMeasure scope 3 emissions
\nNot applicable
\nNot interested
\nYes - require AhyaAI data check
\nOther - applied AhyaAI
\nAnalyze emissions
\nYes - require AhyaAI reduction optimization
\nReporting requirement - investors (IFRS, GRI)
\nMeasure all scopes
\nDedicated climate science/data science teams
\nReduction plan - international buyer requirement (SBTi)
\nLeased assets
\nFinanced emissions
\n1-50
\nAccess to emission factors database
\nYes - require AhyaAI co-pilot assistance
\nSites
\n51-250
\n500+
\nReporting requirement - sustainability report (IFRS, GRI, CDP)
\nOther - integrations with existing software
\n251-500
\nReporting requirement - banking or fund management guidelines (GHG Protocol, IFRS)
\nIFRS S-2
\nSimplifying data collection and GHG accounting)"""),
    description: str = Query(None, description="Description of setting"),
    is_other_field: bool = Query(None, description=""),
    sort_order: int = Query(None, description=""),
    status: int = Query(None, description="status of setting"),
    db: AsyncSession = Depends(get_async_db)):
    filters = {}
    if header_name:
        filters['headerName'] = header_name
    if section_name:
        filters['sectionName'] = section_name
    if sub_value:
        filters['subValue'] = sub_value
    if value:
        filters['value'] = value
    if description:
        filters['description'] = description
    if is_other_field:
        filters['isOtherFeilds'] = is_other_field
    if sort_order:
        filters['sortOrder'] = sort_order
    if status:
        filters['status'] = status
    
    stmt = select(UserSettings).filter_by(**filters).offset(skip).limit(limit)
    states = await db.execute(stmt)
    if states:
        return states.scalars().all()
    else:
        raise HTTPException(status_code=404, detail="Role not found")

@router.get("/user-settings/{user_settings_id}",response_model=schemas.UserSettingsRead,tags=['User Settings'])
async def get_user_setting(
        user_setting_id: uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):

    user_setting = await crud_user_settings.get(db=db,id=user_setting_id)

    return user_setting

@router.put("/user-settings/{user_settings_id}",response_model=schemas.UserSettingsResp,tags=['User Settings'])
async def create_user_setting(
        user_setting_id: uuid.UUID,
        user_setting: schemas.UserSettingsCreate,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    

    user_setting_updated = await crud_user_settings.update(db=db,obj_in=user_setting,id=user_setting_id,user_id=user_id)

    return {
        "msg": "User setting updated successfully",
        "user_setting":user_setting_updated
    }

@router.delete("/user-settings/{user_settings_id}",response_model=dict,tags=['User Settings'])
async def create_user_setting(
        user_setting_id: uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    await crud_user_settings.delete(db=db,id=user_setting_id,user_id=user_id)

    return {
        "msg" : "User setting deleted successfully"
    }
      


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

class UserCreate(UserBase):
    pass

class UserResp(UserBase):
    id: uuid.UUID
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None
    createdBy: Optional[uuid.UUID] = None
    updatedBy: Optional[uuid.UUID] = None
    deletedBy: Optional[uuid.UUID] = None
    signupverifiedby: Optional[uuid.UUID] = None
    profileverifiedby: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True


@router.get("/users/", response_model=List[UserResp], tags=["User"])
async def get_user_settings(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to retrieve"),
    first_name: str = Query(None, description="First name of user"),
    last_name: str = Query(None, description="Last name of user"),
    company_name: str = Query(None, description="User's company name"),
    company_email: str = Query(None, description="User's company email"),
    country_id: int = Query(None, description="User's country id"),
    state_id: int = Query(None, description="User's state id"),
    city_id: int = Query(None, description="User's city id"),
    user_type_id: uuid.UUID = Query(None, description="Type id of the user"),
    ip_address: str = Query(None, description="ipaddress of user"),
    third_party_subscription: str = Query(None, description="third party subscriptions of user"),
    status: int = Query(None, description="status of user"),
    remarks: str = Query(None, description="remarks on user"),
    db: AsyncSession = Depends(get_async_db)):
    filters = {}
    if first_name:
        filters['firstName'] = first_name
    if last_name:
        filters['lastName'] = last_name
    if company_name:
        filters['companyName'] = company_name
    if company_email:
        filters['companyEmail'] = company_email
    if country_id:
        filters['country_id'] = country_id
    if state_id:
        filters['state_id'] = state_id
    if city_id:
        filters['city_id'] = city_id
    if status:
        filters['status'] = status
    if user_type_id:
        filters['userTypeId'] = user_type_id
    if ip_address:
        filters['ipAddress'] = ip_address
    if third_party_subscription:
        filters['thirdPartySubscriptionId'] = third_party_subscription
    if remarks:
        filters['remarks'] = remarks

    stmt = select(Users).filter_by(**filters).offset(skip).limit(limit)
    states = await db.execute(stmt)
    if states:
        return states.scalars().all()
    else:
        raise HTTPException(status_code=404, detail="Role not found")


@router.get("/users/{user_id}", response_model=UserResp, tags=["User"])
async def read_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_async_db)):
    user_query = await db.execute(select(Users).filter(Users.id == user_id))
    user_result = user_query.scalars().first()
    if user_result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_result

@router.put("/users/{user_id}", response_model=UserResp, tags=["User"])
async def update_user(user_id: uuid.UUID, user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    user_query = await db.execute(select(Users).filter(Users.id == user_id))
    user_result = user_query.scalars().first()
    if user_result:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(user_result, key, value)
        user_result.updatedAt = datetime.utcnow()
        await db.commit()
        await db.refresh(user_result)
        return user_result
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}", response_model=dict, tags=["User"])
async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_async_db)):
    user_query = await db.execute(select(Users).filter(Users.id == user_id))
    user_result = user_query.scalars().first()
    if user_result:
        # db.delete(user)
        user_result.status = 3  # Update user status to 3 (inactive)
        await db.commit()
        return {"message": "User deleted (Status updated to 3)successfully"}
    raise HTTPException(status_code=404, detail="User not found")
    
@router.post("/change-user-status/",tags=["User"])
async def change_user_status(
    user_id: uuid.UUID = Form(...),
    status: int = Form(...,description="The status of the user (1: Active, 2: Inactive, 3: Delete, 4: Pending Signup/Incomplete, 5: Signup Rejected, 6: Pending Profle/Under Review, 7: Pending for Approval, 8: Rejected Profile, 9: Subscription Pending, 10: Subscription Cancelled)"),
    remarks: str = Form(...),
    db: AsyncSession = Depends(get_async_db)):

    user_query = await db.execute(select(Users).filter(Users.id == user_id))
    user_results = user_query.scalars().first()
    if not user_results:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_results.remarks = remarks
    user_results.status = status
    await db.commit()
    await db.refresh(user_results)
    return {
        "notification":f"status changed to {status} for user{user_id} successfully",
        "user":user_results}


class UserBankAccountInfoBase(BaseModel):
    userId: uuid.UUID
    bankName: Optional[str] = None
    bankBranch: Optional[str] = None
    accountName: Optional[str] = None
    accountNumber: Optional[str] = None
    swiftCode: Optional[str] = None
    iban: Optional[str] = None
    currency: Optional[str] = None
    country_id: Optional[int] = None
    createdAt: Optional[datetime] = None
    createdBy: Optional[uuid.UUID] = None
    updatedAt: Optional[datetime] = None
    updatedBy: Optional[uuid.UUID] = None
    deletedAt: Optional[datetime] = None
    deletedBy: Optional[uuid.UUID] = None

class UserBankAccountInfoCreate(UserBankAccountInfoBase):
    pass

class UserBankAccountInfo(UserBankAccountInfoBase):
    id: uuid.UUID

    class Config:
        orm_mode = True



@router.get("/user_bank_accounts/", response_model=list[UserBankAccountInfo], tags=["User Bank Account Info"])
async def read_user_bank_account_infos(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to retrieve"),
    userId: Optional[uuid.UUID] = Query(None, description="The ID of the user"),
    bankName: Optional[str] = Query(None, description="The name of the bank"),
    bankBranch: Optional[str] = Query(None, description="The branch of the bank"),
    accountTitle: Optional[str] = Query(None, description="The title of the account"),
    accountNumber: Optional[str] = Query(None, description="The account number"),
    iban: Optional[str] = Query(None, description="The IBAN of the account"),
    swiftCode: Optional[str] = Query(None, description="The SWIFT code of the account"),
    createdAt: Optional[datetime] = Query(None, description="The creation timestamp"),
    createdBy: Optional[uuid.UUID] = Query(None, description="The ID of the creator"),
    updatedAt: Optional[datetime] = Query(None, description="The update timestamp"),
    updatedBy: Optional[uuid.UUID] = Query(None, description="The ID of the updater"),
    deletedAt: Optional[datetime] = Query(None, description="The deletion timestamp"),
    deletedBy: Optional[uuid.UUID] = Query(None, description="The ID of the deleter"),
        db: AsyncSession = Depends(get_async_db)):
    query = select(UserBankAccountInformation).offset(skip).limit(limit)
    
    if userId:
        query = query.where(UserBankAccountInformation.userId == userId)
    if bankName:
        query = query.where(UserBankAccountInformation.bankName == bankName)
    if bankBranch:
        query = query.where(UserBankAccountInformation.bankBranch == bankBranch)
    if accountTitle:
        query = query.where(UserBankAccountInformation.accountName == accountTitle)
    if accountNumber:
        query = query.where(UserBankAccountInformation.accountNumber == accountNumber)
    if iban:
        query = query.where(UserBankAccountInformation.iban == iban)
    if swiftCode:
        query = query.where(UserBankAccountInformation.swiftCode == swiftCode)
    if createdAt:
        query = query.where(UserBankAccountInformation.createdAt == createdAt)
    if createdBy:
        query = query.where(UserBankAccountInformation.createdBy == createdBy)
    if updatedAt:
        query = query.where(UserBankAccountInformation.updatedAt == updatedAt)
    if updatedBy:
        query = query.where(UserBankAccountInformation.updatedBy == updatedBy)
    if deletedAt:
        query = query.where(UserBankAccountInformation.deletedAt == deletedAt)
    if deletedBy:
        query = query.where(UserBankAccountInformation.deletedBy == deletedBy)

    result = await db.execute(query)
    results = result.scalars().all()
    return results

@router.get("/user_bank_accounts/{user_bank_account_info_id}", response_model=UserBankAccountInfo, tags=["User Bank Account Info"])
async def read_user_bank_account_info(user_bank_account_info_id: uuid.UUID, db: AsyncSession = Depends(get_async_db)):
    user_bank_info_query = await db.execute(select(UserBankAccountInformation).filter(UserBankAccountInformation.id == user_bank_account_info_id))
    user_result = user_bank_info_query.scalars().first()
    if user_result is None:
        raise HTTPException(status_code=404, detail="User bank account information not found")
    return user_result

@router.put("/user_bank_accounts/{user_bank_account_info_id}", response_model=UserBankAccountInfo, tags=["User Bank Account Info"])
async def update_user_bank_account_info(user_bank_account_info_id: uuid.UUID, user_bank_account_info: UserBankAccountInfoCreate, db: AsyncSession = Depends(get_async_db)):
    user_bank_info_query = await db.execute(select(UserBankAccountInformation).filter(UserBankAccountInformation.id == user_bank_account_info_id))
    user_bank_info_result = user_bank_info_query.scalars().first()
    if user_bank_info_result is None:
        raise HTTPException(status_code=404, detail="User bank account information not found")
    for key, value in user_bank_account_info.dict(exclude_unset=True).items():
        setattr(user_bank_info_result, key, value)
    user_bank_info_result.updatedAt = datetime.utcnow()    
    db.add(user_bank_info_result)
    await db.commit()
    await db.refresh(user_bank_info_result)
    return user_bank_info_result

@router.delete("/user_bank_accounts/{user_bank_account_info_id}", response_model=UserBankAccountInfo, tags=["User Bank Account Info"])
async def delete_user_bank_account_info(user_bank_account_info_id: uuid.UUID, db: AsyncSession = Depends(get_async_db)):
    user_bank_info_query = await db.execute(select(UserBankAccountInformation).filter(UserBankAccountInformation.id == user_bank_account_info_id))
    user_bank_info_result = user_bank_info_query.scalars().first()
    if user_bank_info_result is None:
        raise HTTPException(status_code=404, detail="User bank account information not found")
    user_bank_info_result.deletedAt = datetime.now()
    await db.commit()
    await db.refresh(user_bank_info_result)
    return user_bank_info_result 


class SalutationBase(BaseModel):
    
    
    salutation: str

class Salutation(SalutationBase):
    
    id: int

class SalutationResp(BaseModel):

    notification: str
    salutation: Salutation





    


@router.post("/salutation/",response_model=SalutationResp,tags=["Salutations"])
async def create_salutation(
    salutation : str = Form(...),
    db: AsyncSession = Depends(get_async_db)):

    try:
        salutation_db = UserSalutation(
            salutation = salutation 
        )

        db.add(salutation_db)
        await db.commit()
        await db.refresh(salutation_db)

        return{
            "notification" : "Salutation created successfuly",
            "salutation": salutation_db
        }
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)

@router.get("/salutation/",response_model=List[Salutation],tags=["Salutations"])
async def get_salutations(db: AsyncSession = Depends(get_async_db)):

    try:
        salutations = await db.execute(select(UserSalutation))
        salutation_result  =  salutations.scalars().all()
        return salutation_result
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)

@router.get("/salutation/{salutation_id}",response_model=Salutation,tags=["Salutations"])
async def get_salutation(salutation_id:int,db: AsyncSession = Depends(get_async_db)):

    salutations = await db.execute(select(UserSalutation).filter(UserSalutation.id==salutation_id))
    salutation_result  =  salutations.scalars().first()
    if salutation_result:
        return salutation_result
    raise HTTPException(status_code=404, detail="Salutation not found")



@router.put("/salutation/{salutation_id}",response_model=SalutationResp,tags=["Salutations"])
async def get_salutation(salutation_id:int,salutation:SalutationBase,db: AsyncSession = Depends(get_async_db)):

    try:
        salutations = await db.execute(select(UserSalutation).filter(UserSalutation.id==salutation_id))
        salutation_result  =  salutations.scalars().first()
        salutation_result.salutation = salutation.salutation
        await db.commit()
        await db.refresh(salutation_result)
        return{
            "notification" : "Salutation updated successfuly",
            "salutation": salutation_result
        }
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)

@router.delete("/salutation/{salutation_id}", response_model=dict, tags=["Salutations"])
async def delete_salutation(salutation_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await db.execute(select(UserSalutation).filter(UserSalutation.id == salutation_id))
        salutation_result = result.scalars().first()
        if salutation_result is None:
            raise HTTPException(status_code=404, detail="Salutation not found")
        
        await db.delete(salutation_result)
        await db.commit()
        
        return {"notification": "Salutation deleted successfully"}
    except:
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


class IndustrySectorBase(BaseModel):
    name:str


class IndustrySectorMany(IndustrySectorBase):
    
    id: int
    created_at: Optional[datetime] = None
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None

class IndustrySectorResp(BaseModel):
    msg:str
    industry_sector:IndustrySectorMany


    

@router.post("/industry-sector/",response_model=IndustrySectorResp,tags=["Industry Sector"])
async def create_industry_sector(
    name : str = Form(...),
    db: AsyncSession = Depends(get_async_db)):

    try:
        industry_sector_db = IndustrySector(
            name = name 
        )

        db.add(industry_sector_db)
        await db.commit()
        await db.refresh(industry_sector_db)

        return{
            "msg" : "Industry sector created successfuly",
            "industry_sector": industry_sector_db
        }
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)
    
@router.get("/industry-sector/",response_model=List[IndustrySectorMany],tags=["Industry Sector"])
async def get_industry_sectors(db: AsyncSession = Depends(get_async_db)):

    try:
        inddustry_sectors = await db.execute(select(IndustrySector))
        inddustry_sectors_result  =  inddustry_sectors.scalars().all()
        return inddustry_sectors_result
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)
    
@router.get("/industry-sector/{industry_sector_id}",response_model=IndustrySectorMany,tags=["Industry Sector"])
async def get_industry_sectors(industry_sector_id:int,db: AsyncSession = Depends(get_async_db)):

    try:
        inddustry_sector = await db.execute(select(IndustrySector).where(IndustrySector.id == industry_sector_id))
        inddustry_sector_result  =  inddustry_sector.scalars().first()
        
        return inddustry_sector_result
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)
    
@router.put("/industry-sector/{industry_sector_id}",response_model=IndustrySectorMany,tags=["Industry Sector"])
async def update_industry_sectors(industry_sector_id:int,industry_sector:IndustrySectorBase,db: AsyncSession = Depends(get_async_db)):

    try:
        inddustry_sector = await db.execute(select(IndustrySector).where(IndustrySector.id == industry_sector_id))
        inddustry_sector_result  =  inddustry_sector.scalars().first()
        inddustry_sector_result.name = industry_sector.name
        print(industry_sector)
        await db.commit()
        await db.refresh(inddustry_sector_result)
        return {"msg":"Industry sector save successfully","industry_sector":inddustry_sector_result}
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)

@router.delete("/industry-sector/{industry_sector_id}",tags=["Industry Sector"])
async def delete_industry_sectors(industry_sector_id:int,db: AsyncSession = Depends(get_async_db)):

    try:
        inddustry_sector = await db.execute(select(IndustrySector).where(IndustrySector.id == industry_sector_id))
        inddustry_sector_result  =  inddustry_sector.scalars().first()
        await db.delete(inddustry_sector_result)
        
        await db.commit()
        # await db.refresh(inddustry_sector_result)
        return {"msg":"industry sector deleted successfully"}
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)
    
class IndustryBase(BaseModel):
    name:str
    sector_id: int

class IndustryMany(IndustryBase):
    
    id: int


class IndustryResp(BaseModel):
    msg:str
    industry:IndustryBase


    

@router.post("/industry/",response_model=IndustryResp,tags=["Industry"])
async def create_industry(
    name : str = Form(...),
    sector_id : int = Form(...),
    db: AsyncSession = Depends(get_async_db)):

    try:
        industry_db = Industry(
            name = name,
            sector_id = sector_id
        )

        db.add(industry_db)
        await db.commit()
        await db.refresh(industry_db)

        return{
            "msg" : "Industry created successfuly",
            "industry": industry_db
        }
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)
    
@router.get("/industry/",response_model=List[IndustryMany],tags=["Industry"])
async def get_industry(sector_id:int = Query(None, description="Industry sector"),db: AsyncSession = Depends(get_async_db)):

    try:
        if sector_id:
            filter = {"sector_id":sector_id}
        else:
            filter = {}
        inddustry_sectors = await db.execute(select(Industry).filter_by(**filter))
        inddustry_sectors_result  =  inddustry_sectors.scalars().all()
        return inddustry_sectors_result
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)
    
@router.get("/industry/{industry_id}",response_model=IndustryMany,tags=["Industry"])
async def get_industry_sectors(industry_id:int,db: AsyncSession = Depends(get_async_db)):

    try:
        inddustry = await db.execute(select(Industry).where(Industry.id == industry_id))
        inddustry_result  =  inddustry.scalars().first()
        
        return inddustry_result
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)
    
@router.put("/industry/{industry_id}",response_model=IndustryResp,tags=["Industry"])
async def update_industry_sectors(industry_id:int,industry:IndustryBase,db: AsyncSession = Depends(get_async_db)):

    try:
        inddustry = await db.execute(select(Industry).filter(Industry.id == industry_id))
        inddustry_result  =  inddustry.scalars().first()
        inddustry_result.name = industry.name
        inddustry_result.sector_id = industry.sector_id
        inddustry_result.updated_at = datetime.utcnow
        await db.commit()
        await db.refresh(inddustry_result)
        return {"msg":"Industry updated successfully","industry":inddustry_result}
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)

@router.delete("/industry/{industry_id}",tags=["Industry"])
async def delete_industry_sectors(industry_id:int,db: AsyncSession = Depends(get_async_db)):

    try:
        inddustry = await db.execute(select(Industry).where(Industry.id == industry_id))
        inddustry_result  =  inddustry.scalars().first()
        inddustry_result.deleted_at = datetime.utcnow
        await db.commit()
        await db.refresh(inddustry_result)
        
        await db.commit()
        # await db.refresh(inddustry_sector_result)
        return {"msg":"industry deleted successfully"}
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)
    

@router.get("/years/", response_model=List[int],tags=["Years"])
async def get_years(start_year: Optional[int] = Query(None, description="Start year"),
                    end_year: Optional[int] = Query(None, description="End year")):
    if start_year is not None and end_year is not None:
        if start_year > end_year:
            raise HTTPException(status_code=400, detail="Start year must be less than or equal to end year")
        years = list(range(start_year, end_year + 1))
    else:
        years = list(range(1900, 2101))  # Default range if no start or end year is provided
    
    return years


class CategoryBase(BaseModel):
    name:str
    type: Optional[str] = None


class CategoryMany(CategoryBase):
    
    id: int
    created_at: Optional[datetime] = None
    created_by: Optional[uuid.UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[uuid.UUID] = None


class CategoryResp(BaseModel):
    msg:str
    category:CategoryMany



@router.post("/categories/",response_model=CategoryResp,tags=["Categories"])
async def create_category(
    name : str = Form(...),
    type: str = Form(...),
    db: AsyncSession = Depends(get_async_db)):

    try:
        category = Category(
            name = name,
            type = type
        )

        db.add(category)
        await db.commit()
        await db.refresh(category)

        return{
            "msg" : "Category created successfuly",
            "category": category
        }
    except:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500)


@router.get("/categories/",response_model=List[CategoryMany],tags=["Categories"])
async def get_categories(
    name:str = Query(None,description="Name of the category"),
    type:str = Query(None,description="Type of the category"),
    db: AsyncSession = Depends(get_async_db)):

    try:
        filters = {}

        if name:
            filters["name"] = name
        if type:
            filters["type"] = type
        
        categories = await db.execute(select(Category).filter_by(**filters))
        categories_result  =  categories.scalars().all()
        return categories_result
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)
    


@router.get("/categories/{category_id}",response_model=CategoryMany,tags=["Categories"])
async def get_categories(category_id:int,db: AsyncSession = Depends(get_async_db)):

    try:
        category = await db.execute(select(Category).where(Category.id == category_id))
        category_result  =  category.scalar_one_or_none()
        if category_result is None:
            raise HTTPException(
                status_code=404,
                detail="category not found"
            )
        return category_result
    except HTTPException as e:
        raise e
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)


@router.put("/categoies/{category_id}",response_model=CategoryResp,tags=["Categories"])
async def update_category(category_id:int,category:CategoryBase,db: AsyncSession = Depends(get_async_db)):

    try:
        category_db = await db.execute(select(Category).filter(Category.id == category_id))
        category_db_result  =  category_db.scalar_one_or_none()
        if category_db_result is None:
            raise HTTPException(
                status_code=404,
                detail="category not found"
            )
        category_db_result.name = category.name
        category_db_result.type = category.type
        category_db_result.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(category_db_result)
        return {"msg":"Category updated successfully","category":category_db_result}
    except HTTPException as e:
        raise e
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500)

@router.delete("/categoies/{category_id}",response_model=dict,tags=["Categories"])
async def update_category(category_id:int,db: AsyncSession = Depends(get_async_db)):

    try:
        category_db = await db.execute(select(Category).filter(Category.id == category_id))
        category_db_result  =  category_db.scalar_one_or_none()
        if category_db_result is None:
            raise HTTPException(
                status_code=404,
                detail="category not found"
            )
        category_db_result.deleted_at = datetime.utcnow()
        await db.commit()
        await db.refresh(category_db_result)
        return {"msg":"Category deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500)


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



class SubCategoryResp(BaseModel):
    msg:str
    sub_category:SubCategoryMany

@router.post("/sub-categories/",response_model=SubCategoryResp,tags=["Sub Categories"])
async def create_sub_category(
    name : str = Form(...),
    category_id: int = Form(...),
    db: AsyncSession = Depends(get_async_db)):

    try:
        sub_category = SubCategory(
            name = name,
            category_id = category_id
        )

        db.add(sub_category)
        await db.commit()
        await db.refresh(sub_category)

        return{
            "msg" : "Sub Category created successfuly",
            "sub_category": sub_category
        }
    except:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500)
    
@router.get("/sub-categories/",response_model=List[SubCategoryMany],tags=["Sub Categories"])
async def get_sub_categories(db: AsyncSession = Depends(get_async_db)):

    try:
        sub_categories = await db.execute(select(SubCategory))
        sub_categories_result  =  sub_categories.scalars().all()
        return sub_categories_result
    except:
        traceback.print_exc()
        raise HTTPException(status_code=500)


@router.get("/sub-categories/{sub_category_id}",response_model=SubCategoryMany,tags=["Sub Categories"])
async def get_sub_categories(sub_category_id:int,db: AsyncSession = Depends(get_async_db)):

    try:
        sub_category = await db.execute(select(SubCategory).where(SubCategory.id == sub_category_id))
        sub_category_result  =  sub_category.scalar_one_or_none()
        if sub_category_result is None:
            raise HTTPException(
                status_code=404,
                detail="sub category not found"
            )
        return sub_category_result
    except HTTPException as e:
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500)


@router.put("/sub-categoies/{sub_category_id}",response_model=SubCategoryResp,tags=["Sub Categories"])
async def update_sub_category(sub_category_id:int,category:SubCategoryBase,db: AsyncSession = Depends(get_async_db)):

    try:
        sub_category_db = await db.execute(select(SubCategory).filter(SubCategory.id == sub_category_id))
        sub_category_db_result  =  sub_category_db.scalar_one_or_none()
        if sub_category_db_result is None:
            raise HTTPException(
                status_code=404,
                detail="category not found"
            )
        sub_category_db_result.name = category.name
        sub_category_db_result.category_id = category.category_id
        sub_category_db_result.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(sub_category_db_result)
        return {"msg":"Sub category updated successfully","sub_category":sub_category_db_result}
    except HTTPException as e:
        raise e
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500)  


@router.delete("/sub-categoies/{sub_category_id}",response_model=dict,tags=["Sub Categories"])
async def sub_update_category(sub_category_id:int,db: AsyncSession = Depends(get_async_db)):

    try:
        sub_category_db = await db.execute(select(SubCategory).filter(SubCategory.id == sub_category_id))
        sub_category_db_result  =  sub_category_db.scalar_one_or_none()
        if sub_category_db_result is None:
            raise HTTPException(
                status_code=404,
                detail="category not found"
            )
        sub_category_db_result.deleted_at = datetime.utcnow()
        await db.commit()
        await db.refresh(sub_category_db_result)
        return {"msg":"sub category deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500)
    
@router.post("/gross-area/",response_model=schemas.GrossAreaResp,tags=["Gross Area"])
async def create_gross_area(
    area : int = Form(...),
    db: AsyncSession = Depends(get_async_db)):
    

    form_data = {
        "area":area
    }
    gross_area = await crud_gross_area.create(db=db, obj_in=form_data)
    return {
        "msg": "Gross area added successfully",
        "gross_area": gross_area
    }

@router.get("/gross-area/",response_model=List[schemas.GrossAreaRead],tags=["Gross Area"])
async def get_gross_areas(db: AsyncSession = Depends(get_async_db),
                         skip:int = Query(None, description="Number of records to skip"),
                         limit:int = Query(None, description="Number of records to retrieve")):


    return await crud_gross_area.get_multi(db=db,skip=skip,limit=limit)

@router.get("/gross-area/{gross_area_id}",response_model=schemas.GrossAreaRead,tags=["Gross Area"])
async def get_gross_area(gross_area_id:int,db: AsyncSession = Depends(get_async_db)):

    gross_area_db = await crud_gross_area.get(db=db,id=gross_area_id)
    return gross_area_db
    


@router.put("/gross-area/",response_model=schemas.GrossAreaResp,tags=["Gross Area"])
async def update_gross_area(gross_area_id:int, gross_area:schemas.GrossAreaBase, db: AsyncSession = Depends(get_async_db)):

    
    gross_area_db = await crud_gross_area.update(db=db,obj_in=gross_area,id=gross_area_id)
    return {
        "msg" : "Gross area updated successfully",
        "gross_area": gross_area_db
    }

    
@router.delete("/gross-area/{gross_area_id}",response_model=dict,tags=["Gross Area"])
async def delete_gross_area(gross_area_id:int,db: AsyncSession = Depends(get_async_db)):

    gross_area_db = await crud_gross_area.delete(db=db,id=gross_area_id)

    return {
        "msg": "gross area deleted successfully"
    }





    
@router.post("/unit/",response_model=schemas.UnitResp,tags=["Unit"])
async def create_gross_area_unit(
    name : str = Form(...),
    type: str = Form(...),
    db: AsyncSession = Depends(get_async_db)):
    

    form_data = {
        "name":name,
        "type":type
    }
    unit = await crud_unit.create(db=db, obj_in=form_data)
    return {
        "msg": "unit added successfully",
        "unit": unit
    }

@router.get("/unit/",response_model=List[schemas.UnitRead],tags=["Unit"])
async def get_gross_area_units(db: AsyncSession = Depends(get_async_db),
                        name : str = Query(None, description="Name of unit"),
                        type: str = Query(None, description="Type of Unit (Weght,Area etc)"),
                        skip:int = Query(None, description="Number of records to skip"),
                        limit:int = Query(None, description="Number of records to retrieve")):
    
    filters = {}

    if name:
        filters['name'] = name
    if type:
        filters['type'] = type


    return await crud_unit.get_multi_filters(db=db,filters=filters,skip=skip,limit=limit)

@router.get("/gross/{unit_id}",response_model=schemas.UnitRead,tags=["Unit"])
async def get_gross_area(unit_id:int,db: AsyncSession = Depends(get_async_db)):

    unit_db = await crud_unit.get(db=db,id=unit_id)
    return unit_db
    


@router.put("/unit/{unit_id}",response_model=schemas.UnitResp,tags=["Unit"])
async def update_gross_area(unit_id:int, gross_area:schemas.UnitBase, db: AsyncSession = Depends(get_async_db)):

    
    unit_db = await crud_unit.update(db=db,obj_in=gross_area,id=unit_id)
    return {
        "msg" : "Unit updated successfully",
        "unit": unit_db
    }

    
@router.delete("/unit/{unit_id}",response_model=dict,tags=["Unit"])
async def delete_gross_area(unit_id:int,db: AsyncSession = Depends(get_async_db)):

    unit_db = await crud_unit.delete(db=db,id=unit_id)

    return {
        "msg": "unit deleted successfully"
    }






# class CalculationMethodBase(BaseModel):
    
    
#     calculationmethod: str

# class CalculationMethod(CalculationMethodBase):
    
#     id: int

# class CalculationMethodResp(BaseModel):

#     notification: str
#     calculationmethod: CalculationMethod





    


# @router.post("/calculationmethod/",response_model=CalculationMethodResp,tags=["CalculationMethod"])
# async def create_calculationmethod(
#     salutation : str = Form(...),
#     db: AsyncSession = Depends(get_async_db)):

#     try:
#         calculationmethod_db = UserSalutation(
#             calculationmethod = calculationmethod 
#         )

#         db.add(calculationmethod_db)
#         await db.commit()
#         await db.refresh(calculationmethod_db)

#         return{
#             "notification" : "calculationmethod created successfuly",
#             "salutation": calculationmethod_db
#         }
#     except:
#         traceback.print_exc()
#         raise HTTPException(status_code=500)

# @router.get("/calculationmethod/",response_model=List[CalculationMethod],tags=["Salutations"])
# async def get_salutations(db: AsyncSession = Depends(get_async_db)):

#     try:
#         calculationmethod = await db.execute(select(UserSalutation))
#         calculationmethod_result  =  calculationmethod.scalars().all()
#         return calculationmethod_result
#     except:
#         traceback.print_exc()
#         raise HTTPException(status_code=500)

# @router.get("/calculationmethod/{calculationmethod_id}",response_model=Salutation,tags=["Salutations"])
# async def get_calculationmethod(calculationmethod_id:int,db: AsyncSession = Depends(get_async_db)):

#     calculationmethod = await db.execute(select(UserSalutation).filter(UserSalutation.id==calculationmethod_id))
#     calculationmethod_result  =  calculationmethod.scalars().first()
#     if calculationmethod_result:
#         return calculationmethod_result
#     raise HTTPException(status_code=404, detail="Salutation not found")



# @router.put("/calculationmethod/{calculationmethod_id}",response_model=SalutationResp,tags=["Salutations"])
# async def get_calculationmethod(salutation_id:int,salutation:SalutationBase,db: AsyncSession = Depends(get_async_db)):

#     try:
#         calculationmethod = await db.execute(select(UserSalutation).filter(UserSalutation.id == calculationmethod_id))
#         calculationmethod_result  =  calculationmethod.scalars().first()
#         calculationmethod_result.calculationmethod = calculationmethod.calculationmethod
#         await db.commit()
#         await db.refresh(calculationmethod_result)
#         return{
#             "notification" : "Salutation updated successfuly",
#             "salutation": calculationmethod_result
#         }
#     except:
#         traceback.print_exc()
#         raise HTTPException(status_code=500)

# @router.delete("/calculationmethod/{calculationmethod_id}", response_model=dict, tags=["Salutations"])
# async def delete_salutation(calculationmethod_id: int, db: AsyncSession = Depends(get_async_db)):
#     try:
#         result = await db.execute(select(UserSalutation).filter(UserSalutation.id == calculationmethod_id))
#         calculationmethod_result = result.scalars().first()
#         if calculationmethod_result is None:
#             raise HTTPException(status_code=404, detail="Calculation Method not found")
        
#         await db.delete(calculationmethod_result)
#         await db.commit()
        
#         return {"notification": "Salutation deleted successfully"}
#     except:
#         traceback.print_exc()
#         await db.rollback()
#         raise HTTPException(status_code=500, detail="Internal Server Error")