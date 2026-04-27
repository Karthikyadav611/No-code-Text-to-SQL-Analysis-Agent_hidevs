from sqlalchemy import text
from sqlalchemy.orm import Session

from utils.config import settings

# Tables you want to ignore internally
INTERNAL_TABLES = {"uploaded_datasets", "query_history"}


def get_schema_map(db: Session) -> dict[str, list[dict[str, str]]]:
    query = text(
        """
        SELECT table_name, column_name, data_type, ordinal_position
        FROM information_schema.columns
        WHERE table_schema = :schema_name
        ORDER BY table_name, ordinal_position
        """
    )

    # Execute query
    rows = db.execute(query, {"schema_name": settings.db_name}).mappings().all()

    schema_map: dict[str, list[dict[str, str]]] = {}

    for row in rows:
        # 🔥 FIX: normalize keys to lowercase (works across MySQL/Postgres/etc.)
        row = {k.lower(): v for k, v in row.items()}

        table_name = row["table_name"]

        # Skip internal tables
        if table_name in INTERNAL_TABLES:
            continue

        # Add columns to schema map
        schema_map.setdefault(table_name, []).append(
            {
                "column": row["column_name"],
                "data_type": row["data_type"]
            }
        )

    return schema_map


def format_schema_for_prompt(schema_map: dict[str, list[dict[str, str]]]) -> str:
    if not schema_map:
        return "No user-uploaded tables are currently available."

    lines: list[str] = []

    for table_name, columns in schema_map.items():
        lines.append(f"Table {table_name}:")

        for column_info in columns:
            lines.append(f"- {column_info['column']} ({column_info['data_type']})")

        lines.append("")  # blank line between tables

    return "\n".join(lines).strip()