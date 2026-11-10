"""Download the public UCI #603 CSV without changing its contents.

Usage (from project root): python scripts/download_data.py [--overwrite]
Source: https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation
License of upstream dataset: CC BY 4.0. This script does not grant a code license.
"""
from __future__ import annotations
import argparse
import hashlib
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile, BadZipFile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT_ROOT / "data" / "raw" / "in-vehicle-coupon-recommendation.csv"
URLS = [
    "https://archive.ics.uci.edu/static/public/603/in%2Bvehicle%2Bcoupon%2Brecommendation.zip",
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00603/in-vehicle-coupon-recommendation.csv",
]


def get_csv_bytes() -> tuple[bytes, str]:
    errors = []
    for url in URLS:
        try:
            req = Request(url, headers={"User-Agent": "CSC17104-Academic-Project/1.0"})
            with urlopen(req, timeout=35) as response:
                content = response.read()
            if url.lower().endswith(".zip"):
                with ZipFile(BytesIO(content)) as zf:
                    names = [name for name in zf.namelist() if name.lower().endswith(".csv")]
                    if not names:
                        raise ValueError("ZIP không chứa file CSV")
                    content = zf.read(names[0])  # read into memory; no path traversal
            if b"destination" not in content[:500] or b"Y" not in content[:500]:
                raise ValueError("File tải không giống UCI #603 CSV")
            return content, url
        except (OSError, ValueError, BadZipFile) as exc:
            errors.append(f"{url}: {exc}")
    raise RuntimeError(
        "Không tải được dữ liệu tự động. Truy cập trang UCI #603 và tải CSV thủ công."
        "\n" + "\n".join(errors)
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Download UCI #603 raw CSV")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing raw file")
    args = parser.parse_args()
    if OUTPUT.exists() and not args.overwrite:
        print(f"Đã tồn tại: {OUTPUT}; dùng --overwrite nếu thật sự muốn tải lại")
        return
    data, url = get_csv_bytes()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(data)
    sha = hashlib.sha256(data).hexdigest()
    print(f"Đã tải {len(data):,} bytes từ: {url}")
    print(f"Đã lưu: {OUTPUT}")
    print(f"SHA-256: {sha}")
    print("Giấy phép nguồn: CC BY 4.0 – vui lòng giữ ghi nhận nguồn UCI")


if __name__ == "__main__":
    main()
