from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .src.database import engine, Base
from .src.routers.api import router as router_api
from .src.config import ALLOWED_HOSTS, API_PREFIX


def get_application():
    application = FastAPI()

    Base.metadata.create_all(bind=engine)

    application.include_router(router_api, prefix=API_PREFIX)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = get_application()
