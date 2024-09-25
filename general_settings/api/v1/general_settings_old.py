# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session, sessionmaker
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.future import select
# from datetime import datetime
# from typing import List, Optional
# from general_settings.db.models import GeneralCountries, GeneralCities, GeneralStates
# from pydantic import BaseModel
# from sqlalchemy.ext.declarative import declarative_base
# router = APIRouter()

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

# # Country models
# class CountryBase(BaseModel):
#     name: str
#     iso3: Optional[str] = None
#     numeric_code: Optional[str] = None
#     iso2: Optional[str] = None
#     phonecode: Optional[str] = None
#     capital: Optional[str] = None
#     currency: Optional[str] = None
#     currency_name: Optional[str] = None
#     currency_symbol: Optional[str] = None
#     tld: Optional[str] = None
#     native: Optional[str] = None
#     region: Optional[str] = None
#     region_id: Optional[int] = None
#     subregion: Optional[str] = None
#     subregion_id: Optional[int] = None
#     nationality: Optional[str] = None
#     latitude: Optional[float] = None
#     longitude: Optional[float] = None
#     emoji: Optional[str] = None
#     emojiU: Optional[str] = None

# class CountryCreate(CountryBase):
#     pass

# class Country(CountryBase):
#     id: int
#     created_at: Optional[datetime]
#     updated_at: datetime
#     flag: int

# # City models
# class CityBase(BaseModel):
#     name: str
#     state_id: int
#     state_code: str
#     country_id: int
#     country_code: str
#     latitude: float
#     longitude: float
#     wikiDataId: Optional[str] = None
#     createdAt: Optional[datetime] = None
#     createdBy: Optional[str] = None
#     updatedAt: Optional[datetime] = None
#     updatedBy: Optional[str] = None
#     deletedAt: Optional[datetime] = None
#     deletedBy: Optional[str] = None

# class CityCreate(CityBase):
#     pass

# class City(CityBase):
#     id: int
#     created_at: Optional[datetime]
#     updated_at: datetime
#     flag: int

# # State models
# class StateBase(BaseModel):
#     name: str
#     country_id: int
#     country_code: str
#     fips_code: Optional[str] = None
#     iso2: Optional[str] = None
#     type: Optional[str] = None
#     latitude: Optional[float] = None
#     longitude: Optional[float] = None
#     created_at: Optional[datetime] = None
#     updated_at: datetime
#     flag: int = 1
#     wikiDataId: Optional[str] = None
#     createdAt: Optional[datetime] = None
#     createdBy: Optional[str] = None
#     updatedAt: Optional[datetime] = None
#     updatedBy: Optional[str] = None
#     deletedAt: Optional[datetime] = None
#     deletedBy: Optional[str] = None

# class StateCreate(StateBase):
#     pass

# class State(StateBase):
#     id: int

# # # Country endpoints
# # @router.post("/countries/", response_model=Country, tags=["Country"])
# # async def create_country(country: CountryCreate, db: AsyncSession = Depends(get_async_db)):
# #     db_country = GeneralCountries(**country.dict(), created_at=datetime.utcnow())
# #     db.add(db_country)
# #     await db.commit()
# #     await db.refresh(db_country)
# #     return db_country

# @router.post("/countries/", response_model=Country, tags=["Country"])
# async def create_country(country: CountryCreate, db: AsyncSession = Depends(get_async_db)):
#     try:
#         db_country = GeneralCountries(**country.dict(), created_at=datetime.utcnow())
#         db.add(db_country)
#         await db.commit()
#         await db.refresh(db_country)
#         return db_country
#     except Exception as e:
#         await db.rollback()
#         raise HTTPException(status_code=500, detail=f"Failed to create country: {str(e)}")
    

