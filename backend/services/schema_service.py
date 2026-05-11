from sqlalchemy import text
from sqlalchemy.orm import Session

from utils.config import settings

INTERNAL_TABLES = {"uploaded_datasets", "query_history"}


def _lower_key_map(row: dict[str, object]) -> dict[str, object]:
    return {str(key).lower(): value for key, value in row.items()}


def get_schema_map(db: Session) -> dict[str, list[dict[str, str]]]:
    query = text(
        """
        SELECT table_name, column_name, data_type, ordinal_position
        FROM information_schema.columns
        WHERE table_schema = :schema_name
        ORDER BY table_name, ordinal_position
        """
    )

    rows = db.execute(query, {"schema_name": settings.db_name}).mappings().all()
    schema_map: dict[str, list[dict[str, str]]] = {}

    for row in rows:
        normalized = _lower_key_map(dict(row))
        table_name = str(normalized.get("table_name", ""))
        if table_name in INTERNAL_TABLES:
            continue

        column_name = str(normalized.get("column_name", ""))
        if not table_name or not column_name:
            continue

        schema_map.setdefault(table_name, []).append(
            {"column": column_name, "data_type": str(normalized.get("data_type", ""))}
        )

    return schema_map


def _singularize(name: str) -> str:
    lowered = name.lower()
    if lowered.endswith("ies") and len(lowered) > 3:
        return lowered[:-3] + "y"
    if lowered.endswith("ses") and len(lowered) > 3:
        return lowered[:-2]
    if lowered.endswith("s") and len(lowered) > 1:
        return lowered[:-1]
    return lowered


def _get_declared_foreign_keys(db: Session) -> list[dict[str, str]]:
    query = text(
        """
        SELECT
            table_name AS child_table,
            column_name AS child_column,
            referenced_table_name AS parent_table,
            referenced_column_name AS parent_column
        FROM information_schema.key_column_usage
        WHERE table_schema = :schema_name
          AND referenced_table_name IS NOT NULL
        ORDER BY table_name, column_name
        """
    )

    rows = db.execute(query, {"schema_name": settings.db_name}).mappings().all()
    relationships: list[dict[str, str]] = []

    for row in rows:
        normalized = _lower_key_map(dict(row))
        child_table = str(normalized.get("child_table", ""))
        parent_table = str(normalized.get("parent_table", ""))
        if child_table in INTERNAL_TABLES or parent_table in INTERNAL_TABLES:
            continue
        if not child_table or not parent_table:
            continue

        child_column = str(normalized.get("child_column", ""))
        parent_column = str(normalized.get("parent_column", ""))
        if not child_column or not parent_column:
            continue

        relationships.append(
            {
                "child_table": child_table,
                "child_column": child_column,
                "parent_table": parent_table,
                "parent_column": parent_column,
                "source": "declared",
            }
        )

    return relationships


def _get_inferred_relationships(
    schema_map: dict[str, list[dict[str, str]]],
) -> list[dict[str, str]]:
    table_columns: dict[str, set[str]] = {
        table_name: {column["column"].lower() for column in columns}
        for table_name, columns in schema_map.items()
    }
    tables = list(schema_map.keys())
    inferred: list[dict[str, str]] = []

    for child_table in tables:
        child_columns = table_columns[child_table]
        for child_column in child_columns:
            if not child_column.endswith("_id"):
                continue

            prefix = child_column[:-3]
            for parent_table in tables:
                if parent_table == child_table:
                    continue

                parent_columns = table_columns[parent_table]
                parent_singular = _singularize(parent_table)
                table_match = parent_singular == prefix

                if not table_match:
                    continue

                parent_column_candidates = {"id", f"{parent_singular}_id", f"{parent_table}_id"}
                parent_column = next(
                    (
                        candidate
                        for candidate in parent_column_candidates
                        if candidate in parent_columns
                    ),
                    None,
                )

                if not parent_column:
                    continue

                inferred.append(
                    {
                        "child_table": child_table,
                        "child_column": child_column,
                        "parent_table": parent_table,
                        "parent_column": parent_column,
                        "source": "inferred",
                    }
                )

    return inferred


def get_table_relationships(
    db: Session,
    schema_map: dict[str, list[dict[str, str]]],
) -> list[dict[str, str]]:
    try:
        declared = _get_declared_foreign_keys(db)
    except Exception:
        # If metadata inspection fails due permissions/driver quirks,
        # continue with inferred relationships so querying still works.
        declared = []

    inferred = _get_inferred_relationships(schema_map)

    deduped: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for relationship in declared + inferred:
        key = (
            relationship["child_table"],
            relationship["child_column"],
            relationship["parent_table"],
            relationship["parent_column"],
        )

        # Declared relationships take precedence over inferred ones.
        if key not in deduped or relationship["source"] == "declared":
            deduped[key] = relationship

    return sorted(
        deduped.values(),
        key=lambda item: (
            item["child_table"],
            item["child_column"],
            item["parent_table"],
            item["parent_column"],
        ),
    )


def format_schema_for_prompt(
    schema_map: dict[str, list[dict[str, str]]],
    relationships: list[dict[str, str]] | None = None,
) -> str:
    if not schema_map:
        return "No user-uploaded tables are currently available."

    lines: list[str] = []
    for table_name, columns in schema_map.items():
        lines.append(f"Table {table_name}:")
        for column_info in columns:
            lines.append(f"- {column_info['column']} ({column_info['data_type']})")
        lines.append("")

    if relationships:
        lines.append("Detected table relationships:")
        for relationship in relationships:
            lines.append(
                "- "
                f"{relationship['child_table']}.{relationship['child_column']} -> "
                f"{relationship['parent_table']}.{relationship['parent_column']} "
                f"({relationship['source']})"
            )

    return "\n".join(lines).strip()
