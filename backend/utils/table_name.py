import re
import secrets
from datetime import datetime
from pathlib import Path


def generate_table_name(filename: str) -> str:
    # Keep table names SQL-safe and unique to avoid collisions between uploads.
    stem = Path(filename).stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "_", stem).strip("_")
    stem = stem or "dataset"
    if stem[0].isdigit():
        stem = f"t_{stem}"

    suffix = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    token = secrets.token_hex(2)
    return f"{stem[:40]}_{suffix}_{token}"[:64]
