import re

FORBIDDEN_SQL_KEYWORDS = {
    "drop",
    "delete",
    "update",
    "alter",
    "truncate",
    "insert",
    "create",
    "replace",
    "grant",
    "revoke",
    "merge",
    "call",
    "execute",
    "exec",
    "load",
    "outfile",
}

SQL_COMMENT_PATTERN = re.compile(r"(--[^\n]*$)|(/\*.*?\*/)", flags=re.MULTILINE | re.DOTALL)


def _strip_comments(sql: str) -> str:
    return re.sub(SQL_COMMENT_PATTERN, " ", sql)


def _normalize_whitespace(sql: str) -> str:
    return re.sub(r"\s+", " ", sql).strip()


def validate_select_query(sql: str) -> tuple[bool, str]:
    cleaned = _normalize_whitespace(_strip_comments(sql or ""))

    if not cleaned:
        return False, "Generated SQL is empty."

    # Only allow one statement. A trailing semicolon is fine.
    if ";" in cleaned[:-1]:
        return False, "Multiple SQL statements are not allowed."

    if cleaned.endswith(";"):
        cleaned = cleaned[:-1].strip()

    lowered = cleaned.lower()

    if not (lowered.startswith("select") or lowered.startswith("with")):
        return False, "Only SELECT queries are allowed."

    for keyword in FORBIDDEN_SQL_KEYWORDS:
        if re.search(rf"\b{keyword}\b", lowered):
            return False, f"Forbidden keyword detected: {keyword.upper()}"

    # WITH clauses are allowed only when they eventually select data.
    if lowered.startswith("with") and "select" not in lowered:
        return False, "CTE queries must resolve to a SELECT statement."

    return True, cleaned
