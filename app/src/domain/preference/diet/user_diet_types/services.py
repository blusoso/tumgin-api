from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import model, schema

DEFAULT_LIMIT_USER_DIET_TYPE = 100

def get_all_user_diet_types(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_USER_DIET_TYPE):
    return db.query(model.UserDietType).offset(skip).limit(limit).all()

def get_user_diet_type(user_id: int, db: Session):
    return db.query(model.UserDietType)\
        .filter(model.UserDietType.user_id == user_id)\
        .all()

def check_exit_user_diet_type(user_diet_type: schema.UserDietTypeCreate, db: Session):
    return db.query(model.UserDietType)\
        .filter(and_(
            model.UserDietType.user_id == user_diet_type.user_id,
            model.UserDietType.diet_type_id == user_diet_type.diet_type_id,
        )).first()

def check_duplicate(user_diet_type: schema.UserDietTypeCreate, db: Session):
    exited_row = check_exit_user_diet_type(user_diet_type, db)

    if exited_row is not None:
        raise HTTPException(status_code=400, detail="Duplicate user diet type")

def create_user_diet_type(user_diet_type: schema.UserDietTypeCreate, db: Session):
    check_duplicate(user_diet_type, db)

    db_user_diet_type = model.UserDietType(**user_diet_type.dict())
    db.add(db_user_diet_type)
    db.commit()
    db.refresh(db_user_diet_type)
    return db_user_diet_type