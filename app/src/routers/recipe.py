from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ..dependencies import get_db

router = APIRouter(prefix='/recipe', tags=["recipe"])


@router.get('/')
def get_users(db: Session = Depends(get_db)):
    return {'recipe'}
