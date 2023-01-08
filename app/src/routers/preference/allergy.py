from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...domain.preference.allergy.user_allergy import schema, services

router = APIRouter(prefix='/allergy', tags=["allergy"])


@router.get('/', response_model=List[schema.UserAllergy])
def get_user_allergies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_allergies = services.get_all_user_allergies(db, skip, limit)
    return user_allergies

@router.post('/', response_model=schema.UserAllergy)
def create_user_allergy(user_allergy: schema.UserAllergyCreate, db: Session = Depends(get_db)):
    new_user_allergy = services.create_user_allergy(user_allergy, db)
    return new_user_allergy
