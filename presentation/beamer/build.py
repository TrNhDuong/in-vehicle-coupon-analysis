"""Tạo hình từ output notebook, diễn đạt câu hỏi cho slide và biên dịch Beamer.

Chạy từ repo: python presentation/beamer/build.py --compile
Không thực thi hay chỉnh sửa notebook; không thay đổi dữ liệu hoặc mô hình.
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

# Nguyên văn bảng câu hỏi mới ở origin/final-ver2, commit 4c3e9db.
# Chỉ đồng bộ phần trình bày; notebook trong thư mục làm việc giữ nguyên.
SLIDE_QUESTIONS = {
    1: "Tỷ lệ nhận phiếu thay đổi thế nào theo thời gian lái xe đến quán và theo việc quán nằm cùng hay ngược hướng với điểm đến? Xu hướng này có giống nhau giữa các chuyến đi và các loại dịch vụ không?",
    2: "Phiếu có hạn một ngày hay hai giờ được chấp nhận nhiều hơn? Chênh lệch đó thay đổi thế nào theo giờ trong ngày và loại dịch vụ?",
    3: "Với cùng một loại dịch vụ, người thường xuyên ghé loại quán đó có dễ nhận phiếu ưu đãi hơn người ít ghé không?",
    4: "Với cùng loại phiếu và mục đích chuyến đi, người đi cùng bạn bè hoặc bạn đời có dễ nhận phiếu hơn người đi một mình không?",
    5: "Khi so sánh những người có thói quen ghé quán tương tự và nhận cùng loại phiếu, tỷ lệ chấp nhận còn khác nhau thế nào theo tuổi và thu nhập?",
    6: "Với thông tin có trước khi gửi phiếu, mô hình dự đoán ý định nhận phiếu của người mới tốt hơn bao nhiêu so với cách luôn đoán “đồng ý nhận”?",
}


def escape_tex(text):
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(c, c) for c in text)


def questions():
    path = ROOT / "notebooks/02_analysis.ipynb"
    notebook = json.loads(path.read_text(encoding="utf-8"))
    questions = {}
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
                questions[int(match[1])] = question
    assert set(questions) == set(range(1, 7))
    assert set(SLIDE_QUESTIONS) == set(questions)
    text = "% Nguyên văn 6 câu hỏi trong notebook 02 tại commit 4c3e9db (origin/final-ver2).\n"
    for number, question in sorted(SLIDE_QUESTIONS.items()):
        text += (rf"\expandafter\def\csname question{number}\endcsname"
                 + "{" + escape_tex(question) + "}\n")
    (HERE / "questions.tex").write_text(text, encoding="utf-8")
    return questions


def figures():
    from reference_visuals import build
    return build()


def compile_deck():
    engine = shutil.which("xelatex")
    if not engine:
        raise RuntimeError("Cần XeLaTeX (MiKTeX hoặc TeX Live) để biên dịch.")
    build = HERE / ".build"
    build.mkdir(exist_ok=True)
    command = [engine, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
               "-no-shell-escape", f"-output-directory={build}", "slides.tex"]
    for _ in range(2):
        subprocess.run(command, cwd=HERE, check=True)
    source = build / "slides.pdf"
    for dest in [HERE / "slides.pdf", HERE.parent / "slides.pdf", ROOT / "slides.pdf"]:
        shutil.copy2(source, dest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compile", action="store_true", help="Biên dịch PDF bằng XeLaTeX")
    args = parser.parse_args()
    protected = [*ROOT.glob("notebooks/*.ipynb"), ROOT / "data/raw/in-vehicle-coupon-recommendation.csv"]
    before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    text = questions()
    count = figures()
    if args.compile:
        compile_deck()
    assert before == {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    print(f"Đã đối chiếu {len(text)} câu hỏi gốc, tạo bản diễn đạt cho slide và {count} hình; notebook và CSV giữ nguyên.")


if __name__ == "__main__":
    main()
