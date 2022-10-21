from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from jose import jwt, JWTError

from ...dependencies import get_db
from ...config import oauth2_scheme, JWT_SECRET, ALGORITHM, DEFAULT_TOKEN_EXPIRE_MINUTES
from . import schema, model


def create_user(user: schema.UserCreate, db: Session):
    password_hash = bcrypt.hash(user.password_hash)
    db_user = model.User(
        username=user.username,
        password_hash=password_hash,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(id: int, db: Session):
    return db.query(model.User).filter(model.User.id == id).first()


def get_user_by_username(username: str, db: Session):
    return db.query(model.User).filter(model.User.username == username).first()


def verify_password(plain_password: str, password_hash: str):
    return bcrypt.verify(plain_password, password_hash)


def authenticate_user(username: str, password: str, db: Session):
    user = get_user_by_username(username, db)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False

    return user


def create_access_token(data: dict(), expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=DEFAULT_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user_by_username(username=username, db=db)
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(current_user: schema.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
