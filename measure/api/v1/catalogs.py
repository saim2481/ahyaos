import csv
import io
from datetime import datetime,timezone
import traceback
from typing import List,Optional
import uuid
from sqlalchemy import Select, select
from measure.services.auth_service import get_current_user
from general_settings.db.models import GeneralCities, GeneralStates, SubCategory
from measure.dependencies import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, File, HTTPException, Query, Form, UploadFile, status
from measure.schemas import schemas
from measure.db import models
from measure.db.crud.crude_gross_area import crud_user_company_assignment,crud_customer,crud_supplier,crud_product,crud_equipment_type,crud_facilities,crud_financed_entities
from measure.services.utils import generalized_bulk_upload

router = APIRouter(tags=['Catalogs'], prefix='/api/v1/catalogs')

@router.post("/locations-bulk/", response_model=schemas.LocationRespBulk)
async def bulk_upload_locations(
        file: UploadFile = File(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    try:


        # Process the CSV file
        locations = []
        content = await file.read()
        content_str = content.decode('utf-8-sig')  # Handle BOM by using 'utf-8-sig'
        csv_file = io.StringIO(content_str)
        reader = csv.DictReader(csv_file)

        # Extract unique country, state, and city names from the CSV
        country_names = set()
        state_names = set()
        city_names = set()

        for row in reader:
            country_names.add(row['country_name'])
            state_names.add(row['state_name'])
            city_names.add(row['city_name'])

        # Rewind the CSV file to re-read it
        csv_file.seek(0)
        reader = csv.DictReader(csv_file)

        # Fetch relevant data from the database
        countries_result = await db.execute(select(models.GeneralCountries).filter(models.GeneralCountries.name.in_(country_names)))
        states_result = await db.execute(select(models.GeneralStates).filter(models.GeneralStates.name.in_(state_names)))
        cities_result = await db.execute(select(models.GeneralCities).filter(models.GeneralCities.name.in_(city_names)))

        countries = countries_result.scalars().all()
        states = states_result.scalars().all()
        cities = cities_result.scalars().all()

        # Create dictionaries for easy lookup
        country_state_map = {
            country.id: {state.name: state.id for state in states if state.country_id == country.id}
            for country in countries
        }
        state_city_map = {
            state.id: {city.name: city.id for city in cities if city.state_id == state.id}
            for state in states
        }

        print(country_state_map,state_city_map)
        # content = await file.read()
        # content_str = content.decode('utf-8-sig')
        # csv_file = io.StringIO(content_str)
        # reader = csv.DictReader(csv_file)
        # print(reader.fieldnames)

        for row in reader:
            country_name = row['country_name']
            state_name = row['state_name']
            city_name = row['city_name']

            # Validate country, state, and city names
            country_id = next((country.id for country in countries if country.name == country_name), None)
            state_id = country_state_map.get(country_id, {}).get(state_name)
            city_id = state_city_map.get(state_id, {}).get(city_name)

            if not country_id or not state_id or not city_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid country/state/city names: {row['country_name']}/{row['state_name']}/{row['city_name']}"
                )

            # Create the location object
            location = models.CatalogsLocation(
                name=row['name'],
                address=row['address'],
                aptsuite=row['apt_or_suite'],
                country_id=country_id,
                state_id=state_id,
                city_id=city_id,
                zip_code=row['zip_code'],
                description=row['description'],
                created_by = user_id
            )
            locations.append(location)
        
        # Bulk insert locations
        db.add_all(locations)
        await db.commit()
        
        # Refresh and return the locations
        for location in locations:
            await db.refresh(location)
        locations
        
        return {"msg": "location saved successfully", "locations": locations}
    
    except HTTPException as e:
        await db.rollback()
        raise e
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error saving locations"
        )




        
@router.post("/location/", response_model=schemas.LocationResp)
async def create_location(
        name: str = Form(...),
        address: str = Form(...),
        aptsuite: str = Form(...),
        country_id: int = Form(...),
        state_id: int = Form(...),
        city_id: int = Form(...),
        zip_code: str = Form(...),
        description: str = Form(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):

    try:

        state = await (db.execute(select(GeneralStates).where(GeneralStates.id == state_id)))
        state_result = state.scalar_one_or_none()

        city = await (db.execute(select(GeneralCities).where(GeneralCities.id == city_id)))
        city_reult = city.scalar_one_or_none()

        if (state_result.country_id != country_id) or (city_reult.state_id != state_id):
            raise HTTPException(
                status_code=400,
                detail= "Country,state and city does not match"
            )

        location = models.CatalogsLocation(
            name=name,
            address=address,
            aptsuite=aptsuite,
            country_id=country_id,
            state_id=state_id,
            city_id=city_id,
            zip_code=zip_code,
            description=description,
            created_by = user_id
        )
        db.add(location)
        await db.commit()
        await db.refresh(location)
        return {
            "msg": "location saved successfully",
            "location": location
        }
    except HTTPException as e:
        await db.rollback()
        raise e
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error saving location"
        )

@router.get("/location/", response_model=List[schemas.LocationRead])
async def get_locations(
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(10, description="Maximum number of records to retrieve"),
        name: Optional[str] = Query(None,description="name of the location"),
        address: Optional[str] = Query(None,description="address of the location"),
        aptsuit: Optional[str] = Query(None,description="APT/Suite"),
        counry_id: Optional[int] = Query(None,description="Country in which the location is"),
        state_id: Optional[int] = Query(None,description="State in which the location is"),
        city_id: Optional[int] = Query(None,description="City in which the location is"),
        zip_code: Optional[str] = Query(None,description="ZIP code of the location"),
        description: Optional[str] = Query(None,description="description of the location"),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):

    try:
        filters = {}
        if name:
            filters['name'] = name
        if address:
            filters['address'] = address
        if aptsuit:
            filters['aptsuite'] = aptsuit
        if counry_id:
            filters['country_id'] = counry_id
        if state_id:
            filters['state_id'] = state_id
        if city_id:
            filters['city_id'] = city_id
        if zip_code:
            filters['zip_code'] = zip_code
        if description:
            filters['description'] = description
        locations_query = await db.execute(select(models.CatalogsLocation).filter_by(**filters).offset(skip).limit(limit).order_by(models.CatalogsLocation.id))
        locations_results = locations_query.scalars().all()
        return locations_results
    except HTTPException as e:
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error getting locations"
        )
    
@router.get("/location/{location_id}", response_model=schemas.LocationRead)
async def get_location(location_id:str,user_id:uuid.UUID = Depends(get_current_user),db: AsyncSession = Depends(get_async_db)):

    try:
        
        locations_query = await db.execute(select(models.CatalogsLocation).where(models.CatalogsLocation.id == location_id))
        locations_results = locations_query.scalar_one_or_none()
        if locations_results is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="location not found"
            )
        return locations_results
    except HTTPException as e:
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error getting locations"
        )
    
