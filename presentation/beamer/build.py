"""Tạo 17 biểu đồ vector PDF từ output notebook, đồng bộ 6 câu hỏi và biên dịch slide Beamer.

Chạy từ thư mục gốc repo: python presentation/beamer/build.py --compile
Không thực thi hay chỉnh sửa notebook; không thay đổi dữ liệu gốc hoặc mô hình.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def escape_tex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(c, c) for c in text)


def questions() -> dict[int, str]:
    """Đọc nguyên văn 6 câu hỏi nghiên cứu từ notebooks/02_analysis.ipynb và ghi questions.tex."""
    path = ROOT / "notebooks/02_analysis.ipynb"
    notebook = json.loads(path.read_text(encoding="utf-8"))
    found = {}
    for cell in notebook["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        source = "".join(cell.get("source", []))
        if "## Danh sách câu hỏi nghiên cứu" not in source:
            continue
        for line in source.splitlines():
            match = re.match(r"\| \*\*Q([1-6])\*\* \|", line)
            if match:
                question = line.split("|")[3].strip()
                question = re.sub(r"\s*\*\(`03_ml_question.ipynb`\)\*", "", question)
                question = question.replace("`", "").strip()
                assert question.endswith("?"), question
                found[int(match[1])] = question
    assert set(found) == set(range(1, 7)), f"Thiếu câu hỏi trong notebook 02: {found.keys()}"
    text = "% Nguyên văn 6 câu hỏi nghiên cứu đồng bộ từ notebooks/02_analysis.ipynb.\n"
    for number, question in sorted(found.items()):
        text += (
            rf"\expandafter\def\csname question{number}\endcsname"
            + "{" + escape_tex(question) + "}\n"
        )
    (HERE / "questions.tex").write_text(text, encoding="utf-8")
    return found


def figures() -> int:
    from reference_visuals import build
    return build()


def compile_deck():
    engine = shutil.which("xelatex") or "/Library/TeX/texbin/xelatex"
    if not Path(engine).exists():
        raise RuntimeError("Cần XeLaTeX (MiKTeX hoặc TeX Live) để biên dịch.")
    build_dir = HERE / ".build"
    build_dir.mkdir(exist_ok=True)
    command = [
        engine, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
        "-no-shell-escape", f"-output-directory={build_dir}", "slides.tex",
    ]
    for _ in range(2):
        subprocess.run(command, cwd=HERE, check=True)
    shutil.copy2(build_dir / "slides.pdf", ROOT / "slides.pdf")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compile", action="store_true", help="Biên dịch slides.pdf bằng XeLaTeX")
    args = parser.parse_args()
    protected = [*ROOT.glob("notebooks/*.ipynb"), ROOT / "data/raw/in-vehicle-coupon-recommendation.csv"]
    before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    found = questions()
    count = figures()
    if args.compile:
        compile_deck()
    assert before == {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    print(f"Đã đồng bộ {len(found)} câu hỏi, dựng {count} hình vector và xuất slides.pdf; notebook/CSV giữ nguyên.")


if __name__ == "__main__":
    main()