# @router.get("/countries/", response_model=List[Country], tags=["Country"])
# async def read_countries(
#     skip: int = Query(0, description="Number of records to skip"),
#     limit: int = Query(10, description="Maximum number of records to retrieve"),
#     name: Optional[str] = Query(None, description="Name of the country"),
#     iso3: Optional[str] = Query(None, description="ISO3 code of the country"),
#     numeric_code: Optional[str] = Query(None, description="Numeric code of the country"),
#     iso2: Optional[str] = Query(None, description="ISO2 code of the country"),
#     phonecode: Optional[str] = Query(None, description="Phone code of the country e.g. 93"),
#     capital: Optional[str] = Query(None, description="Capital city of the country"),
#     currency: Optional[str] = Query(None, description="Currency code of the country"),
#     currency_name: Optional[str] = Query(None, description="Currency name of the country"),
#     currency_symbol: Optional[str] = Query(None, description="Currency symbol of the country e.g. ؋"),
#     tld: Optional[str] = Query(None, description="Top-level domain of the country e.g. .af"),
#     native: Optional[str] = Query(None, description="Native name of the country"),
#     region: Optional[str] = Query(None, description="Region of the country"),
#     region_id: Optional[int] = Query(None, description="Region ID of the country"),
#     subregion: Optional[str] = Query(None, description="Subregion of the country"),
#     subregion_id: Optional[int] = Query(None, description="Subregion ID of the country"),
#     nationality: Optional[str] = Query(None, description="Nationality of the country"),
#     latitude: Optional[float] = Query(None, description="Latitude of the country"),
#     longitude: Optional[float] = Query(None, description="Longitude of the country"),
#     db: AsyncSession = Depends(get_async_db)
# ):
#     filters = {}
#     if name:
#         filters['name'] = name
#     if iso3:
#         filters['iso3'] = iso3
#     if numeric_code:
#         filters['numeric_code'] = numeric_code
#     if iso2:
#         filters['iso2'] = iso2
#     if phonecode:
#         filters['phonecode'] = phonecode
#     if capital:
#         filters['capital'] = capital
#     if currency:
#         filters['currency'] = currency
#     if currency_name:
#         filters['currency_name'] = currency_name
#     if currency_symbol:
#         filters['currency_symbol'] = currency_symbol
#     if tld:
#         filters['tld'] = tld
#     if native:
#         filters['native'] = native
#     if region:
#         filters['region'] = region
#     if region_id:
#         filters['region_id'] = region_id
#     if subregion:
#         filters['subregion'] = subregion
#     if subregion_id:
#         filters['subregion_id'] = subregion_id
#     if nationality:
#         filters['nationality'] = nationality
#     if latitude:
#         filters['latitude'] = latitude
#     if longitude:
#         filters['longitude'] = longitude

#     stmt = select(GeneralCountries).filter_by(**filters).offset(skip).limit(limit)
#     countries = await db.execute(stmt)
#     return countries.scalars().all()

# # @router.get("/countries/{country_id}", response_model=Country, tags=["Country"])
# # async def read_country(country_id: int, db: AsyncSession = Depends(get_async_db)):
# #     country = await db.query(GeneralCountries).filter(GeneralCountries.id == country_id).first()
# #     if country is None:
# #         raise HTTPException(status_code=404, detail="Country not found")
# #     return country
# # @router.get("/countries/{country_id}", response_model=Country, tags=["Country"])
# # async def read_country(country_id: int):
# #     async with get_async_db() as session:
# #         statement = select(GeneralCountries).where(GeneralCountries.id == country_id)
# #         result = await session.execute(statement)
# #         country = result.scalars().first()
# #         return country
# @router.get("/countries/{country_id}", response_model=Country, tags=["Country"])
# async def read_country(country_id: int, db: AsyncSession = Depends(get_async_db)):
#     statement = select(GeneralCountries).where(GeneralCountries.id == country_id)
#     result = await db.execute(statement)
#     country = result.scalars().first()
#     if country is None:
#         raise HTTPException(status_code=404, detail="Country not found")
#     return country
# @router.put("/countries/{country_id}", response_model=Country, tags=["Country"])
# async def update_country(country_id: int, country: CountryCreate, db: AsyncSession = Depends(get_async_db)):
#     db_country = await db.query(GeneralCountries).filter(GeneralCountries.id == country_id).first()
#     if db_country:
#         for key, value in country.dict(exclude_unset=True).items():
#             setattr(db_country, key, value)
#         db_country.updated_at = datetime.utcnow()
#         await db.commit()
#         await db.refresh(db_country)
#         return db_country
#     raise HTTPException(status_code=404, detail="Country not found")

