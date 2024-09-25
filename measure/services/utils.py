from typing import List, Dict, Any, Callable, Optional, Type, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase
from fastapi import UploadFile, HTTPException
import csv
import io
import uuid
import traceback


async def generalized_bulk_upload(
    file: UploadFile,
    db: AsyncSession,
    user_id: uuid.UUID,
    model: Type[DeclarativeBase],
    field_mappings: Dict[str, str],
    foreign_key_configs: Dict[str, Tuple[Type[DeclarativeBase], str]],
    relationship_configs: Dict[Tuple[str, str], Tuple[Type[DeclarativeBase], str, str]],
    convertions: Optional[Dict[str,Any]] = None,
):
    try:
        # Read and process CSV file
        content = await file.read()
        content_str = content.decode('utf-8-sig')
        csv_file = io.StringIO(content_str)
        reader = csv.DictReader(csv_file)

        # Extract unique values for lookup
        lookup_values = {field: set() for field,item in foreign_key_configs.items()}
        print(reader)
        for row in reader:
            print(row)
            for csv_field, db_field in field_mappings.items():
                if db_field in lookup_values.keys():
                    lookup_values[db_field].add(row[csv_field])
        print(lookup_values)
        # Fetch relevant data from the database
        fetched_data = {}
        for field, values in lookup_values.items():
            entity_model, name_field = foreign_key_configs[field]
            result = await db.execute(
                select(entity_model).filter(getattr(entity_model, name_field).in_(values))
            )
            fetched_data[field] = result.scalars().all()
        print(fetched_data)
        # Create dictionaries for easy lookup
        lookup_maps = {
            field: {getattr(item, name_field): item.id for item in items}
            for field, items in fetched_data.items() 
            for _, (_, name_field) in foreign_key_configs.items() 
        }

        print(lookup_maps)

        relationship_maps = {}
        for (parent_field, child_field), (rel_model, parent_key, child_key) in relationship_configs.items():
            result = await db.execute(select(rel_model))
            items = result.scalars().all()
            relationship_maps[(parent_field, child_field)] = {}
            for item in items:
                parent_id = getattr(item, parent_key)
                child_name = getattr(item, child_key)
                if parent_id not in relationship_maps[(parent_field, child_field)]:
                    relationship_maps[(parent_field, child_field)][parent_id] = {}
                relationship_maps[(parent_field, child_field)][parent_id][child_name] = item.id
        print(relationship_maps)
        # Prepare entities list
        entities = []

        # Validate and create entity records
        csv_file.seek(0)
        reader = csv.DictReader(csv_file)
        for idx, row in enumerate(reader, start=1):
            try:
                entity_data = {}
                for csv_field, db_field in field_mappings.items():
                    if db_field in fetched_data.keys():
                        name_value = row[csv_field]
                        entity_data[db_field] = lookup_maps[db_field].get(name_value)
                        if entity_data[db_field] is None:
                            raise ValueError(f"Invalid {db_field[:-3]} '{name_value}' at row {idx}")
                    else:
                        entity_data[db_field] = row[csv_field]

                # Run relationship validators
                for (parent_field, child_field), _ in relationship_configs.items():
                    parent_id = entity_data[parent_field]
                    print(parent_id)
                    child_name = row[child_field[:-3]]
                    print(child_name)
                    valid_children = relationship_maps[(parent_field, child_field)].get(parent_id, {})
                    print(valid_children)
                    if child_name not in valid_children:
                        raise ValueError(f"Invalid relationship between {parent_field[:-3]} and {child_field[:-3]} at row {idx}")
                    entity_data[child_field] = valid_children[child_name]

                #convert datatype according to db
                if convertions:  
                    for feild,type in convertions.items():
                        entity_data[feild] = type(entity_data[feild])

                # Create the entity object
                entity = model(**entity_data, created_by=user_id)
                entities.append(entity)

            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Error in row {idx}: {str(e)}")

        # Bulk insert entities
        db.add_all(entities)
        await db.commit()

        # Refresh and return the entities
        for entity in entities:
            await db.refresh(entity)

        return entities

    except HTTPException as e:
        traceback.print_exc()
        raise e
    except Exception as e:
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving {model.__name__}")