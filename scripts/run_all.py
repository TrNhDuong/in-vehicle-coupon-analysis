"""Chạy kiểm chứng và thực thi toàn bộ pipeline bằng 1 lệnh (check -> pytest -> 01 -> 02 -> 03)."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT / "data" / "raw" / "in-vehicle-coupon-recommendation.csv"
NOTEBOOKS = [
    "notebooks/01_collection_exploration.ipynb",
    "notebooks/02_analysis.ipynb",
    "notebooks/03_ml_question.ipynb",
]


def run_step(cmd: list[str], label: str) -> None:
    print(f"\n=== {label} ===", flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    py = sys.executable
    run_step([py, "scripts/check_project.py"], "1. Kiểm tra cấu trúc dự án")
    run_step([py, "-m", "pytest", "-q"], "2. Chạy kiểm thử đơn vị (pytest)")

    raw_before = hashlib.sha256(RAW_CSV.read_bytes()).hexdigest()
    for nb_rel in NOTEBOOKS:
        run_step(
            [py, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", "--ExecutePreprocessor.timeout=300", nb_rel],
            f"3. Thực thi {nb_rel}",
        )
        nb = json.loads((ROOT / nb_rel).read_text(encoding="utf-8"))
        errs = [o for c in nb["cells"] if c["cell_type"] == "code" for o in c.get("outputs", []) if o.get("output_type") == "error"]
        if errs:
            raise RuntimeError(f"Phát hiện lỗi khi chạy {nb_rel}: {errs}")

    raw_after = hashlib.sha256(RAW_CSV.read_bytes()).hexdigest()
    if raw_before != raw_after:
        raise RuntimeError("Mã kiểm tra SHA-256 của CSV gốc bị thay đổi bất thường!")

    figs = len(list((ROOT / "reports" / "figures").glob("*.png")))
    tabs = len(list((ROOT / "reports" / "tables").glob("*.csv")))
    print(f"\n[OK] Hoàn tất toàn bộ kiểm tra và 3 notebook ({figs} biểu đồ, {tabs} bảng; SHA-256 CSV gốc giữ nguyên).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
