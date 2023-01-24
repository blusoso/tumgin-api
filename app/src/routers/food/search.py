from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...dependencies import get_db
from ...domain.food.search import services

router = APIRouter(prefix='/search', tags=["search"])


@router.get('/')
def get_search(
    q: str | None = None,
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    search = services.get_search(db, q, skip, limit)
    return search
