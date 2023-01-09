from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...routers.auth import check_token

from ...domain.preference.diet.user_diet_types import schema, services

router = APIRouter(prefix='/user-diet', tags=["user diet"])


@router.get('/', response_model=List[schema.UserDietType])
def get_user_diet_types(skip: int = 0, limit: int = 100, token: str = Depends(check_token), db: Session = Depends(get_db)):
    user_diet_types = services.get_all_user_diet_types(db, skip, limit)
    return user_diet_types

@router.get('/{user_id}', response_model=List[schema.UserDietType])
def get_user_diet_types(user_id: int, token: str = Depends(check_token), db: Session = Depends(get_db)):
    user_diet_type = services.get_user_diet_type(user_id, db)
    return user_diet_type

@router.post('/', response_model=schema.UserDietType)
def create_user_diet_type(user_diet_type: schema.UserDietTypeCreate, token: str = Depends(check_token), db: Session = Depends(get_db)):
    new_user_diet_type = services.create_user_diet_type(user_diet_type, db)
    return new_user_diet_type
