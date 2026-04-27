import io
import re
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy.engine import Engine

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def _normalize_column_names(columns: list[Any]) -> list[str]:
    seen: dict[str, int] = {}
    normalized: list[str] = []

    for index, raw_name in enumerate(columns, start=1):
        name = re.sub(r"[^a-zA-Z0-9]+", "_", str(raw_name).strip().lower()).strip("_")
        name = name or f"column_{index}"
        if name[0].isdigit():
            name = f"col_{name}"

        count = seen.get(name, 0) + 1
        seen[name] = count
        normalized.append(name if count == 1 else f"{name}_{count}")

    return normalized


def load_dataframe_from_upload(filename: str, raw_bytes: bytes) -> pd.DataFrame:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError("Only CSV and Excel files (.csv, .xlsx, .xls) are supported.")

    buffer = io.BytesIO(raw_bytes)

    if suffix == ".csv":
        dataframe = pd.read_csv(buffer)
    else:
        dataframe = pd.read_excel(buffer)

    if dataframe.empty:
        raise ValueError("Uploaded file has no data rows.")

    dataframe.columns = _normalize_column_names(list(dataframe.columns))
    return dataframe


def persist_dataframe(dataframe: pd.DataFrame, table_name: str, engine: Engine) -> None:
    sanitized = dataframe.where(pd.notnull(dataframe), None)
    sanitized.to_sql(table_name, con=engine, if_exists="replace", index=False, method="multi")


def dataframe_preview(dataframe: pd.DataFrame, limit: int = 5) -> list[dict[str, Any]]:
    sample = dataframe.head(limit)
    sample = sample.where(pd.notnull(sample), None)
    return sample.to_dict(orient="records")