# @router.delete("/countries/{country_id}", response_model=dict, tags=["Country"])
# async def delete_country(country_id: int, db: AsyncSession = Depends(get_async_db)):
#     country = await db.query(GeneralCountries).filter(GeneralCountries.id == country_id).first()
#     if country:
#         db.delete(country)
#         await db.commit()
#         return {"message": "Country deleted successfully"}
#     raise HTTPException(status_code=404, detail="Country not found")

# # City endpoints
# @router.post("/cities/", response_model=City, tags=["City"])
# async def create_city(city: CityCreate, db: AsyncSession = Depends(get_async_db)):
#     db_city = GeneralCities(**city.dict(), created_at=datetime.utcnow())
#     db.add(db_city)
#     await db.commit()
#     await db.refresh(db_city)
#     return db_city

# @router.get("/cities/", response_model=List[City], tags=["City"])
# async def read_cities(
#     skip: int = Query(0, description="Number of records to skip"),
#     limit: int = Query(10, description="Maximum number of records to retrieve"),
#     name: Optional[str] = Query(None, description="Name of the city"),
#     state_id: Optional[int] = Query(None, description="ID of the state to filter by"),
#     state_code: Optional[str] = Query(None, description="Code of the state to filter by"),
#     country_id: Optional[int] = Query(None, description="ID of the country to filter by"),
#     country_code: Optional[str] = Query(None, description="Code of the country to filter by"),
#     latitude: Optional[float] = Query(None, description="Latitude of the city"),
#     longitude: Optional[float] = Query(None, description="Longitude of the city"),
#     db: AsyncSession = Depends(get_async_db)
# ):
#     filters = {}
#     if name:
#         filters['name'] = name
#     if state_id:
#         filters['state_id'] = state_id
#     if state_code:
#         filters['state_code'] = state_code
#     if country_id:
#         filters['country_id'] = country_id
#     if country_code:
#         filters['country_code'] = country_code
#     if latitude:
#         filters['latitude'] = latitude
#     if longitude:
#         filters['longitude'] = longitude

#     stmt = select(GeneralCities).filter_by(**filters).offset(skip).limit(limit)
#     cities = await db.execute(stmt)
#     return cities.scalars().all()

# @router.get("/cities/{city_id}", response_model=City, tags=["City"])
# async def read_city(city_id: int, db: AsyncSession = Depends(get_async_db)):
#     city = await db.query(GeneralCities).filter(GeneralCities.id == city_id).first()
#     if city is None:
#         raise HTTPException(status_code=404, detail="City not found")
#     return city

# @router.put("/cities/{city_id}", response_model=City, tags=["City"])
# async def update_city(city_id: int, city: CityCreate, db: AsyncSession = Depends(get_async_db)):
#     db_city = await db.query(GeneralCities).filter(GeneralCities.id == city_id).first()
#     if db_city:
#         for key, value in city.dict(exclude_unset=True).items():
#             setattr(db_city, key, value)
#         db_city.updated_at = datetime.utcnow()
#         await db.commit()
#         await db.refresh(db_city)
#         return db_city
#     raise HTTPException(status_code=404, detail="City not found")

# @router.delete("/cities/{city_id}", response_model=dict, tags=["City"])
# async def delete_city(city_id: int, db: AsyncSession = Depends(get_async_db)):
#     city = await db.query(GeneralCities).filter(GeneralCities.id == city_id).first()
#     if city:
#         db.delete(city)
#         await db.commit()
#         return {"message": "City deleted successfully"}
#     raise HTTPException(status_code=404, detail="City not found")

# # State endpoints
# @router.post("/states/", response_model=State, tags=["State"])
# async def create_state(state: StateCreate, db: AsyncSession = Depends(get_async_db)):
#     db_state = GeneralStates(**state.dict(), created_at=datetime.utcnow())
#     db.add(db_state)
#     await db.commit()
#     await db.refresh(db_state)
#     return db_state

