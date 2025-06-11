from pydantic import BaseModel


class IngestRequest(BaseModel):
    text: str
    type: str = "message"


class QueryRequest(BaseModel):
    text: str
    k: int = 8
    type: str | None = None
