from sqlalchemy.orm import Session
from . import model, schema

DEFAULT_LIMIT_USER_ALLERGY = 100

def get_all_user_allergies(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_USER_ALLERGY):
    return db.query(model.UserAllergy).offset(skip).limit(limit).all()

def create_user_allergy(user_allergy: schema.UserAllergyCreate, db: Session):
    db_user_allergy = model.UserAllergy(**user_allergy.dict())
    db.add(db_user_allergy)
    db.commit()
    db.refresh(db_user_allergy)
    return db_user_allergy