# @router.get("/states/", response_model=List[State], tags=["State"])
# async def read_states(
#     skip: int = Query(0, description="Number of records to skip"),
#     limit: int = Query(10, description="Maximum number of records to retrieve"),
#     name: Optional[str] = Query(None, description="Name of the state"),
#     country_id: Optional[int] = Query(None, description="ID of the country to filter by"),
#     country_code: Optional[str] = Query(None, description="Code of the country to filter by"),
#     fips_code: Optional[str] = Query(None, description="FIPS code of the state"),
#     iso2: Optional[str] = Query(None, description="ISO2 code of the state"),
#     type: Optional[str] = Query(None, description="Type of the state"),
#     latitude: Optional[float] = Query(None, description="Latitude of the state"),
#     longitude: Optional[float] = Query(None, description="Longitude of the state"),
#     db: AsyncSession = Depends(get_async_db)
# ):
#     filters = {}
#     if name:
#         filters['name'] = name
#     if country_id:
#         filters['country_id'] = country_id
#     if country_code:
#         filters['country_code'] = country_code
#     if fips_code:
#         filters['fips_code'] = fips_code
#     if iso2:
#         filters['iso2'] = iso2
#     if type:
#         filters['type'] = type
#     if latitude:
#         filters['latitude'] = latitude
#     if longitude:
#         filters['longitude'] = longitude

#     stmt = select(GeneralStates).filter_by(**filters).offset(skip).limit(limit)
#     states = await db.execute(stmt)
#     return states.scalars().all()

# @router.get("/states/{state_id}", response_model=State, tags=["State"])
# async def read_state(state_id: int, db: AsyncSession = Depends(get_async_db)):
#     state = await db.query(GeneralStates).filter(GeneralStates.id == state_id).first()
#     if state is None:
#         raise HTTPException(status_code=404, detail="State not found")
#     return state

# @router.put("/states/{state_id}", response_model=State, tags=["State"])
# async def update_state(state_id: int, state: StateCreate, db: AsyncSession = Depends(get_async_db)):
#     db_state = await db.query(GeneralStates).filter(GeneralStates.id == state_id).first()
#     if db_state:
#         for key, value in state.dict(exclude_unset=True).items():
#             setattr(db_state, key, value)
#         db_state.updated_at = datetime.utcnow()
#         await db.commit()
#         await db.refresh(db_state)
#         return db_state
#     raise HTTPException(status_code=404, detail="State not found")

# @router.delete("/states/{state_id}", response_model=dict, tags=["State"])
# async def delete_state(state_id: int, db: AsyncSession = Depends(get_async_db)):
#     state = await db.query(GeneralStates).filter(GeneralStates.id == state_id).first()
#     if state:
#         db.delete(state)
#         await db.commit()
#         return {"message": "State deleted successfully"}
#     raise HTTPException(status_code=404, detail="State not found")



import uuid
from fastapi import APIRouter, Depends, Form, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List, Optional
from general_settings.db.models import GeneralCountries, GeneralCities, GeneralStates, Users, UserBusinessDetails,UserBankAccountInformation
from general_settings.dependencies import get_db#, get_async_db
from pydantic import BaseModel  # Ensure this line is added
router = APIRouter()

# Synchronous endpoints for countries
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
    region_id: Optional[int] = None
    subregion: Optional[str] = None
    subregion_id: Optional[int] = None
    nationality: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    emoji: Optional[str] = None
    emojiU: Optional[str] = None

class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    id: int
    created_at: Optional[datetime]
    updated_at: datetime
    flag: int

@router.post("/countries/", response_model=Country, tags=["Country"])
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    db_country = GeneralCountries(**country.dict(), created_at=datetime.utcnow())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

@router.get("/countries/", response_model=List[Country], tags=["Country"])
def read_countries(
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
    db: Session = Depends(get_db)
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

    countries = db.query(GeneralCountries).filter_by(**filters).offset(skip).limit(limit).all()
    return countries

@router.get("/countries/{country_id}", response_model=Country, tags=["Country"])
def read_country(country_id: int, db: Session = Depends(get_db)):
    country = db.query(GeneralCountries).filter(GeneralCountries.id == country_id).first()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@router.put("/countries/{country_id}", response_model=Country, tags=["Country"])
def update_country(country_id: int, country: CountryCreate, db: Session = Depends(get_db)):
    db_country = db.query(GeneralCountries).filter(GeneralCountries.id == country_id).first()
    if db_country:
        for key, value in country.dict(exclude_unset=True).items():
            setattr(db_country, key, value)
        db_country.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_country)
        return db_country
    raise HTTPException(status_code=404, detail="Country not found")

