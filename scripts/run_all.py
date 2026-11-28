"""Chạy kiểm chứng và thực thi toàn bộ pipeline bằng 1 lệnh (check -> pytest -> 01 -> 02 -> 03)."""
from __future__ import annotations
import hashlib
import json
import os
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
CELL_TIMEOUT = 600  # giây cho mỗi cell (cell GridSearchCV của Q6 là cell chạy lâu nhất)

# In tiếng Việt an toàn cả khi output bị chuyển hướng ra file trên Windows (mặc định cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CHILD_ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def run_step(cmd: list[str], label: str) -> None:
    print(f"\n=== {label} ===", flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True, env=CHILD_ENV)


def notebook_errors(nb_rel: str) -> list[dict]:
    """Trả về danh sách output lỗi (output_type == "error") trong notebook đã thực thi."""
    nb = json.loads((ROOT / nb_rel).read_text(encoding="utf-8"))
    return [
        out
        for cell in nb["cells"] if cell["cell_type"] == "code"
        for out in cell.get("outputs", []) if out.get("output_type") == "error"
    ]


def main() -> int:
    py = sys.executable
    run_step([py, "scripts/check_project.py"], "1. Kiểm tra cấu trúc dự án")
    run_step([py, "-m", "pytest", "-q"], "2. Chạy kiểm thử đơn vị (pytest)")

    raw_before = hashlib.sha256(RAW_CSV.read_bytes()).hexdigest()
    for nb_rel in NOTEBOOKS:
        # Gọi "python -m nbconvert" (không qua file jupyter-nbconvert.exe) để chạy được cả trên
        # Windows bật Smart App Control
        cmd = [py, "-m", "nbconvert", "--to", "notebook", "--execute", "--inplace",
               f"--ExecutePreprocessor.timeout={CELL_TIMEOUT}", nb_rel]
        run_step(cmd, f"3. Thực thi {nb_rel}")
        errs = notebook_errors(nb_rel)
        if errs:
            raise RuntimeError(f"Phát hiện lỗi khi chạy {nb_rel}: {errs}")

    raw_after = hashlib.sha256(RAW_CSV.read_bytes()).hexdigest()
    if raw_before != raw_after:
        raise RuntimeError("Mã kiểm tra SHA-256 của CSV gốc bị thay đổi bất thường!")

    figs = len(list((ROOT / "reports" / "figures").glob("*.png")))
    tabs = len(list((ROOT / "reports" / "tables").glob("*.csv")))
    print(f"\n[OK] Hoàn tất toàn bộ kiểm tra và 3 notebook ({figs} biểu đồ, {tabs} bảng; "
          "SHA-256 CSV gốc giữ nguyên).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
