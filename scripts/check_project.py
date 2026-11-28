"""Kiểm tra cấu trúc dự án và tính hợp lệ cơ bản của dữ liệu gốc."""
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "pyproject.toml", "environment.yml", "requirements.txt", "LLM_USAGE.md",
    "docs/CONTRIBUTING.md", "docs/workflow_and_api.md", "docs/research_questions.md",
    "data/raw/.gitkeep", "data/processed/.gitkeep",
    "notebooks/01_collection_exploration.ipynb", "notebooks/02_analysis.ipynb",
    "notebooks/03_ml_question.ipynb",
    "src/coupon_project/data.py", "src/coupon_project/features.py", "src/coupon_project/stats.py",
    "src/coupon_project/plotting.py", "src/coupon_project/modeling.py",
    "scripts/run_all.py", "reports/figures/.gitkeep", "reports/tables/.gitkeep",
]

# In tiếng Việt an toàn cả khi output bị chuyển hướng ra file trên Windows (mặc định cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    missing = [f for f in REQUIRED if not (ROOT / f).exists()]
    print("=== Kiểm tra cấu trúc dự án CSC17104 ===")
    if missing:
        for f in missing:
            print(f"  [THIẾU] {f}")
    else:
        print(f"  [OK] Đủ {len(REQUIRED)} tệp cấu trúc quan trọng")

    raw_path = ROOT / "data" / "raw" / "in-vehicle-coupon-recommendation.csv"
    if not raw_path.is_file():
        print("  [TIẾP THEO] Chưa có CSV gốc; chạy: python scripts/download_data.py")
    else:
        if str(ROOT / "src") not in sys.path:
            sys.path.insert(0, str(ROOT / "src"))
        try:
            from coupon_project.data import load_raw_data, target_is_binary
            df = load_raw_data(raw_path)
            print(f"  [OK] Dữ liệu gốc: {len(df):,} dòng, {len(df.columns)} cột")
            status = "OK" if target_is_binary(df) else "CẢNH BÁO"
            print(f"  [{status}] Nhãn mục tiêu Y là nhị phân (0/1)")
        except Exception as exc:
            print(f"  [CẢNH BÁO] Không kiểm tra được CSV: {exc}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
