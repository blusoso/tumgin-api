from typing import List
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from fastapi.security import OAuth2PasswordBearer

API_PREFIX = "/api"
ROUTE_PREFIX_V1 = "/v1"
FOOD_ROUTE_PREFIX_V1 = '/food'

config = Config(".env")

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)

# Authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='api/v1/auth/token')
JWT_SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DEFAULT_TOKEN_EXPIRE_MINUTES = 15
