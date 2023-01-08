from sqlalchemy.orm import Session
from . import model, schema

DEFAULT_LIMIT_USER_DIET_TYPE = 100

def get_all_user_diet_types(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_USER_DIET_TYPE):
    return db.query(model.UserDietType).offset(skip).limit(limit).all()

def create_user_diet_type(user_diet_type: schema.UserDietTypeCreate, db: Session):
    db_user_diet_type = model.UserDietType(**user_diet_type.dict())
    db.add(db_user_diet_type)
    db.commit()
    db.refresh(db_user_diet_type)
    return db_user_diet_type