@router.delete("/countries/{country_id}", response_model=dict, tags=["Country"])
def delete_country(country_id: int, db: Session = Depends(get_db)):
    country = db.query(GeneralCountries).filter(GeneralCountries.id == country_id).first()
    if country:
        db.delete(country)
        db.commit()
        return {"message": "Country deleted successfully"}
    raise HTTPException(status_code=404, detail="Country not found")

# Asynchronous endpoints for cities
class CityBase(BaseModel):
    name: str
    state_id: int
    state_code: str
    country_id: int
    country_code: str
    latitude: float
    longitude: float
    wikiDataId: Optional[str] = None
    createdAt: Optional[datetime] = None
    createdBy: Optional[str] = None
    updatedAt: Optional[datetime] = None
    updatedBy: Optional[str] = None
    deletedAt: Optional[datetime] = None
    deletedBy: Optional[str] = None

class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int
    created_at: Optional[datetime]
    updated_at: datetime
    flag: int

@router.post("/cities/", response_model=City, tags=["City"])
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    db_city = GeneralCities(**city.dict(), created_at=datetime.utcnow())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

@router.get("/cities/", response_model=List[City], tags=["City"])
def read_cities(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to retrieve"),
    name: Optional[str] = Query(None, description="Name of the city"),
    state_code: Optional[str] = Query(None, description="State code of the city"),
    country_code: Optional[str] = Query(None, description="Country code of the city"),
    db: Session = Depends(get_db)
):
    filters = {}
    if name:
        filters['name'] = name
    if state_code:
        filters['state_code'] = state_code
    if country_code:
        filters['country_code'] = country_code

    cities = db.query(GeneralCities).filter_by(**filters).offset(skip).limit(limit).all()
    return cities

@router.get("/cities/{city_id}", response_model=City, tags=["City"])
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(GeneralCities).filter(GeneralCities.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.put("/cities/{city_id}", response_model=City, tags=["City"])
def update_city(city_id: int, city: CityCreate, db: Session = Depends(get_db)):
    db_city = db.query(GeneralCities).filter(GeneralCities.id == city_id).first()
    if db_city:
        for key, value in city.dict(exclude_unset=True).items():
            setattr(db_city, key, value)
        db_city.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_city)
        return db_city
    raise HTTPException(status_code=404, detail="City not found")

@router.delete("/cities/{city_id}", response_model=dict, tags=["City"])
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(GeneralCities).filter(GeneralCities.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
        return {"message": "City deleted successfully"}
    raise HTTPException(status_code=404, detail="City not found")

######################################################################

class StateBase(BaseModel):
    name: str
    country_id: int
    country_code: str
    fips_code: Optional[str] = None
    iso2: Optional[str] = None
    type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: datetime
    flag: int = 1
    wikiDataId: Optional[str] = None
    createdAt: Optional[datetime] = None
    createdBy: Optional[str] = None
    updatedAt: Optional[datetime] = None
    updatedBy: Optional[str] = None
    deletedAt: Optional[datetime] = None
    deletedBy: Optional[str] = None

class StateCreate(StateBase):
    pass

class State(StateBase):
    id: int

@router.post("/states/", response_model=State, tags=["State"])
def create_state(state: StateCreate, db: Session = Depends(get_db)):
    db_state = GeneralStates(**state.dict(), created_at=datetime.utcnow())
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    return db_state

@router.get("/states/", response_model=List[State], tags=["State"])
def read_states(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to retrieve"),
    country_id: int = Query(None, description="ID of the country to filter states"),
    country_code: str = Query(None, description="Code of the country to filter states"),
    db: Session = Depends(get_db)
):
    filters = {}
    if country_id:
        filters['country_id'] = country_id
    if country_code:
        filters['country_code'] = country_code

    states = db.query(GeneralStates).filter_by(**filters).offset(skip).limit(limit).all()
    return states

@router.get("/states/{state_id}", response_model=State, tags=["State"])
def read_state(state_id: int, db: Session = Depends(get_db)):
    state = db.query(GeneralStates).filter(GeneralStates.id == state_id).first()
    if state is None:
        raise HTTPException(status_code=404, detail="State not found")
    return state

@router.put("/states/{state_id}", response_model=State, tags=["State"])
def update_state(state_id: int, state: StateCreate, db: Session = Depends(get_db)):
    db_state = db.query(GeneralStates).filter(GeneralStates.id == state_id).first()
    if db_state:
        for key, value in state.dict(exclude_unset=True).items():
            setattr(db_state, key, value)
        db_state.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_state)
        return db_state
    raise HTTPException(status_code=404, detail="State not found")

