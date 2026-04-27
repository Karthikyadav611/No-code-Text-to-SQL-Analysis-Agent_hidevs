from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database.connection import get_db
from services.query_service import query_service

router = APIRouter(prefix="/api", tags=["Query"])


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)


class QueryResponse(BaseModel):
    question: str
    sql: str
    row_count: int
    execution_time_ms: float
    limit_applied: bool
    columns: list[str]
    rows: list[dict[str, Any]]


@router.post("/query", response_model=QueryResponse)
def run_natural_language_query(
    payload: QueryRequest, db: Session = Depends(get_db)
) -> QueryResponse:
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        result = query_service.execute_user_query(db, question)
        return QueryResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
