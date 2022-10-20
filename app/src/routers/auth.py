from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter(prefix='/auth', tags=["auth"])


@router.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token': form_data.username + 'token'}


@router.get('/')
async def index(token: str = Depends(oauth2_scheme)):
    return {'the_token': token}
