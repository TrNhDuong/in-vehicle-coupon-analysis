"""Execute only Ha's two notebooks from fresh kernels and verify raw integrity."""
from __future__ import annotations

import hashlib
import asyncio
import os
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/in-vehicle-coupon-recommendation.csv"
NOTEBOOKS = ["01_collection_exploration.ipynb", "02B_ha_q3_q4.ipynb"]


def main():
    if not RAW.is_file():
        raise SystemExit("Run python scripts/download_data.py first")
    initial = hashlib.sha256(RAW.read_bytes()).hexdigest()
    # Keep Jupyter runtime files inside the project rather than the user profile.
    runtime = ROOT / ".jupyter_runtime"
    runtime.mkdir(exist_ok=True)
    os.environ["JUPYTER_RUNTIME_DIR"] = str(runtime)
    os.environ["IPYTHONDIR"] = str(runtime / "ipython")
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    for name in NOTEBOOKS:
        path = ROOT / "notebooks" / name
        notebook = nbformat.read(path, as_version=4)
        print(f"Executing {name}", flush=True)
        NotebookClient(notebook, timeout=240, kernel_name="python3",
                       resources={"metadata": {"path": str(ROOT)}}).execute()
        nbformat.write(notebook, path)
        assert hashlib.sha256(RAW.read_bytes()).hexdigest() == initial, "Raw CSV changed"
        print(f"OK: {name}", flush=True)
    print(f"Raw SHA-256 unchanged: {initial}", flush=True)


if __name__ == "__main__":
    main()
