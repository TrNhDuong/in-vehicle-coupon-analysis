"""Project paths, raw CSV schema contract, quality audits, and I/O helpers."""
from pathlib import Path
import pandas as pd

def _find_root() -> Path:
    for start in (Path(__file__).resolve(), Path.cwd().resolve()):
        for parent in (start, *start.parents):
            if (parent / "pyproject.toml").is_file() and (parent / "src").is_dir():
                return parent
    return Path(__file__).resolve().parents[2]


PROJECT_ROOT = _find_root()
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
RAW_CSV_PATH = DATA_RAW_DIR / "in-vehicle-coupon-recommendation.csv"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
TABLES_DIR = PROJECT_ROOT / "reports" / "tables"
TARGET = "Y"

REQUIRED_COLUMNS = {
    "destination", "passanger", "weather", "temperature", "time",
    "coupon", "expiration", "age", "income", "Bar", "CoffeeHouse",
    "CarryAway", "RestaurantLessThan20", "Restaurant20To50",
    "toCoupon_GEQ15min", "toCoupon_GEQ25min", "direction_same", "Y",
}


def load_raw_data(path: str | Path = RAW_CSV_PATH) -> pd.DataFrame:
    """Read raw CSV and verify required schema without modifying rows or nulls."""
    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError(
            f"Chưa có dữ liệu: {csv_path}. Chạy `python scripts/download_data.py` "
            "từ repo root hoặc đặt CSV vào data/raw/."
        )
    df = pd.read_csv(csv_path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"CSV thiếu các cột dự kiến: {sorted(missing)}")
    return df


def row_count_log(before: int, after: int, action: str) -> str:
    """Format a transparent row-count log for filtering/cleaning actions."""
    if before < 0 or after < 0:
        raise ValueError("Row counts cannot be negative")
    return f"{action}: {before:,} -> {after:,} rows (delta {after - before:+,})"


def audit_row(action: str, before: int, after: int, reason: str) -> dict:
    """Build a structured row-count audit record."""
    return {
        "action": action, "n_before": before, "n_after": after,
        "rows_removed": before - after, "reason": reason,
    }


def missing_table(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize missing counts and percentages sorted descending."""
    if len(df) == 0:
        return pd.DataFrame({"missing_count": 0, "missing_pct": 0.0}, index=df.columns)
    return pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_pct": df.isna().mean().mul(100).round(2),
    }).sort_values("missing_pct", ascending=False)


def target_is_binary(df: pd.DataFrame, target: str = TARGET) -> bool:
    """Return True when target exists, has no nulls, and takes only 0/1."""
    if target not in df.columns:
        return False
    vals = df[target]
    return bool(vals.notna().all() and vals.isin([0, 1]).all())


def save_table(df: pd.DataFrame, name: str, out_dir: Path = TABLES_DIR) -> Path:
    """Write a summary table as UTF-8 CSV into reports/tables/."""
    path = Path(out_dir) / f"{name}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path
