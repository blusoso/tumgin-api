from sqlalchemy.orm import Session
from . import model, schema
from sqlalchemy import and_
from fastapi import HTTPException

DEFAULT_LIMIT_DIRECTION = 100


def get_directions(db: Session, skip: int = 0, limit: int = DEFAULT_LIMIT_DIRECTION):
    return db.query(model.Direction)\
        .filter(model.Direction.is_active == True)\
        .filter(model.Direction.deleted_at == None)\
        .offset(skip)\
        .limit(limit)\
        .all()


def check_exit_direction(direction: schema.DirectionCreate, db: Session):
    return db.query(model.Direction)\
        .filter(and_(
            model.Direction.recipe_id == direction.recipe_id,
            model.Direction.step_number == direction.step_number,
            model.Direction.description == direction.description,
        )).first()


def check_direction_duplicate(direction: schema.DirectionCreate, db: Session):
    exited_row = check_exit_direction(direction, db)

    if exited_row is not None:
        raise HTTPException(status_code=400, detail="Duplicate direction")


def get_last_step_number_row(recipe_id: int, db: Session):
    return db.query(model.Direction)\
        .filter(model.Direction.recipe_id == recipe_id)\
        .filter(model.Direction.is_active == True)\
        .filter(model.Direction.deleted_at == None)\
        .order_by(model.Direction.step_number.desc())\
        .first()


def create_direction(direction: schema.DirectionCreate, db: Session):
    check_direction_duplicate(direction, db)
    last_step_number_row = get_last_step_number_row(direction.recipe_id, db)

    step_number = 1

    if last_step_number_row is not None:
        step_number = last_step_number_row.step_number + 1

    direction.step_number = step_number

    db_direction = model.Direction(**direction.dict())
    db.add(db_direction)
    db.commit()
    db.refresh(db_direction)

    return db_direction
