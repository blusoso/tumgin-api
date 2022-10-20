from fastapi import APIRouter

from ..config import ROUTE_PREFIX_V1
from . import recipe, auth

router = APIRouter()


def include_api_routes():
    router.include_router(recipe.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(auth.router, prefix=ROUTE_PREFIX_V1)


include_api_routes()
