from sqlalchemy.orm import Session
from . import model, schema

DEFAULT_LIMIT_REVIEW = 5


def get_reviews(db: Session, recipe_id: int, skip: int = 0, limit: int = DEFAULT_LIMIT_REVIEW):
    return db.query(model.Review)\
        .filter(model.Review.recipe_id == recipe_id)\
        .filter(model.Review.deleted_at == None)\
        .order_by(model.Review.id.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()


def create_review(review: schema.ReviewCreate, db: Session):
    db_review = model.Review(**review.dict())
    db.add(db_review)

    db.commit()
    db.refresh(db_review)

    return db_review
