from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from ..recipes.model import Recipe

DEFAULT_LIMIT_SEARCH_RECIPE = 5


def get_search(
    db: Session,
    q: str | None = None,
    skip: int = 0,
    limit: int = DEFAULT_LIMIT_SEARCH_RECIPE
):
    q = q.lower()

    db_search_recipe = db.query(
        Recipe.id,
        Recipe.name,
        Recipe.name_en,
        Recipe.slug)\
        .filter(or_(
            func.lower(Recipe.name).like(f"%{q}%"),
            func.lower(Recipe.name_en).like(f"%{q}%")))\
        .filter(Recipe.is_active == True)\
        .filter(Recipe.deleted_at == None)\
        .offset(skip)\
        .limit(limit)\
        .all()

    return db_search_recipe
