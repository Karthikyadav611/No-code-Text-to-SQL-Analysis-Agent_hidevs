from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import QueryHistory, UploadedDataset
from services.schema_service import format_schema_for_prompt, get_schema_map

router = APIRouter(prefix="/api", tags=["Metadata"])


@router.get("/schema")
def read_schema(db: Session = Depends(get_db)) -> dict[str, object]:
    schema_map = get_schema_map(db)
    return {
        "schema": schema_map,
        "schema_text": format_schema_for_prompt(schema_map),
    }


@router.get("/datasets")
def read_datasets(db: Session = Depends(get_db)) -> dict[str, list[dict[str, object]]]:
    datasets = (
        db.query(UploadedDataset)
        .order_by(desc(UploadedDataset.created_at))
        .all()
    )

    return {
        "datasets": [
            {
                "id": dataset.id,
                "original_filename": dataset.original_filename,
                "table_name": dataset.table_name,
                "row_count": dataset.row_count,
                "created_at": dataset.created_at.isoformat(),
            }
            for dataset in datasets
        ]
    }


@router.get("/history")
def read_history(
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> dict[str, list[dict[str, object]]]:
    history_rows = (
        db.query(QueryHistory)
        .order_by(desc(QueryHistory.created_at))
        .limit(limit)
        .all()
    )

    return {
        "history": [
            {
                "id": item.id,
                "user_query": item.user_query,
                "generated_sql": item.generated_sql,
                "execution_time_ms": item.execution_time_ms,
                "status": item.status,
                "error_message": item.error_message,
                "created_at": item.created_at.isoformat(),
            }
            for item in history_rows
        ]
    }
