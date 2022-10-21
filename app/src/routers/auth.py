from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..dependencies import get_db
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..domain.user import schema, services

router = APIRouter(prefix='/auth', tags=["auth"])


@router.post('/signup', response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    user_created = services.create_user(user, db)
    return user_created


@router.post('/token', response_model=schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = services.authenticate_user(
        form_data.username,
        form_data.password,
        db
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/users/me')
async def read_users_me(current_user: schema.User = Depends(services.get_current_active_user)):
    return current_user
