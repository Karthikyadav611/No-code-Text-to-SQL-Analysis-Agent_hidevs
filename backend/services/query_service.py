import re
from time import perf_counter
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.models import QueryHistory
from services.schema_service import format_schema_for_prompt, get_schema_map
from services.sql_generator import sql_generator_service
from utils.config import settings
from utils.serializers import serialize_value
from utils.sql_validator import validate_select_query


def _enforce_limit(sql: str, max_rows: int) -> tuple[str, bool]:
    if re.search(r"\blimit\b", sql, flags=re.IGNORECASE):
        return sql, False
    return f"{sql} LIMIT {max_rows}", True


class QueryService:
    def _save_history(
        self,
        db: Session,
        *,
        user_query: str,
        generated_sql: str,
        status: str,
        execution_time_ms: float | None = None,
        error_message: str | None = None,
    ) -> None:
        history_item = QueryHistory(
            user_query=user_query,
            generated_sql=generated_sql,
            status=status,
            execution_time_ms=execution_time_ms,
            error_message=error_message,
        )
        db.add(history_item)
        db.commit()

    def execute_user_query(self, db: Session, user_query: str) -> dict[str, Any]:
        schema_map = get_schema_map(db)
        schema_text = format_schema_for_prompt(schema_map)
        generated_sql = sql_generator_service.generate_sql(user_query, schema_text)

        is_valid, validation_message = validate_select_query(generated_sql)
        if not is_valid:
            self._save_history(
                db,
                user_query=user_query,
                generated_sql=generated_sql,
                status="blocked",
                error_message=validation_message,
            )
            raise ValueError(validation_message)

        safe_sql, limit_applied = _enforce_limit(validation_message, settings.max_result_rows)
        start_time = perf_counter()

        try:
            result = db.execute(text(safe_sql))
            columns = list(result.keys())
            rows = []
            for row in result:
                rows.append({key: serialize_value(value) for key, value in row._mapping.items()})

            execution_time_ms = round((perf_counter() - start_time) * 1000, 2)
            self._save_history(
                db,
                user_query=user_query,
                generated_sql=safe_sql,
                status="success",
                execution_time_ms=execution_time_ms,
            )

            return {
                "question": user_query,
                "sql": safe_sql,
                "row_count": len(rows),
                "execution_time_ms": execution_time_ms,
                "limit_applied": limit_applied,
                "columns": columns,
                "rows": rows,
            }
        except SQLAlchemyError as exc:
            execution_time_ms = round((perf_counter() - start_time) * 1000, 2)
            error_message = str(exc.__cause__ or exc)

            try:
                db.rollback()
                self._save_history(
                    db,
                    user_query=user_query,
                    generated_sql=safe_sql,
                    status="failed",
                    execution_time_ms=execution_time_ms,
                    error_message=error_message,
                )
            except SQLAlchemyError:
                db.rollback()

            raise RuntimeError(f"SQL execution failed: {error_message}") from exc


query_service = QueryService()
