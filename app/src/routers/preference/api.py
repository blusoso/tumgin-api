from fastapi import APIRouter

from ...config import PREFERENCE_ROUTE_PREFIX_V1
from . import allergy, user_allergy, diet, user_diet

router = APIRouter()


def include_api_routes():
    router.include_router(allergy.router, prefix=PREFERENCE_ROUTE_PREFIX_V1)
    router.include_router(user_allergy.router, prefix=PREFERENCE_ROUTE_PREFIX_V1)
    router.include_router(diet.router, prefix=PREFERENCE_ROUTE_PREFIX_V1)
    router.include_router(user_diet.router, prefix=PREFERENCE_ROUTE_PREFIX_V1)


include_api_routes()
