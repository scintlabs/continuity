from fastapi import APIRouter

from base.api import routes

api_router = APIRouter()
api_router.include_router(routes.router)
