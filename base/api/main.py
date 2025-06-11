from fastapi import APIRouter

from base.api.routes import ingest, retrieve

api_router = APIRouter()
api_router.include_router(ingest.router)
api_router.include_router(retrieve.router)
