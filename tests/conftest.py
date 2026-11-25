"""Pytest setup; package is editable-installed via pyproject.toml (fallback keeps src importable)."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
