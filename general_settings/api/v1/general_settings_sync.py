from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List, Optional
from general_settings.db.models import GeneralCountries, GeneralCities, GeneralStates
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