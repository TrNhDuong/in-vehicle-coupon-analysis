"""One-command verification and full notebook pipeline runner (check -> pytest -> 01 -> 02 -> 03)."""
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
    run_step([py, "scripts/check_project.py"], "1. Project structure check")
    run_step([py, "-m", "pytest", "-q"], "2. Unit tests")

    raw_before = hashlib.sha256(RAW_CSV.read_bytes()).hexdigest()
    for nb_rel in NOTEBOOKS:
        run_step(
            [py, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", "--ExecutePreprocessor.timeout=300", nb_rel],
            f"3. Execute {nb_rel}",
        )
        nb = json.loads((ROOT / nb_rel).read_text(encoding="utf-8"))
        errs = [o for c in nb["cells"] if c["cell_type"] == "code" for o in c.get("outputs", []) if o.get("output_type") == "error"]
        if errs:
            raise RuntimeError(f"Execution errors found in {nb_rel}: {errs}")

    raw_after = hashlib.sha256(RAW_CSV.read_bytes()).hexdigest()
    if raw_before != raw_after:
        raise RuntimeError("Raw CSV checksum changed unexpectedly!")

    figs = len(list((ROOT / "reports" / "figures").glob("*.png")))
    tabs = len(list((ROOT / "reports" / "tables").glob("*.csv")))
    print(f"\n[OK] All checks and 3 notebooks completed cleanly ({figs} figures, {tabs} tables; raw SHA-256 unchanged).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
