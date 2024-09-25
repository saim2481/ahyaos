from datetime import datetime
import traceback
from typing import Any, Dict, Type, TypeVar, Generic, List, Optional, Union
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy import update, delete,or_,and_

# Define generic type variables
ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        :param model: A SQLAlchemy model class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Union[int, UUID] ) -> Optional[ModelType]:
        """
        Get a single item by ID.
        """
        try:
            db_query = await db.execute(select(self.model).filter(self.model.id == id))
            db_obj = db_query.scalar_one_or_none()
            
            
            if db_obj is None:
                raise HTTPException(
                status_code=404,
                detail=f"{self.model.__tablename__} not found"
                )
            
            return db_obj
             

        except HTTPException as e:
            raise e
        except:
            await db.rollback()
            traceback.print_exc()
            raise HTTPException(status_code=500)
    
    async def get_multi_filters(
        self,
        db: AsyncSession,
        filters: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """
        Get all records with optional search filters.
        Args:
            db (AsyncSession): The database session.
            filters (Optional[Dict[str, Any]]): A dictionary of filters where keys are attribute names and values are the corresponding values to filter by.
            skip (int): Number of records to skip for pagination.
            limit (int): Maximum number of records to return.
        Returns:
            List[ModelType]: A list of filtered model instances.
        """
        try:
            query = select(self.model)

            # If filters are provided, dynamically build filter conditions
            if filters:
                filter_conditions = []
                for attr, value in filters.items():
                    column = getattr(self.model, attr, None)  # Get the model attribute
                    if column is not None and isinstance(column, InstrumentedAttribute):  # Ensure the attribute is valid
                        filter_conditions.append(column == value)

                if filter_conditions:
                    query = query.filter(and_(*filter_conditions))  # Apply all filters using AND logic

            # Apply pagination (skip and limit)
            query = query.offset(skip).limit(limit)

            # Execute the query and return results
            result = await db.execute(query)
            return result.scalars().all()
        except HTTPException as e:
            raise e
        except Exception:
            await db.rollback()
            traceback.print_exc()
            raise HTTPException(status_code=500)


    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get multiple items, optionally skip and limit.
        """
        try:
            result = await db.execute(select(self.model).offset(skip).limit(limit))
            return result.scalars().all()
        except:
            traceback.print_exc()
            raise HTTPException(status_code=500)

    async def create(self,db: AsyncSession,obj_in: Union[CreateSchemaType, Dict[str, Any]]) -> ModelType:

        try:
            # If obj_in is a dictionary (from form data), use it directly
            if isinstance(obj_in, dict):
                data = obj_in
            else:
                data = obj_in.dict()

            # Create a new model instance with the form data
            db_obj = self.model(**data)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except:
            await db.rollback()
            traceback.print_exc()
            raise HTTPException(status_code=500)

    async def update(self, db: AsyncSession, id: int,user_id:UUID, obj_in: UpdateSchemaType) -> ModelType:
        """
        Update an existing item.
        """
        try:
            db_query = await db.execute(select(self.model).where(self.model.id == id))
            db_obj = db_query.scalar_one_or_none()

            if db_obj is None:
                raise HTTPException(
                status_code=404,
                detail=f"{self.model.__tablename__} not found"
                )

            obj_data = obj_in.dict(
                exclude_unset=True)  # Only update fields that are provided
            obj_data["updated_at"] = datetime.utcnow()
            db_obj.updated_by = user_id
            for field, value in obj_data.items():
                setattr(db_obj, field, value)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except HTTPException as e:
            raise e
        except:
            await db.rollback()
            traceback.print_exc()
            raise HTTPException(status_code=500)

    async def delete(self, db: AsyncSession, id: int,user_id:UUID) -> Optional[ModelType]:
        """
        Delete an item by ID.
        """
        try:
            db_query = await db.execute(select(self.model).where(self.model.id == id))
            db_obj = db_query.scalar_one_or_none()

            if db_obj is None:
                raise HTTPException(
                status_code=404,
                detail=f"{self.model.__tablename__} not found"
                )
            
            db_obj.deleted_at = datetime.utcnow()
            db_obj.deleted_by = user_id

            await db.commit()
            await db.refresh(db_obj)
            return db_obj   
        except HTTPException as e:
            raise e
        except:
            await db.rollback()
            traceback.print_exc()
            raise HTTPException(status_code=500)
        
