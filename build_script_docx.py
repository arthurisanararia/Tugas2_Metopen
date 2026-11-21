# -*- coding: utf-8 -*-
"""
Konversi SCRIPT_Presentasi_dan_QnA.md -> .docx (rapi untuk dibaca/ dicetak).
Jalankan: python build_script_docx.py
"""
import os
import re

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "SCRIPT_Presentasi_dan_QnA.md")
OUT = os.path.join(HERE, "SCRIPT_Presentasi_dan_QnA.docx")

NAVY = RGBColor(0x0F, 0x2A, 0x44)
TEAL = RGBColor(0x0E, 0x9F, 0x8E)
AMBER = RGBColor(0xB5, 0x74, 0x0F)
GRAY = RGBColor(0x6B, 0x7A, 0x8A)
RED = RGBColor(0xC9, 0x46, 0x3D)


def shade(par, hex_fill):
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear")
    el.set(qn("w:fill"), hex_fill)
    par._p.get_or_add_pPr().append(el)


def add_runs(par, text, size=11, color=None, base_bold=False):
    """Pecah **bold**, `code`, dan [SLIDE n] jadi run berformat."""
    tokens = re.split(r"(\*\*.+?\*\*|\*[^*\n]+\*|`[^`]+`|\[SLIDE[^\]]*\])", text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            inner = tok[2:-2]
            for part in re.split(r"(`[^`]+`)", inner):
                if not part:
                    continue
                if part.startswith("`") and part.endswith("`"):
                    r = par.add_run(part[1:-1])
                    r.font.name = "Consolas"
                    r.font.size = Pt(size - 1.5)
                    r.font.color.rgb = TEAL
                    r.bold = True
                else:
                    r = par.add_run(part)
                    r.bold = True
                    r.font.size = Pt(size)
                    r.font.name = "Calibri"
                    if color is not None:
                        r.font.color.rgb = color
            continue
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            r = par.add_run(tok[1:-1])
            r.italic = True
        elif tok.startswith("`") and tok.endswith("`"):
            r = par.add_run(tok[1:-1])
            r.font.name = "Consolas"
            r.font.size = Pt(size - 1.5)
            r.font.color.rgb = TEAL
            continue
        elif tok.startswith("[SLIDE"):
            r = par.add_run(tok)
            r.bold = True
            r.font.color.rgb = AMBER
            continue
        else:
            r = par.add_run(tok)
            r.bold = base_bold
        r.font.size = Pt(size)
        r.font.name = "Calibri"
        if color is not None:
            r.font.color.rgb = color


def main():
    with open(SRC, encoding="utf-8") as f:
        lines = f.read().splitlines()

    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(1.9)
    sec.bottom_margin = Cm(1.9)
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(1.8)

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    style.paragraph_format.space_after = Pt(4)

    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        line = raw.rstrip()

        # ---- tabel
        if line.startswith("|"):
            rows = []
            while i < n and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            if rows:
                cols = max(len(r) for r in rows)
                t = doc.add_table(rows=0, cols=cols)
                t.style = "Table Grid"
                t.alignment = WD_TABLE_ALIGNMENT.CENTER
                for ri, row in enumerate(rows):
                    cells = t.add_row().cells
                    for ci in range(cols):
                        txt = row[ci] if ci < len(row) else ""
                        p = cells[ci].paragraphs[0]
                        p.paragraph_format.space_after = Pt(1)
                        add_runs(p, txt, size=9.5, base_bold=(ri == 0))
                        if ri == 0:
                            shade(p, "0F2A44")
                            for r in p.runs:
                                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                doc.add_paragraph()
            continue

        # ---- heading
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            text = line.lstrip("#").strip()
            if level == 1:
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(2)
                add_runs(p, text, size=20, color=NAVY, base_bold=True)
            elif level == 2:
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(14)
                p.paragraph_format.space_after = Pt(4)
                add_runs(p, text, size=14, color=NAVY, base_bold=True)
                pbdr = OxmlElement("w:pBdr")
                bottom = OxmlElement("w:bottom")
                bottom.set(qn("w:val"), "single")
                bottom.set(qn("w:sz"), "8")
                bottom.set(qn("w:color"), "0E9F8E")
                pbdr.append(bottom)
                p._p.get_or_add_pPr().append(pbdr)
            else:
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(10)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.keep_with_next = True
                add_runs(p, text, size=12, color=TEAL, base_bold=True)
            i += 1
            continue

        # ---- garis pemisah
        if re.fullmatch(r"-{3,}", line.strip()):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            pPr = p._p.get_or_add_pPr()
            pbdr = OxmlElement("w:pBdr")
            bottom = OxmlElement("w:bottom")
            bottom.set(qn("w:val"), "single")
            bottom.set(qn("w:sz"), "4")
            bottom.set(qn("w:color"), "D9DEE4")
            pbdr.append(bottom)
            pPr.append(pbdr)
            i += 1
            continue

        # ---- kutipan / catatan
        if line.startswith(">"):
            text = line.lstrip("> ").strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.4)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            add_runs(p, text, size=10, color=NAVY)
            shade(p, "FDF4E3")
            i += 1
            continue

        # ---- checklist
        m = re.match(r"^\s*-\s*\[( |x|X)\]\s*(.+)$", line)
        if m:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.5)
            p.paragraph_format.space_after = Pt(2)
            mark = "\u2611  " if m.group(1).lower() == "x" else "\u2610  "
            r = p.add_run(mark)
            r.font.size = Pt(11)
            r.font.color.rgb = TEAL
            add_runs(p, m.group(2), size=10.5)
            i += 1
            continue

        # ---- bullet biasa
        if re.match(r"^\s*[-*]\s+", line):
            text = re.sub(r"^\s*[-*]\s+", "", line)
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
            add_runs(p, text, size=10.5)
            i += 1
            continue

        # ---- paragraf biasa
        if line.strip():
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_runs(p, line.strip(), size=11)
            if "[SLIDE" in line:
                p.paragraph_format.keep_with_next = True
                p.paragraph_format.space_before = Pt(10)
                p.paragraph_format.space_after = Pt(2)
            i += 1
            continue

        i += 1

    doc.save(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    main()
