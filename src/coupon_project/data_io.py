"""Simple I/O helpers; no transformations or research findings included."""
from pathlib import Path
import pandas as pd
from .config import RAW_CSV_PATH, REQUIRED_COLUMNS


def load_raw_data(path: str | Path = RAW_CSV_PATH) -> pd.DataFrame:
    """Read raw CSV and guard against wrong file/schema.

    This function deliberately does not fill nulls, remove duplicates,
    encode features, or fit any analysis method.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(
            f"Chưa có dữ liệu: {path}. Hãy chạy python scripts/download_data.py "
            "từ repo root, hoặc đặt CSV vào data/raw/."
        )
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"CSV thiếu các cột dự kiến: {sorted(missing)}")
    return df


def row_count_log(before: int, after: int, action: str) -> str:
    """Format a transparent row-count log for cleaning decisions."""
    if before < 0 or after < 0:
        raise ValueError("Row counts cannot be negative")
    return f"{action}: {before:,} -> {after:,} rows (delta {after-before:+,})"
