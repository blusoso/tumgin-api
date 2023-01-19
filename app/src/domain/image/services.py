from sqlalchemy.orm import Session

from . import model, schema

DEFAULT_LIMIT_IMAGE = 100


def get_images(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_IMAGE):
    return db.query(model.Image)\
        .filter(model.Image.deleted_at == None)\
        .offset(skip)\
        .limit(limit)\
        .all()


def create_image(image: schema.ImageCreate, db: Session):
    db_image = model.Image(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
