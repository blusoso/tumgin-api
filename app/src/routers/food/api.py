from fastapi import APIRouter

from ...config import FOOD_ROUTE_PREFIX_V1
from . import recipe, tag, recipe_tag, ingredient, recipe_ingredient, direction, user_like_recipe, review, recipe_img, search

router = APIRouter()


def include_api_routes():
    router.include_router(recipe.router, prefix=FOOD_ROUTE_PREFIX_V1)
    router.include_router(tag.router, prefix=FOOD_ROUTE_PREFIX_V1)
    router.include_router(recipe_tag.router, prefix=FOOD_ROUTE_PREFIX_V1)
    router.include_router(ingredient.router, prefix=FOOD_ROUTE_PREFIX_V1)
    router.include_router(direction.router, prefix=FOOD_ROUTE_PREFIX_V1)
    router.include_router(review.router, prefix=FOOD_ROUTE_PREFIX_V1)
    router.include_router(search.router, prefix=FOOD_ROUTE_PREFIX_V1)

    router.include_router(recipe_ingredient.router,
                          prefix=FOOD_ROUTE_PREFIX_V1)
    router.include_router(user_like_recipe.router,
                          prefix=FOOD_ROUTE_PREFIX_V1)
    router.include_router(recipe_img.router,
                          prefix=FOOD_ROUTE_PREFIX_V1)


include_api_routes()
