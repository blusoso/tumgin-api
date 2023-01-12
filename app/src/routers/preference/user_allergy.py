from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...routers.auth import check_token

from ...domain.preference.allergy.user_allergy import schema, services

router = APIRouter(prefix='/user-allergy', tags=["user allergy"])


@router.get('/', response_model=List[schema.UserAllergy])
def get_user_allergies(skip: int = 0, limit: int = 100, token: str = Depends(check_token), db: Session = Depends(get_db)):
    user_allergies = services.get_all_user_allergies(db, skip, limit)
    return user_allergies

@router.get('/{user_id}', response_model=List[schema.UserAllergy])
def get_user_allergy_by_user_id(user_id: int, db: Session = Depends(get_db)):
    user_allergy = services.get_user_allergy_by_user_id(user_id, db)
    return user_allergy

@router.post('/', response_model=schema.UserAllergy)
def create_user_allergy(user_allergy: schema.UserAllergyCreate, token: str = Depends(check_token), db: Session = Depends(get_db)):
    new_user_allergy = services.create_user_allergy(user_allergy, db)
    return new_user_allergy

@router.delete('/delete/{id}')
def delete_user_allergy(id: int, token: str = Depends(check_token), db: Session = Depends(get_db)):
    deleted_user_allergy = services.delete_user_allergy(id, db)
    return deleted_user_allergy