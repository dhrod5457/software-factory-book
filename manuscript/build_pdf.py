#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
BOOK = ROOT / "book.md"
OUT_DIR = ROOT / "build"
OUT_DIR.mkdir(parents=True, exist_ok=True)

text = BOOK.read_text(encoding="utf-8")

# The PDF has its own title page and generated TOC. Drop working-copy front matter.
start = text.find("# 들어가며")
if start < 0:
    raise SystemExit("Could not find preface heading")
text = text[start:]

# Remove internal placement markers.
text = re.sub(r"^<!-- (?:FIGURE|CASE) [^\n]+ -->\n?", "", text, flags=re.M)

# Replace embedded Mermaid source with rendered PNGs.
figure_files = {}
for path in sorted((ROOT / "figures" / "rendered").glob("F*.png")):
    figure_files[path.name[:3]] = path

fig_re = re.compile(
    r"\*\*Figure (F\d+)\. ([^\n]+)\*\*\n\n"
    r"```mermaid\n.*?\n```\n\n"
    r"\*([^\n]+)\*",
    re.S,
)

def replace_figure(m):
    fid, title, caption = m.group(1), m.group(2).strip(), m.group(3).strip()
    path = figure_files.get(fid)
    if not path:
        raise RuntimeError(f"Rendered figure missing: {fid}")
    rel = path.relative_to(ROOT).as_posix()
    return (
        f"![Figure {fid}. {title}]({rel}){{ width=92% }}\n\n"
        f"*{caption}*"
    )

text, count = fig_re.subn(replace_figure, text)
if count != 21:
    raise RuntimeError(f"Expected 21 figures, replaced {count}")

# Part headings become real LaTeX parts.
part_re = re.compile(r"^# Part ([IVX]+)\. (.+)$", re.M)

def replace_part(m):
    title = m.group(2).replace("&", r"\&")
    return f"\\part{{{title}}}"

text = part_re.sub(replace_part, text)

# Numbered chapter headings are promoted one level for scrbook chapters.
text = re.sub(r"^## (\d+장\. .+)$", r"# \1", text, flags=re.M)
text = re.sub(r"^### (\d+\.\d+ .+)$", r"## \1", text, flags=re.M)

# Subheads inside numbered chapters are shifted consistently.
# Existing #### headings are chapter-level subsections.
text = re.sub(r"^#### (.+)$", r"### \1", text, flags=re.M)

# Drop horizontal-rule separators used only in the Markdown working copy.
text = re.sub(r"^---\s*$\n?", "", text, flags=re.M)

metadata = """---
title: "AI Software Factory"
subtitle: "코딩 에이전트를 소프트웨어 생산 시스템으로 운영하는 설계 원칙"
lang: ko-KR
documentclass: scrbook
classoption:
  - openany
geometry:
  - paperwidth=170mm
  - paperheight=240mm
  - inner=21mm
  - outer=18mm
  - top=20mm
  - bottom=22mm
mainfont: "Noto Serif CJK KR"
sansfont: "Noto Sans CJK KR"
monofont: "Noto Sans Mono CJK KR"
fontsize: 10.5pt
toc: true
toc-depth: 2
colorlinks: true
linkcolor: black
urlcolor: blue
---
"""

(OUT_DIR / "book-pdf.md").write_text(metadata + "\n" + text, encoding="utf-8")
print(f"wrote {OUT_DIR / 'book-pdf.md'}")
