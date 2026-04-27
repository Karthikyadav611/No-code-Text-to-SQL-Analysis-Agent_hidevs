from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.connection import engine, get_db
from database.models import UploadedDataset
from services.upload_service import dataframe_preview, load_dataframe_from_upload, persist_dataframe
from utils.table_name import generate_table_name

router = APIRouter(prefix="/api", tags=["Upload"])


class UploadResponse(BaseModel):
    table_name: str
    row_count: int
    columns: list[str]
    preview: list[dict[str, Any]]


@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)) -> UploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="A valid file name is required.")

    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        dataframe = load_dataframe_from_upload(file.filename, raw_bytes)
        table_name = generate_table_name(file.filename)
        persist_dataframe(dataframe, table_name, engine)

        dataset_row = UploadedDataset(
            original_filename=file.filename,
            table_name=table_name,
            row_count=len(dataframe),
        )
        db.add(dataset_row)
        db.commit()

        return UploadResponse(
            table_name=table_name,
            row_count=len(dataframe),
            columns=list(dataframe.columns),
            preview=dataframe_preview(dataframe),
        )
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error during upload: {exc}") from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected upload error: {exc}") from exc
