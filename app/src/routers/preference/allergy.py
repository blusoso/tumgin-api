from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ...routers.auth import check_token

from ...domain.preference.allergy.allergy import services
from ...domain.food.ingredients.schema import Ingredient


router = APIRouter(prefix='/allergy', tags=["allergy"])


@router.get('/', response_model=List[Ingredient])
def get_allergies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    allergies = services.get_all_allergies(db, skip, limit)
    return allergies