@router.put("/location/{location_id}", response_model=schemas.LocationResp)
async def update_location(location_id:str,location:schemas.LocationBase,user_id:uuid.UUID = Depends(get_current_user),db: AsyncSession = Depends(get_async_db)):

    try:
        
        locations_query = await db.execute(select(models.CatalogsLocation).where(models.CatalogsLocation.id == location_id))
        location_result = locations_query.scalar_one_or_none()
        if location_result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="location not found"
            )
        for key, value in location.model_dump(exclude_unset=True).items():
            setattr(location_result, key, value)
        location_result.updated_at = datetime.utcnow()
        location_result.updated_by = user_id
        await db.commit()
        await db.refresh(location_result)
        return {
            "msg" : "location updated successfully",
            "location": location_result
        }
    except HTTPException as e:
        await db.rollback()
        raise e
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error updating locations"
        )
    
@router.delete("/location/{location_id}", response_model=schemas.LocationResp)
async def update_location(location_id:str,user_id:uuid.UUID = Depends(get_current_user),db: AsyncSession = Depends(get_async_db)):

    try:
        
        locations_query = await db.execute(select(models.CatalogsLocation).where(models.CatalogsLocation.id == location_id))
        location_result = locations_query.scalar_one_or_none()
        if location_result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="location not found"
            )
        location_result.deleted_at = datetime.utcnow()
        location_result.deleted_by = user_id
        await db.commit()
        await db.refresh(location_result)
        return {
            "msg" : "location deleted successfully",
            "location": location_result
        }
    except HTTPException as e:
        await db.rollback()
        raise e
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error deleting locations"
        )

@router.post('/facilities/',response_model=schemas.FacilitiesResp)
async def create_facility(
        name:str = Form(...),
        category_id:int = Form(...),
        sub_category_id:int = Form(...),
        location_id:uuid.UUID = Form(...),
        internal_id:str = Form(...),
        description:str = Form(...),
        refrigrant_remaining_at_disposal:float = Form(...),
        gross_area_id:int = Form(...),
        gross_area_unit_id:int = Form(...),
        occupancy:float = Form(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):

    data = {
        "name":name,
        "category_id":category_id,
        "sub_category_id":sub_category_id,
        "location_id":location_id,
        "internal_id":internal_id,
        "description":description,
        "refrigrant_remaining_at_disposal":refrigrant_remaining_at_disposal,
        "gross_area_id":gross_area_id,
        "gross_area_unit_id":gross_area_unit_id,
        "occupancy":occupancy,
        "created_at": user_id
    }   

    sub_category = await (db.execute(select(SubCategory).where(SubCategory.id == sub_category_id)))
    sub_category_result = sub_category.scalar_one_or_none()
    
    if sub_category_result.category_id != category_id:
        raise HTTPException(
            status_code=400,
            detail= "category and subcategory does not match"
        )

    facility = await crud_facilities.create(db=db,obj_in=data)

    return{
        "msg": "facility added successfully",
        "facility": facility
    }

@router.get("/facilities/", response_model=List[schemas.FacilitiesRead])
async def get_facilities(
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(10, description="Maximum number of records to retrieve"),
        name: Optional[str] = Query(None,description="Name of the facility"),
        category_id: Optional[int] = Query(None,description="Category of facility"),
        sub_category_id: Optional[int] = Query(None,description="Category of facility"),
        location_id: Optional[uuid.UUID] = Query(None,description="Location of facility"),
        internal_id: Optional[str] = Query(None,description="Internal ID of facility"),
        description: Optional[str] = Query(None,description="Description of facility"),
        refrigrant_remaining_at_disposal: Optional[float] = Query(None,description="Refrigrant remaining at disposal at facility"),
        gross_area_id: Optional[int] = Query(None,description="Gross area of the facility"),
        gross_area_unit_id: Optional[int] = Query(None,description="Gross area unit of the facility"),
        occupancy: Optional[float] = Query(None,description="Occupancy of the facility"),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    filters = {}
    if name:
        filters['name'] = name
    if category_id:
        filters['category_id'] = category_id
    if sub_category_id:
        filters["sub_category_id"] = sub_category_id
    if location_id:
        filters['location_id'] = location_id
    if internal_id:
        filters['internal_id'] = internal_id
    if refrigrant_remaining_at_disposal:
        filters['refrigrant_remaining_at_disposal'] = refrigrant_remaining_at_disposal
    if gross_area_id:
        filters['gross_area_id'] = gross_area_id
    if description:
        filters['description'] = description
    if gross_area_unit_id:
        filters['gross_area_unit_id'] = gross_area_unit_id
    if occupancy:
        filters['occupancy'] = occupancy


    facilities = await crud_facilities.get_multi_filters(db=db,filters=filters,skip=skip,limit=limit)

    return facilities
    

@router.get("/facilities/{facility_id}", response_model=schemas.FacilitiesRead)
async def get_facility(
        facility_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    facility = await crud_facilities.get(db=db,id=facility_id)

    return facility

@router.put("/facilities/{facility_id}", response_model=schemas.FacilitiesResp)
async def update_facility(
        facility_id:uuid.UUID,
        facility: schemas.FacilitiesCreate,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    facility_db = await crud_facilities.update(db=db,obj_in=facility,id=facility_id,user_id=user_id)

    return {
        "msg" : "Facility updated successfully",
        "facility": facility_db
    }



@router.delete("/facilities/{facility_id}", response_model=dict)
async def delete_facility(
        facility_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    facility_db = await crud_facilities.delete(db=db,id=facility_id,user_id=user_id)

    return {
        "msg" : "Facility deleted successfully",
    }


@router.post("/facilities-bulk/", response_model=schemas.FacilitiesRespBulk)
async def bulk_upload_facilities(
        file: UploadFile = File(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    try:
        # Read and process CSV file
        content = await file.read()
        content_str = content.decode('utf-8-sig')  # Handle BOM by using 'utf-8-sig'
        csv_file = io.StringIO(content_str)
        reader = csv.DictReader(csv_file)

        # Extract unique names for lookup
        category_names = set()
        subcategory_names = set()
        location_names = set()
        gross_area_names = set()
        gross_area_unit_names = set()

        for idx,row in enumerate(reader,start=1):
            category_names.add(row['category_name'])
            subcategory_names.add(row['subcategory_name'])
            location_names.add(row['location_name'])
            try:
                # Convert gross_area to int and handle errors
                gross_area_names.add(int(row['gross_area']))  # Attempt to convert gross_area to integer
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid gross_area value at row {idx}: '{row['gross_area']}' is not a valid integer"
                )
            gross_area_unit_names.add(row['gross_area_unit_name'])

        # Rewind the CSV file to re-read it
        csv_file.seek(0)
        reader = csv.DictReader(csv_file)

        # Fetch relevant data from the database
        categories_result = await db.execute(
            select(models.Category).filter(models.Category.name.in_(category_names))
        )
        subcategories_result = await db.execute(
            select(models.SubCategory).filter(models.SubCategory.name.in_(subcategory_names))
        )
        locations_result = await db.execute(
            select(models.CatalogsLocation).filter(models.CatalogsLocation.name.in_(location_names))
        )
        gross_areas_result = await db.execute(
            select(models.GrossArea).filter(models.GrossArea.area.in_(gross_area_names))
        )
        gross_area_units_result = await db.execute(
            select(models.GrossAreaUnit).filter(models.GrossAreaUnit.name.in_(gross_area_unit_names))
        )

        # Convert results to lists
        categories = categories_result.scalars().all()
        subcategories = subcategories_result.scalars().all()
        locations = locations_result.scalars().all()
        gross_areas = gross_areas_result.scalars().all()
        gross_area_units = gross_area_units_result.scalars().all()

        # Create dictionaries for easy lookup
        category_subcategory_map = {
            category.id: {subcategory.name: subcategory.id for subcategory in subcategories if subcategory.category_id == category.id}
            for category in categories
        }
        location_map = {location.name: location.id for location in locations}
        gross_area_map = {gross_area.area: gross_area.id for gross_area in gross_areas}
        gross_area_unit_map = {gross_area_unit.name: gross_area_unit.id for gross_area_unit in gross_area_units}

        # Prepare facilities list
        facilities = []

        # Validate and create facility records
        for idx, row in enumerate(reader, start=1):
            # Validate category and subcategory
            category_name = row['category_name']
            subcategory_name = row['subcategory_name']
            category_id = next((category.id for category in categories if category.name == category_name), None)
            subcategory_id = category_subcategory_map.get(category_id, {}).get(subcategory_name)

            if not category_id or not subcategory_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid category/subcategory: {row['category_name']}/{row['subcategory_name']} at row {idx}"
                )

            # Validate location
            location_name = row['location_name']
            location_id = location_map.get(location_name)
            if not location_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid location: {row['location_name']} at row {idx}"
                )
            print(gross_areas)
            print(gross_area_map)
            print(gross_area_names)
            # Validate gross area
            gross_area_name = int(row['gross_area'])
            gross_area_id = gross_area_map.get(gross_area_name)
            if not gross_area_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid gross area: {row['gross_area']} at row {idx}"
                )

            # Validate gross area unit
            gross_area_unit_name = row['gross_area_unit_name']
            gross_area_unit_id = gross_area_unit_map.get(gross_area_unit_name)
            if not gross_area_unit_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid gross area unit: {row['gross_area_unit_name']} at row {idx}"
                )
            try:
            # Create the facility object
                facility = models.CatalogsFacilities(
                    name=row['name'],
                    category_id=category_id,
                    sub_category_id=subcategory_id,
                    location_id=location_id,
                    internal_id=row['internal_id'],
                    description=row['description'],
                    refrigrant_remaining_at_disposal=float(row['refrigrant_remaining_at_disposal']),
                    gross_area_id=gross_area_id,
                    gross_area_unit_id=gross_area_unit_id,
                    occupancy=float(row['occupancy']),
                    created_by = user_id
                )
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid occupancy or refrigrant_remaining_at_disposal value at row {idx}: '{row['refrigrant_remaining_at_disposal']}' or {row['occupancy']} is not a valid floating point"
                )
            facilities.append(facility)

        # Bulk insert facilities
        db.add_all(facilities)
        await db.commit()

        # Refresh and return the facilities
        for facility in facilities:
            await db.refresh(facility)

        return {"msg": "Facilities saved successfully", "facilities": facilities}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error saving facilities"
        )
    


