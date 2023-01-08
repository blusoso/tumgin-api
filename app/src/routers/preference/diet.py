from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...domain.preference.diet.diet_types import schema, services

router = APIRouter(prefix='/diet', tags=["diet"])


@router.get('/', response_model=List[schema.DietType])
def get_diet_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    diet_types = services.get_all_diet_types(db, skip, limit)
    return diet_types

@router.post('/', response_model=schema.DietType)
def create_diet_type(user_allergy: schema.DietTypeCreate, db: Session = Depends(get_db)):
    new_diet_type = services.create_diet_type(user_allergy, db)
    return new_diet_type
