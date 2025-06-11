from fastapi import APIRouter

from base.schema.requests import IngestRequest, QueryRequest

router = APIRouter()


@router.post("/ingest")
async def ingest_endpoint(req: IngestRequest): ...


@router.post("/classify")
async def classify_endpoint(req: IngestRequest): ...


@router.post("/context")
async def context_endpoint(req: QueryRequest): ...


@router.post("/knowledge")
async def knowledge_endpoint(req: IngestRequest): ...


@router.post("/preferences")
async def preferences_endpoint(req: IngestRequest): ...
