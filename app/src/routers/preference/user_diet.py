from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...domain.preference.diet.user_diet_types import schema, services

router = APIRouter(prefix='/user-diet', tags=["user diet"])


@router.get('/', response_model=List[schema.UserDietType])
def get_user_diet_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_diet_types = services.get_all_user_user_diet_types(db, skip, limit)
    return user_diet_types

@router.post('/', response_model=schema.UserDietType)
def create_user_diet_type(user_diet_type: schema.UserDietTypeCreate, db: Session = Depends(get_db)):
    new_user_diet_type = services.create_user_diet_type(user_diet_type, db)
    return new_user_diet_type