@router.post('/financed-enities/',response_model=schemas.FinancedEntitiesResp)
async def create_financed_entity(
        name:str = Form(...),
        listed:bool = Form(...),
        ticker:str = Form(...),
        description:str = Form(...),
        contact_name:str = Form(...),
        contact_email:str = Form(...),
        internal_id:str = Form(...),
        country_id:int = Form(...),
        state_id:int = Form(...),
        city_id:int = Form(...),
        industry_sector_id:int = Form(...),
        industry_id:int = Form(...),
        sub_industry_id:int = Form(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):

    data = {
        "name":name,
        "listed":listed,
        "ticker": ticker,
        "contact_name":contact_name,
        "contact_email":contact_email,
        "internal_id":internal_id,
        "description":description,
        "country_id":country_id,
        "state_id":state_id,
        "city_id":city_id,
        "industry_sector_id":industry_sector_id,
        "industry_id":industry_id,
        "sub_industry_id":sub_industry_id,
        "created_by": user_id
    }   

    state = await (db.execute(select(GeneralStates).where(GeneralStates.id == state_id)))
    state_result = state.scalar_one_or_none()

    city = await (db.execute(select(GeneralCities).where(GeneralCities.id == city_id)))
    city_reult = city.scalar_one_or_none()

    if (state_result.country_id != country_id) or (city_reult.state_id != state_id):
        raise HTTPException(
            status_code=400,
            detail= "Country,state and city does not match"
        )
    
    industry = await (db.execute(select(models.Industry).where(models.Industry.id == industry_id)))
    industry_reult = industry.scalar_one_or_none()
    
    sub_industry = await (db.execute(select(models.SubIndustry).where(models.SubIndustry.id == sub_industry_id)))
    sub_industry_reult = sub_industry.scalar_one_or_none()

    if (industry_reult.sector_id != industry_sector_id) or (sub_industry_reult.industry_id != industry_id):
        raise HTTPException(
            status_code=400,
            detail= "sector,industry and sub industry does not match"
        )


    financed_entity = await crud_financed_entities.create(db=db,obj_in=data)

    assignment_data = {
        "user_id": user_id,
        "financed_entity_id": financed_entity.id
    }

    user_company_assignment = await crud_user_company_assignment.create(db=db,obj_in=assignment_data)



    return{
        "msg": "financed entity added successfully",
        "financed_entity": financed_entity
    }

@router.post("/assign-listed-entity/",response_model = schemas.UserCompanyAssignmentResp)
async def create_user_company_assignment(
        financed_entity_id:uuid.UUID = Form(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    assignment_data = {
        "user_id": user_id,
        "financed_entity_id": financed_entity_id,
        "created_by": user_id
    }

    user_company_assignment_exs = await crud_user_company_assignment.get_multi_filters(db = db,filters={"user_id":user_id,"financed_entity_id":financed_entity_id})

    if len(user_company_assignment_exs) != 0:
        raise HTTPException(
            status_code=409,
            detail = 'Financed entity already assigned to user'
        )

    user_company_assignment = await crud_user_company_assignment.create(db=db,obj_in=assignment_data)

    return  {
        "msg": "financed_entity assigned succesfully",
        "user_company_assignment": user_company_assignment
        }

@router.put("/assign-listed-entity/{user_financed_enitity_assignment_id}",response_model = schemas.UserCompanyAssignmentResp)
async def update_user_company_assignment(
        user_financed_enitity_assignment_id:uuid.UUID,
        financed_entity_id:uuid.UUID = Form(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
 
    assignment = schemas.UserCompanyAssignmentCreate(
        financed_entity_id=financed_entity_id,
        user_id= user_id
    )

    user_company_assignment_exs = await crud_user_company_assignment.get_multi_filters(db = db,filters={"user_id":user_id,"financed_entity_id":financed_entity_id})

    if len(user_company_assignment_exs) != 0:
        raise HTTPException(
            status_code=409,
            detail = 'Financed entity already assigned to user'
        )

    user_company_assignment = await crud_user_company_assignment.update(db=db,obj_in=assignment,user_id=user_id,id=user_financed_enitity_assignment_id)

    return  {
        "msg": "financed_entity re-assigned succesfully",
        "user_company_assignment": user_company_assignment
        }

@router.get("/assign-listed-entity/{user_financed_enitity_assignment_id}",response_model = schemas.UserCompanyAssignmentRead)
async def get_user_company_assignment(
        user_financed_enitity_assignment_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    user_company_assignment = await crud_user_company_assignment.get(db=db,id=user_financed_enitity_assignment_id)

    return user_company_assignment

@router.get("/assign-listed-entity/",response_model = List[schemas.UserCompanyAssignmentRead])
async def get_user_company_assignments(
        user_Id:uuid.UUID = Query(None,description="User id assigned"),
        financed_entity_id:uuid.UUID = Query(None,description="Financed entity id assigned"),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    

    filters = {}

    if user_Id:
        filters['user_Id'] = user_Id
    if financed_entity_id:
        filters['financed_entity_id'] = financed_entity_id

    user_company_assignment_exs = await crud_user_company_assignment.get_multi_filters(db = db,filters=filters)

    return user_company_assignment_exs


@router.delete("/assign-listed-entity/{user_financed_enitity_assignment_id}",response_model = dict)
async def delete_user_company_assignments(
        user_financed_enitity_assignment_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    user_company_db = await crud_user_company_assignment.delete(db=db,id=user_financed_enitity_assignment_id,user_id=user_id)

    return {
        "msg" : "assignment deleted successfully",
    }
  



@router.get("/financed-enities/", response_model=List[schemas.FinancedEntitiesRead])
async def get_financed_entities(
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(10, description="Maximum number of records to retrieve"),
        name: Optional[str] = Query(None,description="Name of the financed entities"),
        listed: Optional[bool] = Query(None,description="Is financed entities listed or not"),
        ticker: Optional[str] = Query(None,description="Ticker of company if listed"),
        contact_name: Optional[str] = Query(None,description="Conact name of the financed entity"),
        contact_email: Optional[str] = Query(None,description="Contact email of financed entity"),
        internal_id: Optional[str] = Query(None,description="Internal ID of financed entity"),
        description: Optional[str] = Query(None,description="Description of financed entity"),
        country_id: Optional[int] = Query(None,description="Country id of financed entity"),
        state_id: Optional[int] = Query(None,description="State id of financed entity"),
        city_id: Optional[int] = Query(None,description="City id of financed entity"),
        industry_sector_id: Optional[int] = Query(None,description="Sector id of financed entity"),
        industry_id: Optional[int] = Query(None,description="Industry id of financed entity"),
        sub_industry_id: Optional[int] = Query(None,description="Sub industry id of financed entity"),
        
        
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    filters = {}
    if name:
        filters['name'] = name
    if listed != None:
        filters['listed'] = listed
    if contact_name:
        filters["contact_name"] = contact_name
    if contact_email:
        filters['contact_email'] = contact_email
    if internal_id:
        filters['internal_id'] = internal_id
    if country_id:
        filters['country_id'] = country_id
    if state_id:
        filters['state_id'] = state_id
    if description:
        filters['description'] = description
    if city_id:
        filters['city_id'] = city_id
    if industry_sector_id:
        filters['industry_sector_id'] = industry_sector_id
    if industry_id:
        filters['industry_id'] = industry_id
    if sub_industry_id:
        filters['sub_industry_id'] = sub_industry_id
    if ticker:
        filters['ticker'] = ticker
    
    

    financed_entities = await crud_financed_entities.get_multi_filters(db=db,filters=filters,skip=skip,limit=limit)
    print(listed)
    print(state_id)
    print(filters)
    return financed_entities



@router.get("/financed-enities/{financed_entity_id}", response_model=schemas.FinancedEntitiesRead)
async def get_financed_entities(
        financed_entity_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    financed_entity = await crud_financed_entities.get(db=db,id=financed_entity_id)

    return financed_entity

@router.put("/financed-enities/{financed_entity_id}", response_model=schemas.FinancedEntitiesResp)
async def update_facility(
        financed_entity_id:uuid.UUID,
        financed_entity: schemas.FinancedEntitiesCreate,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    

    
    financed_entity_db = await crud_financed_entities.update(db=db,obj_in=financed_entity,id=financed_entity_id,user_id=user_id)

    return {
        "msg" : "Financed enitites updated successfully",
        "financed_entity": financed_entity_db
    }



@router.delete("/financed-enities/{financed_entity_id}", response_model=dict)
async def delete_facility(
        financed_entity_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    financed_entity_db = await crud_financed_entities.delete(db=db,id=financed_entity_id,user_id=user_id)

    return {
        "msg" : "Financed enitites deleted successfully",
    }

@router.post("/financed-entities-bulk/", response_model=schemas.FinancedEntitiesRespBulk)
async def bulk_upload_financed_entities(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_async_db),
        user_id:uuid.UUID = Depends(get_current_user)):
    
    try:
         # Read and process CSV file
        content = await file.read()
        content_str = content.decode('utf-8-sig')  # Handle BOM by using 'utf-8-sig'
        csv_file = io.StringIO(content_str)
        reader = csv.DictReader(csv_file)
        
        # Extract unique names for lookup
        country_names = set()
        state_names = set()
        city_names = set()
        industry_sector_names = set()
        industry_names = set()
        sub_industry_names = set()

        # Keep track of row index for error handling
        row_index = 1
        print(reader.fieldnames)
        for row in reader:
            row_index += 1  # Increment row index to track the row being processed

            # Collect fields for lookup
            country_names.add(row['country_name'])
            state_names.add(row['state_name'])
            city_names.add(row['city_name'])
            industry_sector_names.add(row['industry_sector_name'])
            industry_names.add(row['industry_name'])
            sub_industry_names.add(row['sub_industry_name'])

        # Fetch relevant data from the database
        countries_result = await db.execute(
            select(models.GeneralCountries).filter(models.GeneralCountries.name.in_(country_names))
        )
        states_result = await db.execute(
            select(models.GeneralStates).filter(models.GeneralStates.name.in_(state_names))
        )
        cities_result = await db.execute(
            select(models.GeneralCities).filter(models.GeneralCities.name.in_(city_names))
        )
        industry_sectors_result = await db.execute(
            select(models.IndustrySector).filter(models.IndustrySector.name.in_(industry_sector_names))
        )
        industries_result = await db.execute(
            select(models.Industry).filter(models.Industry.name.in_(industry_names))
        )
        sub_industries_result = await db.execute(
            select(models.SubIndustry).filter(models.SubIndustry.name.in_(sub_industry_names))
        )

        # Convert results to lists
        countries = countries_result.scalars().all()
        states = states_result.scalars().all()
        cities = cities_result.scalars().all()
        industry_sectors = industry_sectors_result.scalars().all()
        industries = industries_result.scalars().all()
        sub_industries = sub_industries_result.scalars().all()

        # Create dictionaries for easy lookup
        country_map = {country.name: country.id for country in countries}
        state_map = {state.name: state.id for state in states}
        city_map = {city.name: city.id for city in cities}
        industry_sector_map = {sector.name: sector.id for sector in industry_sectors}
        industry_map = {industry.name: industry.id for industry in industries}
        sub_industry_map = {sub_industry.name: sub_industry.id for sub_industry in sub_industries}

        # Create dictionaries to validate relationships
        country_state_map = {
            country.id: {state.name: state.id for state in states if state.country_id == country.id}
            for country in countries
        }
        state_city_map = {
            state.id: {city.name: city.id for city in cities if city.state_id == state.id}
            for state in states
        }
        industry_sector_to_industries = {
            sector.id: {industry.name: industry.id for industry in industries if industry.sector_id == sector.id}
            for sector in industry_sectors
        }
        industry_to_sub_industries = {
            industry.id: {sub_industry.name: sub_industry.id for sub_industry in sub_industries if sub_industry.industry_id == industry.id}
            for industry in industries
        }

        # Prepare financed entities list
        financed_entities = []

        # Validate and create financed entity records
        # Rewind the CSV file to re-read it
        csv_file.seek(0)
        reader = csv.DictReader(csv_file)
        for idx, row in enumerate(reader, start=1):
            try:
                # Validate and get IDs
                country_name = row['country_name']
                state_name = row['state_name']
                city_name = row['city_name']
                industry_sector_name = row['industry_sector_name']
                industry_name = row['industry_name']
                sub_industry_name = row['sub_industry_name']
                
                country_id = country_map.get(country_name)
                state_id = state_map.get(state_name)
                city_id = city_map.get(city_name)
                industry_sector_id = industry_sector_map.get(industry_sector_name)
                industry_id = industry_map.get(industry_name)
                sub_industry_id = sub_industry_map.get(sub_industry_name)
                print(country_name,city_name,state_name)
                if not country_id or not state_id or not city_id:
                    raise ValueError(f"Invalid country/state/city at row {idx}")
                
                if not industry_sector_id or not industry_id or not sub_industry_id:
                    raise ValueError(f"Invalid sector/idustry/sub industry at row {idx}")

                # Validate state and country
                if country_id and state_id:
                    valid_states = country_state_map.get(country_id, {})
                    if state_id not in valid_states.values():
                        raise ValueError(f"Invalid state {row["state_name"]} for country {row["country_name"]} at row {idx}")

                # Validate city and state
                if state_id and city_id:
                    valid_cities = state_city_map.get(state_id, {})
                    if city_id not in valid_cities.values():
                        raise ValueError(f"Invalid city {row["city_name"]} for state {row['state_name']} at row {idx}")

                # Validate industry sector and industry
                if industry_sector_id and industry_id:
                    valid_industries = industry_sector_to_industries.get(industry_sector_id, {})
                    if industry_id not in valid_industries.values():
                        raise ValueError(f"Invalid industry {row["industry_name"]} for {row["industry_sector_name"]} sector at row {idx}")

                # Validate sub-industry and industry
                if industry_id and sub_industry_id:
                    valid_sub_industries = industry_to_sub_industries.get(industry_id, {})
                    if sub_industry_id not in valid_sub_industries.values():
                        raise ValueError(f"Invalid sub-industry {row["sub_industry_name"]} for industry {row["industry_name"]} at row {idx}")

                # Create the financed entity object
                financed_entity = models.CatalogsFinancedEntities(
                    name=row['name'],
                    listed=row['listed'].lower() in ['true', '1'],
                    description=row['description'],
                    contact_name=row['contact_name'],
                    contact_email=row['contact_email'],
                    internal_id=row['internal_id'],
                    country_id=country_id,
                    state_id=state_id,
                    city_id=city_id,
                    industry_sector_id=industry_sector_id,
                    industry_id=industry_id,
                    sub_industry_id=sub_industry_id,
                    created_by = user_id
                )
                financed_entities.append(financed_entity)

            except ValueError as e:
                # Catch validation errors and include row index in the exception
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error in row {idx}: {str(e)}"
                )

        # Bulk insert financed entities
        db.add_all(financed_entities)
        await db.commit()

        # Refresh and return the financed entities
        for entity in financed_entities:
            await db.refresh(entity)

        return {"msg": "Financed entities saved successfully", "financed_entities": financed_entities}

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error saving facilities"
        )
    

@router.post('/equipment-type/',response_model=schemas.EquipmentTypeResp)
async def create_equipment_type(
        name:str = Form(...),
        installation_emission:int = Form(...),
        operation_emission_per_year:int = Form(...),
        refrigrant_remaining_at_disposal:int = Form(...),
        refrigrant_remaining_at_disposal_percentage:float = Form(...),
        category_id:int = Form(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    data = {
        "name":name,
        "installation_emission":installation_emission,
        "operation_emission_per_year":operation_emission_per_year,
        "refrigrant_remaining_at_disposal":refrigrant_remaining_at_disposal,
        "refrigrant_remaining_at_disposal_percentage":refrigrant_remaining_at_disposal_percentage,
        "category_id":category_id,
        "created_by": user_id
    }

    category = await db.execute(select(models.Category).where(models.Category.id == category_id))
    category_db = category.scalar_one_or_none()

    if category_db == None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    equipment_type = await crud_equipment_type.create(db=db,obj_in=data)

    return{
        "msg": "Equipment type added successfully",
        "equipment_type": equipment_type
    }

@router.get('/equipment-type/',response_model=List[schemas.EquipmentTypeRead])
async def get_equipment_types(
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(10, description="Maximum number of records to retrieve"),
        name:str = Query(None,description="Name of equipment type"),
        installation_emission:int = Query(None,description="Installation emission of equipment type"),
        operation_emission_per_year:int = Query(None,description="Operation emission per year of equipment type"),
        refrigrant_remaining_at_disposal:int =Query(None,description="Refrigrant remaining at disposal of equipment type"),
        refrigrant_remaining_at_disposal_percentage:float = Query(None,description="Refrigrant remaining at disposal in percentage of equipment type"),
        category_id:int = Query(None,description="Category of equipment type"),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    filters = {}
    if name:
        filters['name'] = name
    if installation_emission:
        filters["installation_emission"] = installation_emission
    if operation_emission_per_year:
        filters['operation_emission_per_year'] = operation_emission_per_year
    if refrigrant_remaining_at_disposal:
        filters['refrigrant_remaining_at_disposal'] = refrigrant_remaining_at_disposal
    if refrigrant_remaining_at_disposal_percentage:
        filters['refrigrant_remaining_at_disposal_percentage'] = refrigrant_remaining_at_disposal_percentage
    if category_id:
        filters['category_id'] = category_id


    equipment_types = await crud_equipment_type.get_multi_filters(db=db,filters=filters,skip=skip,limit=limit)

    return equipment_types


@router.get('/equipment-type/{equipment_type_id}',response_model=schemas.EquipmentTypeRead)
async def get_equipment_type(
        equipment_type_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    financed_entity = await crud_equipment_type.get(db=db,id=equipment_type_id)

    return financed_entity


@router.put('/equipment-type/{equipment_type_id}',response_model=schemas.EquipmentTypeResp)
async def update_equipment_type(
        equipment_type: schemas.EquipmentTypeCreate,
        equipment_type_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    category = await db.execute(select(models.Category).where(models.Category.id == equipment_type.category_id))
    category_db = category.scalar_one_or_none()

    if category_db == None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    equipment_type = await crud_equipment_type.update(db=db,obj_in=equipment_type,user_id=user_id,id=equipment_type_id)

    return{
        "msg": "Equipment type updated successfully",
        "equipment_type": equipment_type
    }

@router.delete('/equipment-type/{equipment_type_id}',response_model=dict)
async def delete_equipment_type(
        equipment_type_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    equipment_type = await crud_equipment_type.delete(db=db,id=equipment_type_id,user_id=user_id)

    return {
        "msg" : "Equipment type deleted successfully",
    }

@router.post("/equipment-type-bulk/", response_model=schemas.EquipmentTypeRespBulk)
async def bulk_upload_equipment_type(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_async_db),
        user_id:uuid.UUID = Depends(get_current_user)):
    
    try:
         # Read and process CSV file
        content = await file.read()
        content_str = content.decode('utf-8-sig')  # Handle BOM by using 'utf-8-sig'
        csv_file = io.StringIO(content_str)
        reader = csv.DictReader(csv_file)

         # Extract unique names for lookup
        category_names = set()
        
        for row in reader:
            category_names.add(row['category_name'])

         # Fetch relevant data from the database
        category_results = await db.execute(
            select(models.Category).filter(models.Category.name.in_(category_names))
        )

         # Convert results to lists
        categories = category_results.scalars().all()
        # Create dictionaries for easy lookup
        category_map = {category.name: category.id for category in categories}

        # Prepare financed entities list
        equipent_types = []

        # Validate and create financed entity records
        # Rewind the CSV file to re-read it
        csv_file.seek(0)
        reader = csv.DictReader(csv_file)
        # Validate and create facility records
        for idx, row in enumerate(reader, start=1):
            try:
                # Validate category and subcategory
                category_name = row['category_name']
                category_id = category_map.get(category_name)


                if not category_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid category: {row['category_name']} at row {idx}"
                    )
                try:
                    equipment_type = models.CatalogsEquipmentType(
                    name=row['name'],
                    installation_emission=int(row['installation_emission']),
                    operation_emission_per_year=int(row['operation_emission_per_year']),
                    refrigrant_remaining_at_disposal=int(row['refrigrant_remaining_at_disposal']),
                    refrigrant_remaining_at_disposal_percentage=float(row['refrigrant_remaining_at_disposal_percentage']),
                    category_id=category_id,
                    created_by = user_id
                    )
                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid integar or float of on the columns at row {idx}"
                    )
                equipent_types.append(equipment_type)

            except ValueError as e:
                # Catch validation errors and include row index in the exception
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error in row {idx}: {str(e)}"
                )
        
         # Bulk insert financed entities
        db.add_all(equipent_types)
        await db.commit()

        # Refresh and return the financed entities
        for entity in equipent_types:
            await db.refresh(entity)

        return {"msg": "Equipment types saved successfully", "equipment_types": equipent_types}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error saving facilities"
        )


@router.post('/product/',response_model=schemas.ProductResp)
async def create_product(
        name:str = Form(...),
        weight:int = Form(...),
        category_id:int = Form(...),
        sub_category_id:int = Form(...),
        weight_unit_id:int = Form(...),
        internal_id:str = Form(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    data = {
        "name":name,
        "weight":weight,
        "sub_category_id":sub_category_id,
        "weight_unit_id":weight_unit_id,
        "internal_id":internal_id,
        "category_id":category_id,
        "created_by": user_id
    }

    category = await db.execute(select(models.Category).where(models.Category.id == category_id))
    category_db = category.scalar_one_or_none()

    
    weight_unit = await db.execute(select(models.GeneralUnit).where(models.GeneralUnit.id == weight_unit_id))
    weight_unit_db = weight_unit.scalar_one_or_none()

    

    if category_db == None or weight_unit_db == None:
        raise HTTPException(
            status_code=404,
            detail="Category or weight unit not found"
        )
    

    sub_category = await (db.execute(select(SubCategory).where(SubCategory.id == sub_category_id)))
    sub_category_result = sub_category.scalar_one_or_none()
    
    if sub_category_result.category_id != category_id:
        raise HTTPException(
            status_code=400,
            detail= "category and subcategory does not match"
        )

    product = await crud_product.create(db=db,obj_in=data)

    return{
        "msg": "Product added successfully",
        "product": product
    }

@router.get('/product/',response_model=List[schemas.ProductRead])
async def get_products(
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(10, description="Maximum number of records to retrieve"),
        name:str = Query(None, description="Name of the product"),
        weight:int = Query(None, description="Weight of the product"),
        category_id:int = Query(None, description="Category id of the product"),
        sub_category_id:int = Query(None, description="Sub category id of the product"),
        weight_unit_id:int = Query(None, description="weight unit id of the product"),
        internal_id:str = Query(None, description="Internal id of the product"),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    filters = {}
    if name:
        filters['name'] = name
    if weight:
        filters["weight"] = weight
    if sub_category_id:
        filters['sub_category_id'] = sub_category_id
    if weight_unit_id:
        filters['weight_unit_id'] = weight_unit_id
    if internal_id:
        filters['internal_id'] = internal_id
    if category_id:
        filters['category_id'] = category_id


    products = await crud_product.get_multi_filters(db=db,filters=filters,skip=skip,limit=limit)

    return products


@router.get('/product/{product_id}',response_model=schemas.ProductRead)
async def get_equipment_type(
        product_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    product = await crud_product.get(db=db,id=product_id)

    return product


@router.put('/product/{product_id}',response_model=schemas.ProductResp)
async def update_product(
        product: schemas.ProductCreate,
        product_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    category = await db.execute(select(models.Category).where(models.Category.id == product.category_id))
    category_db = category.scalar_one_or_none()

    
    weight_unit = await db.execute(select(models.GeneralUnit).where(models.GeneralUnit.id == product.weight_unit_id))
    weight_unit_db = weight_unit.scalar_one_or_none()

    

    if category_db == None or weight_unit_db == None:
        raise HTTPException(
            status_code=404,
            detail="Category or weight unit not found"
        )
    

    sub_category = await (db.execute(select(SubCategory).where(SubCategory.id == product.sub_category_id)))
    sub_category_result = sub_category.scalar_one_or_none()
    
    if sub_category_result.category_id != product.category_id:
        raise HTTPException(
            status_code=400,
            detail= "category and subcategory does not match"
        )


    product = await crud_product.update(db=db,obj_in=product,user_id=user_id,id=product_id)

    return{
        "msg": "Product updated successfully",
        "product": product
    }

@router.delete('/product/{product_id}',response_model=dict)
async def delete_product(
        product_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    await crud_product.delete(db=db,id=product_id,user_id=user_id)

    return {
        "msg" : "Product deleted successfully",
    }

@router.post("/product-bulk/", response_model=schemas.ProductRespBulk)
async def bulk_upload_suppliers(
        file: UploadFile = File(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):

    convertions = {
        'weight': int
    }

    field_mappings = {
        'name': 'name',
        'weight': 'weight',
        'category': 'category_id',
        'sub_category': 'sub_category_id',
        'unit': 'weight_unit_id',
        'internal_id': 'internal_id'
    }

    foreign_key_configs = {
        'category_id': (models.Category, 'name'),
        'sub_category_id': (models.SubCategory, 'name'),
        'weight_unit_id': (models.GeneralUnit, 'name')
    }

    relationship_configs = {
        ('category_id', 'sub_category_id'): (models.SubCategory, 'category_id', 'name')
    }

    products =  await generalized_bulk_upload(
        file, db, user_id, models.CatalogsProduct,convertions,
        field_mappings, foreign_key_configs, relationship_configs
    )

    return {
        "msg": "Prodcts created successfully",
        "products": products
    }


@router.post('/supplier/',response_model=schemas.SupplierResp)
async def create_supplier(
        name:str = Form(...),
        contact_name:str = Form(...),
        contact_email:str = Form(...),
        industry_sector_id:int = Form(...),
        industry_id:int = Form(...),
        sub_industry_id:int = Form(...),
        notes:str = Form(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    data = {
        "name":name,
        "contact_name":contact_name,
        "contact_email":contact_email,
        "industry_sector_id":industry_sector_id,
        "industry_id":industry_id,
        "sub_industry_id":sub_industry_id,
        "notes":notes,
        "created_by": user_id
    }

    sector = await db.execute(select(models.IndustrySector).where(models.IndustrySector.id == industry_sector_id))
    sector_db = sector.scalar_one_or_none()

    industry = await db.execute(select(models.Industry).where(models.Industry.id == industry_id))
    industry_db = industry.scalar_one_or_none()
    
    
    sub_industry = await db.execute(select(models.SubIndustry).where(models.SubIndustry.id == sub_industry_id))
    sub_industry_db = sub_industry.scalar_one_or_none()

    

    if industry_db == None or sub_industry_db == None or sector_db == None:
        raise HTTPException(
            status_code=404,
            detail="industry sector, industry or sub industry not found"
        )
    
    
    if industry_db.sector_id != industry_sector_id or sub_industry_db.industry_id != industry_id:
        raise HTTPException(
            status_code=400,
            detail= "industry sector, industry or sub industry does not match"
        )

    supplier = await crud_supplier.create(db=db,obj_in=data)

    return{
        "msg": "Supplier added successfully",
        "supplier": supplier
    }


@router.get('/supplier/',response_model=List[schemas.SupplierRead])
async def get_suppliers(
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(10, description="Maximum number of records to retrieve"),
        name:str = Query(None,description="Name of the supplier"),
        contact_name:str = Query(None,description="Contact name of the supplier"),
        contact_email:str = Query(None,description="Contact email of the supplier"),
        industry_sector_id:int = Query(None,description="Sector id of supplier"),
        industry_id:int = Query(None,description="Industry id of supplier of the supplier"),
        sub_industry_id:int = Query(None,description="Sub industry id of the supplier"),
        notes:str = Query(None,description="Notes on supplier"),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    filters = {}
    if name:
        filters['name'] = name
    if contact_name:
        filters["contact_name"] = contact_name
    if contact_email:
        filters['contact_email'] = contact_email
    if industry_sector_id:
        filters['industry_sector_id'] = industry_sector_id
    if industry_id:
        filters['industry_id'] = industry_id
    if sub_industry_id:
        filters['sub_industry_id'] = sub_industry_id
    if notes:
        filters['notes'] = notes

    suppliers = await crud_supplier.get_multi_filters(db=db,filters=filters,skip=skip,limit=limit)

    return suppliers




@router.get('/supplier/{supplier_id}',response_model=schemas.SupplierRead)
async def get_supplier(
        supplier_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    supplier = await crud_supplier.get(db=db,id=supplier_id)

    return supplier


@router.put('/supplier/{supplier_id}',response_model=schemas.SupplierResp)
async def update_supplier(
        supplier: schemas.SupplierCreate,
        supplier_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):

    sector = await db.execute(select(models.IndustrySector).where(models.IndustrySector.id == supplier.industry_sector_id))
    sector_db = sector.scalar_one_or_none()

    industry = await db.execute(select(models.Industry).where(models.Industry.id == supplier.industry_id))
    industry_db = industry.scalar_one_or_none()
    
    
    sub_industry = await db.execute(select(models.SubIndustry).where(models.SubIndustry.id == supplier.sub_industry_id))
    sub_industry_db = sub_industry.scalar_one_or_none()

    

    if industry_db == None or sub_industry_db == None or sector_db == None:
        raise HTTPException(
            status_code=404,
            detail="industry sector, industry or sub industry not found"
        )
    
    
    if industry_db.sector_id != supplier.industry_sector_id or sub_industry_db.industry_id != supplier.industry_id:
        raise HTTPException(
            status_code=400,
            detail= "industry sector, industry or sub industry does not match"
        )


    supplier = await crud_supplier.update(db=db,obj_in=supplier,user_id=user_id,id=supplier_id)

    return{
        "msg": "Supplier updated successfully",
        "supplier": supplier
    }
@router.delete('/supplier/{supplier_id}',response_model=dict)
async def delete_supplier(
        supplier_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    await crud_supplier.delete(db=db,id=supplier_id,user_id=user_id)

    return {
        "msg" : "Supplier deleted successfully",
    }

@router.post("/supplier-bulk/", response_model=schemas.SupplierRespBulk)
async def bulk_upload_suppliers(
        file: UploadFile = File(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):


    field_mappings = {
        'name': 'name',
        'contact_name': 'contact_name',
        'contact_email': 'contact_email',
        'industry_sector': 'industry_sector_id',
        'industry': 'industry_id',
        'sub_industry': 'sub_industry_id',
        'notes': 'notes'
    }

    foreign_key_configs = {
        'industry_sector_id': (models.IndustrySector, 'name'),
        'industry_id': (models.Industry, 'name'),
        'sub_industry_id': (models.SubIndustry, 'name')
    }

    relationship_configs = {
        ('industry_sector_id', 'industry_id'): (models.Industry, 'sector_id', 'name'),
        ('industry_id', 'sub_industry_id'): (models.SubIndustry, 'industry_id', 'name')

    }

    suppliers =  await generalized_bulk_upload(
        file, db, user_id, models.CatalogsSupplier,
        field_mappings, foreign_key_configs, relationship_configs
    )

    return {
        "msg": "Suppliers created successfully",
        "suppliers": suppliers
    }


@router.post('/customer/',response_model=schemas.CustomerResp)
async def create_customer(
        name:str = Form(...),
        contact_name:str = Form(...),
        contact_email:str = Form(...),
        industry_sector_id:int = Form(...),
        industry_id:int = Form(...),
        sub_industry_id:int = Form(...),
        notes:str = Form(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    data = {
        "name":name,
        "contact_name":contact_name,
        "contact_email":contact_email,
        "industry_sector_id":industry_sector_id,
        "industry_id":industry_id,
        "sub_industry_id":sub_industry_id,
        "notes":notes,
        "created_by": user_id
    }

    sector = await db.execute(select(models.IndustrySector).where(models.IndustrySector.id == industry_sector_id))
    sector_db = sector.scalar_one_or_none()

    industry = await db.execute(select(models.Industry).where(models.Industry.id == industry_id))
    industry_db = industry.scalar_one_or_none()
    
    
    sub_industry = await db.execute(select(models.SubIndustry).where(models.SubIndustry.id == sub_industry_id))
    sub_industry_db = sub_industry.scalar_one_or_none()

    

    if industry_db == None or sub_industry_db == None or sector_db == None:
        raise HTTPException(
            status_code=404,
            detail="industry sector, industry or sub industry not found"
        )
    
    
    if industry_db.sector_id != industry_sector_id or sub_industry_db.industry_id != industry_id:
        raise HTTPException(
            status_code=400,
            detail= "industry sector, industry or sub industry does not match"
        )

    customer = await crud_customer.create(db=db,obj_in=data)

    return{
        "msg": "Customer added successfully",
        "customer": customer
    }

@router.get('/customer/',response_model=List[schemas.CustomerRead])
async def get_customers(
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(10, description="Maximum number of records to retrieve"),
        name:str = Query(None,description="Name of the customer"),
        contact_name:str = Query(None,description="Contact name of the customer"),
        contact_email:str = Query(None,description="Contact email of the customer"),
        industry_sector_id:int = Query(None,description="Sector id of customer"),
        industry_id:int = Query(None,description="Industry id of the customer"),
        sub_industry_id:int = Query(None,description="Sub industry id of the customer"),
        notes:str = Query(None,description="Notes on customer"),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    filters = {}
    if name:
        filters['name'] = name
    if contact_name:
        filters["contact_name"] = contact_name
    if contact_email:
        filters['contact_email'] = contact_email
    if industry_sector_id:
        filters['industry_sector_id'] = industry_sector_id
    if industry_id:
        filters['industry_id'] = industry_id
    if sub_industry_id:
        filters['sub_industry_id'] = sub_industry_id
    if notes:
        filters['notes'] = notes

    customers = await crud_customer.get_multi_filters(db=db,filters=filters,skip=skip,limit=limit)

    return customers


@router.get('/customer/{customer_id}',response_model=schemas.SupplierRead)
async def get_cutomer(
        customer_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    customer = await crud_customer.get(db=db,id=customer_id)

    return customer


@router.put('/customer/{customer_id}',response_model=schemas.CustomerResp)
async def update_customer(
        customer: schemas.CustomerCreate,
        customer_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):

    sector = await db.execute(select(models.IndustrySector).where(models.IndustrySector.id == customer.industry_sector_id))
    sector_db = sector.scalar_one_or_none()

    industry = await db.execute(select(models.Industry).where(models.Industry.id == customer.industry_id))
    industry_db = industry.scalar_one_or_none()
    
    
    sub_industry = await db.execute(select(models.SubIndustry).where(models.SubIndustry.id == customer.sub_industry_id))
    sub_industry_db = sub_industry.scalar_one_or_none()

    

    if industry_db == None or sub_industry_db == None or sector_db == None:
        raise HTTPException(
            status_code=404,
            detail="industry sector, industry or sub industry not found"
        )
    
    
    if industry_db.sector_id != customer.industry_sector_id or sub_industry_db.industry_id != customer.industry_id:
        raise HTTPException(
            status_code=400,
            detail= "industry sector, industry or sub industry does not match"
        )


    customer = await crud_customer.update(db=db,obj_in=customer,user_id=user_id,id=customer_id)

    return{
        "msg": "Customer updated successfully",
        "customer": customer
    }

@router.delete('/customer/{customer_id}',response_model=dict)
async def delete_customer(
        customer_id:uuid.UUID,
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):
    
    await crud_customer.delete(db=db,id=customer_id,user_id=user_id)

    return {
        "msg" : "Customer deleted successfully",
    }


@router.post("/customer-bulk/", response_model=schemas.CustomerRespBulk)
async def bulk_upload_customers(
        file: UploadFile = File(...),
        user_id:uuid.UUID = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)):


    field_mappings = {
        'name': 'name',
        'contact_name': 'contact_name',
        'contact_email': 'contact_email',
        'industry_sector': 'industry_sector_id',
        'industry': 'industry_id',
        'sub_industry': 'sub_industry_id',
        'notes': 'notes'
    }

    foreign_key_configs = {
        'industry_sector_id': (models.IndustrySector, 'name'),
        'industry_id': (models.Industry, 'name'),
        'sub_industry_id': (models.SubIndustry, 'name')
    }

    relationship_configs = {
        ('industry_sector_id', 'industry_id'): (models.Industry, 'sector_id', 'name'),
        ('industry_id', 'sub_industry_id'): (models.SubIndustry, 'industry_id', 'name')

    }

    customers =  await generalized_bulk_upload(
        file, db, user_id, models.CatalogsCustomer,
        field_mappings, foreign_key_configs, relationship_configs
    )

    return {
        "msg": "Customers created successfully",
        "customers": customers
    }