@router.delete("/states/{state_id}", response_model=dict, tags=["State"])
def delete_state(state_id: int, db: Session = Depends(get_db)):
    db_state = db.query(GeneralStates).filter(GeneralStates.id == state_id).first()
    if db_state:
        db.delete(db_state)
        db.commit()
        return {"message": "State deleted successfully"}
    raise HTTPException(status_code=404, detail="State not found")



# Pydantic models
class UserBase(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    companyName: Optional[str] = None
    companyEmail: Optional[str] = None
    country_id: Optional[int] = None
    state_id: Optional[int] = None
    city_id: Optional[int] = None
    password: str
    userTypeId: uuid.UUID
    isReset: Optional[bool] = False
    ipAddress: Optional[str] = None
    thirdPartySubscriptionId: Optional[str] = None
    status: Optional[int] = 4
    remarks: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
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


# @router.post("/users/", response_model=User, tags=["User"])
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = Users(**user.dict(), createdAt=datetime.utcnow())
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @router.get("/users/", response_model=List[User], tags=["User"])
# def read_users(
#     skip: int = Query(0, description="Number of records to skip"),
#     limit: int = Query(10, description="Maximum number of records to retrieve"),
#     username: Optional[str] = Query(None, description="Filter by username"),
#     email: Optional[str] = Query(None, description="Filter by email"),
#     db: Session = Depends(get_db)
# ):
#     query = db.query(Users)

#     if username:
#         query = query.filter(Users.firstName == username)
#     if email:
#         query = query.filter(Users.email == email)
#     if email:
#         query = query.filter(Users.email == email)    

#     users = query.offset(skip).limit(limit).all()
#     return users

@router.get("/users/", response_model=List[User], tags=["User"])
def read_users(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to retrieve"),
    firstName: Optional[str] = Query(None, description="Filter by first name"),
    lastName: Optional[str] = Query(None, description="Filter by last name"),
    companyName: Optional[str] = Query(None, description="Filter by company name"),
    companyEmail: Optional[str] = Query(None, description="Filter by company email"),
    country_id: Optional[int] = Query(None, description="Filter by country ID"),
    state_id: Optional[int] = Query(None, description="Filter by state ID"),
    city_id: Optional[int] = Query(None, description="Filter by city ID"),
    userTypeId: Optional[uuid.UUID] = Query(None, description="Filter by user type ID"),
    isReset: Optional[bool] = Query(None, description="Filter by reset status"),
    ipAddress: Optional[str] = Query(None, description="Filter by IP address"),
    thirdPartySubscriptionId: Optional[str] = Query(None, description="Filter by third-party subscription ID"),
    status: Optional[int] = Query(None, description="Filter by status"),
    remarks: Optional[str] = Query(None, description="Filter by remarks"),
    db: Session = Depends(get_db)
):
    query = db.query(Users)

    if firstName:
        query = query.filter(Users.firstName == firstName)
    if lastName:
        query = query.filter(Users.lastName == lastName)
    if companyName:
        query = query.filter(Users.companyName == companyName)
    if companyEmail:
        query = query.filter(Users.companyEmail == companyEmail)
    if country_id:
        query = query.filter(Users.country_id == country_id)
    if state_id:
        query = query.filter(Users.state_id == state_id)
    if city_id:
        query = query.filter(Users.city_id == city_id)
    if userTypeId:
        query = query.filter(Users.userTypeId == userTypeId)
    if isReset is not None:
        query = query.filter(Users.isReset == isReset)
    if ipAddress:
        query = query.filter(Users.ipAddress == ipAddress)
    if thirdPartySubscriptionId:
        query = query.filter(Users.thirdPartySubscriptionId == thirdPartySubscriptionId)
    if status is not None:
        query = query.filter(Users.status == status)
    if remarks:
        query = query.filter(Users.remarks == remarks)

    users = query.offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=User, tags=["User"])
