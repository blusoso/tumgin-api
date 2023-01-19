from fastapi import APIRouter

from ..config import ROUTE_PREFIX_V1

from . import auth, image
from .food.api import router as food_router_api
from .preference.api import router as preference_router_api

router = APIRouter()


def include_api_routes():
    router.include_router(auth.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(image.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(food_router_api, prefix=ROUTE_PREFIX_V1)
    router.include_router(preference_router_api, prefix=ROUTE_PREFIX_V1)


include_api_routes()
