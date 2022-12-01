from sqlalchemy.orm import Session
from . import model, schema
from fastapi import HTTPException

DEFAULT_LIMIT_TAG = 100


def get_tags(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_TAG):
    return db.query(model.Tag).offset(skip).limit(limit).all()


def create_tag(tag: schema.TagCreate, db: Session):
    db_tag = model.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag
