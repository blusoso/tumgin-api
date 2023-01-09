from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import model, schema

DEFAULT_LIMIT_USER_ALLERGY = 100

def get_all_user_allergies(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_USER_ALLERGY):
    return db.query(model.UserAllergy).offset(skip).limit(limit).all()

def get_user_allergy(user_id: int, db: Session):
    return db.query(model.UserAllergy)\
        .filter(model.UserAllergy.user_id == user_id)\
        .all()

def check_exit_user_allergy(user_allergy: schema.UserAllergyCreate, db: Session):
    return db.query(model.UserAllergy)\
        .filter(and_(
            model.UserAllergy.user_id == user_allergy.user_id,
            model.UserAllergy.ingredient_id == user_allergy.ingredient_id,
        )).first()

def check_duplicate(user_allergy: schema.UserAllergyCreate, db: Session):
    exited_row = check_exit_user_allergy(user_allergy, db)

    if exited_row is not None:
        raise HTTPException(status_code=400, detail="Duplicate user allergy")

def create_user_allergy(user_allergy: schema.UserAllergyCreate, db: Session):
    check_duplicate(user_allergy, db)

    db_user_allergy = model.UserAllergy(**user_allergy.dict())
    db.add(db_user_allergy)
    db.commit()
    db.refresh(db_user_allergy)
    return db_user_allergy