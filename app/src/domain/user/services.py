import re
import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from jwt.exceptions import DecodeError, ExpiredSignatureError

from ...config import JWT_SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, DEFAULT_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from . import schema, model
from ..token.access_token.model import AccessToken
from ..token.refresh_token.model import RefreshToken

PASSWORD_MIN_LENGTH = 8

def get_user_by_id(id, db: Session):
    return db.query(model.User).filter(model.User.id == id).first()


def get_user_by_username(username: str, db: Session):
    return db.query(model.User).filter(model.User.username == username).first()

def get_user_by_email(email: str, db: Session):
    return db.query(model.User).filter(model.User.email == email).first()


def verify_password(plain_password: str, password_hash: str):
    return bcrypt.verify(plain_password, password_hash)

def check_email_format(email: str):
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise HTTPException(status_code=400, detail="Email ไม่ถูกต้อง")

def check_password_length(password: str):
    if len(password) < PASSWORD_MIN_LENGTH:
        raise HTTPException(status_code=400, detail=f'Password ต้องมีอย่าางน้อย {PASSWORD_MIN_LENGTH} ตัวอักษร')

def check_username_exist(username: str, db: Session):
    if (get_user_by_username(username, db) is not None):
        raise HTTPException(status_code=400, detail="Username นี้เคยใช้ไปแล้ว")

def check_email_exist(email: str, db: Session):
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ไม่พบ Email นี้ในระบบ"
        )
    return user

def check_email(email: str, db:Session):
    if (get_user_by_email(email, db) is not None):
        raise HTTPException(status_code=400, detail="Email นี้เคยใช้ไปแล้ว")

def validate_create_user_form(user: schema.UserCreate, db: Session):
    if user.login_with == 'site':
        check_password_length(user.password)

    check_email_format(user.email)
    check_username_exist(user.username, db)
    check_email(user.email, db)

def create_user(user: schema.UserCreate, db: Session):
    password_hash = ''
    if user.login_with == 'site':
        password_hash = bcrypt.hash(user.password)

    validate_create_user_form(user, db)

    db_user = model.User(
        username=user.username,
        password_hash=password_hash,
        email=user.email,
        gender=user.gender,
        profile_img=user.profile_img,
        login_with=user.login_with,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_social_user(email: str, db: Session):
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ไม่พบ Email นี้ในระบบ"
        )
    return user

def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(email, db)
    if user and user.password_hash is not None and user.login_with == 'site':
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=400, detail="รหัสผ่านไม่ถูกต้อง")

        return user
    else:
       raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email หรือ Password ไม่ถูกต้อง',
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_access_token_by_user_id(user_id: int, db: Session):
    return db.query(AccessToken).filter(AccessToken.user_id == user_id).first();

def is_user_exist_in_access_token(user_id: int, db: Session):
    user_exist = get_access_token_by_user_id(user_id, db)

    if (user_exist is not None):
        return True
    
    return False

def create_access_token(
    db: Session,
    user_id: int,
    data: dict(),
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=DEFAULT_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

    if not is_user_exist_in_access_token(user_id, db): 
        db_access_token = AccessToken(
            user_id=user_id,
            access_token=encoded_jwt,
            expired_at=expire
        )
        db.add(db_access_token)
        db.commit()
        db.refresh(db_access_token)
    else:
        db_access_token_exist = get_access_token_by_user_id(user_id, db)
        db_access_token_exist.access_token = encoded_jwt
        db_access_token_exist.expired_at = expire
        db_access_token_exist.deleted_at = None
        db.commit()
        db.refresh(db_access_token_exist)

    return encoded_jwt

def get_refresh_token_by_user_id(user_id: int, db: Session):
    return db.query(RefreshToken).filter(RefreshToken.user_id == user_id).first();

def is_user_exist_in_refresh_token(user_id: int, db: Session):
    user_exist = get_refresh_token_by_user_id(user_id, db)

    if (user_exist is not None):
        return True
    
    return False

def create_refresh_token(
    db: Session,
    user_id: int,
    data: dict(),
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

    if not is_user_exist_in_refresh_token(user_id, db): 
        db_refresh_token = RefreshToken(
            user_id=user_id,
            refresh_token=encoded_jwt,
            expired_at=expire
        )
        db.add(db_refresh_token)
        db.commit()
        db.refresh(db_refresh_token)
    else:
        db_refresh_token_exist = get_refresh_token_by_user_id(user_id, db)
        db_refresh_token_exist.refresh_token = encoded_jwt
        db_refresh_token_exist.expired_at = expire
        db_refresh_token_exist.deleted_at = None
        db.commit()
        db.refresh(db_refresh_token_exist)

    return encoded_jwt

def refresh_access_token(refresh_token: dict(), db=Session):
    try:
        to_encode = refresh_token.copy()
        decoded_token = jwt.decode(to_encode.refresh_token, JWT_SECRET, algorithms=ALGORITHM)
        if "refresh" in decoded_token:
            user_id = decoded_token["sub"]
            
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            new_access_token = create_access_token(
                db=db,
                user_id=user_id,
                data={"sub": user_id},
                expires_delta=access_token_expires
            )
            return new_access_token
        else:
            return None
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_token(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=ALGORITHM)
        if decoded_token["exp"] < datetime.utcnow().timestamp():
            raise ExpiredSignatureError
        return decoded_token
    except DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

def get_current_user(token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_id: int = token.get("sub")
        user = get_user_by_id(user_id, db)

        if user is not None:
            return user
        else:
            raise credentials_exception

    except (jwt.JWTError, Exception):
        raise credentials_exception


def get_current_active_user(current_user: schema.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
