"""Check scaffold readiness; does not claim analysis is complete."""
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "environment.yml", "LLM_USAGE.md", "CONTRIBUTING.md",
    "data/raw/.gitkeep", "data/processed/.gitkeep",
    "notebooks/01_collection_exploration.ipynb", "notebooks/02_analysis.ipynb",
    "notebooks/02A_duong_q1_q2.ipynb", "notebooks/02B_ha_q3_q4.ipynb",
    "notebooks/02C_ly_q5.ipynb", "notebooks/03_ml_question.ipynb",
    "docs/research_questions.md", "src/coupon_project/data_io.py",
    "reports/figures/.gitkeep", "reports/tables/.gitkeep",
]


def main() -> int:
    missing = [f for f in REQUIRED if not (ROOT / f).exists()]
    print("=== Kiểm tra cấu trúc CSC17104 starter ===")
    if missing:
        for f in missing:
            print(f"  [MISSING] {f}")
    else:
        print(f"  [OK] {len(REQUIRED)} tệp cấu trúc quan trọng")

    raw_path = ROOT / "data" / "raw" / "in-vehicle-coupon-recommendation.csv"
    if not raw_path.is_file():
        print("  [NEXT] Chưa có CSV gốc; chạy: python scripts/download_data.py")
    else:
        sys.path.insert(0, str(ROOT / "src"))
        try:
            from coupon_project.data_io import load_raw_data
            from coupon_project.quality import target_is_binary
            df = load_raw_data(raw_path)
            print(f"  [OK] Dataset: {len(df):,} rows, {len(df.columns)} columns")
            print(f"  [{'OK' if target_is_binary(df) else 'WARN'}] Target Y nhị phân (0/1)")
        except Exception as exc:
            print(f"  [WARN] Không kiểm tra được CSV: {exc}")
    print("  [NOTE] Đây là kiểm tra scaffold, không phải xác nhận hoàn thành đồ án.")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
