from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..dependencies import get_db
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from ..domain.user import schema, services

router = APIRouter(prefix='/auth', tags=["auth"])


@router.post('/signup', response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    user_created = services.create_user(user, db)
    return user_created


@router.post('/login', response_model=schema.Token)
def login_for_access_token(
    form_data: schema.UserLogin,
    db: Session = Depends(get_db)
):
    user = services.authenticate_user(
        form_data.email,
        form_data.password,
        db
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        db,
        user_id=user.id,
        data={"sub": user.id},
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = services.create_refresh_token(
        db,
        user_id=user.id,
        data={"sub": user.id,"refresh": True},
        expires_delta=refresh_token_expires
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }

@router.post("/refresh")
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    new_access_token = services.refresh_access_token(refresh_token, db)
    if new_access_token is None:
        return {"error": "Invalid refresh token"}
    return {"access_token": new_access_token}


@router.get('/users/me')
async def read_users_me(current_user: schema.User = Depends(services.get_current_active_user)):
    return current_user
