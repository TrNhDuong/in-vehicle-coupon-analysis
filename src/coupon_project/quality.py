"""Low-level checks to support (not replace) human data exploration."""
import pandas as pd


def missing_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Return counts and percentages; does not impute anything."""
    if len(frame) == 0:
        return pd.DataFrame({"missing_count": 0, "missing_pct": 0.0}, index=frame.columns)
    return pd.DataFrame({
        "missing_count": frame.isna().sum(),
        "missing_pct": frame.isna().mean().mul(100).round(2),
    }).sort_values("missing_pct", ascending=False)


def target_is_binary(frame: pd.DataFrame, target: str = "Y") -> bool:
    """Check whether all observed target values are 0/1 and none is missing."""
    if target not in frame.columns:
        return False
    target_values = frame[target]
    return target_values.notna().all() and target_values.isin([0, 1]).all()