def read_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=User, tags=["User"])
def update_user(user_id: uuid.UUID, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db_user.updatedAt = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
        return db_user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}", response_model=dict, tags=["User"])
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user:
        # db.delete(user)
        user.status = 3  # Update user status to 3 (inactive)
        db.commit()
        return {"message": "User deleted (Status updated to 3)successfully"}
    raise HTTPException(status_code=404, detail="User not found")


class UserBankAccountInfoBase(BaseModel):
    userId: uuid.UUID
    bankName: Optional[str] = None
    bankBranch: Optional[str] = None
    accountName: Optional[str] = None
    accountNumber: Optional[str] = None
    swiftCode: Optional[str] = None
    iban: Optional[                         str] = None
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


@router.post("/user_bank_accounts/", response_model=UserBankAccountInfo, tags=["User Bank Account Info"])
def create_user_bank_account_info(user_bank_account_info: UserBankAccountInfoCreate, db: Session = Depends(get_db)):
    db_user_bank_account_info = UserBankAccountInformation(**user_bank_account_info.dict())
    db.add(db_user_bank_account_info)
    db.commit()
    db.refresh(db_user_bank_account_info)
    return db_user_bank_account_info

@router.get("/user_bank_accounts/", response_model=list[UserBankAccountInfo], tags=["User Bank Account Info"])
def read_user_bank_account_infos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(UserBankAccountInformation).offset(skip).limit(limit).all()

@router.get("/user_bank_accounts/{user_bank_account_info_id}", response_model=UserBankAccountInfo, tags=["User Bank Account Info"])
def read_user_bank_account_info(user_bank_account_info_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user_bank_account_info = db.query(UserBankAccountInformation).filter(UserBankAccountInformation.id == user_bank_account_info_id).first()
    if db_user_bank_account_info is None:
        raise HTTPException(status_code=404, detail="User bank account information not found")
    return db_user_bank_account_info

@router.put("/user_bank_accounts/{user_bank_account_info_id}", response_model=UserBankAccountInfo, tags=["User Bank Account Info"])
def update_user_bank_account_info(user_bank_account_info_id: uuid.UUID, user_bank_account_info: UserBankAccountInfoCreate, db: Session = Depends(get_db)):
    db_user_bank_account_info = db.query(UserBankAccountInformation).filter(UserBankAccountInformation.id == user_bank_account_info_id).first()
    if db_user_bank_account_info is None:
        raise HTTPException(status_code=404, detail="User bank account information not found")
    for key, value in user_bank_account_info.dict(exclude_unset=True).items():
        setattr(db_user_bank_account_info, key, value)
    db.add(db_user_bank_account_info)
    db.commit()
    db.refresh(db_user_bank_account_info)
    return db_user_bank_account_info

@router.delete("/user_bank_accounts/{user_bank_account_info_id}", response_model=UserBankAccountInfo, tags=["User Bank Account Info"])
def delete_user_bank_account_info(user_bank_account_info_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user_bank_account_info = db.query(UserBankAccountInformation).filter(UserBankAccountInformation.id == user_bank_account_info_id).first()
    if db_user_bank_account_info is None:
        raise HTTPException(status_code=404, detail="User bank account information not found")
    db.delete(db_user_bank_account_info)
    db.commit()
    return db_user_bank_account_info        

@router.post("/change-user-status/")
async def change_user_status(
    user_id: uuid.UUID = Form(...),
    status: int = Form(...,description="The status of the user (1: Active, 2: Inactive, 3: Delete, 4: Pending Signup/Incomplete, 5: Signup Rejected, 6: Pending Profle/Under Review, 7: Pending for Approval, 8: Rejected Profile, 9: Subscription Pending, 10: Subscription Cancelled)"),
    remarks: str = Form(...),
    db: AsyncSession = Depends(get_db)):

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
    