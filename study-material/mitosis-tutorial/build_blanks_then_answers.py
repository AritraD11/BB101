"""Build 'Blanks then Answers' for the mitosis tutorial worksheet.

Output order: blank p1, answers p1, blank p2, answers p2, ...
Answers are overlaid in red bold on top of each blank, like the 12 Oct sheet.

Usage: python3 -I build.py <source.pdf> <output.pdf>
"""
import sys

import pymupdf

SRC, OUT = sys.argv[1], sys.argv[2]

RED = (0.76, 0.05, 0.12)
FONT = "tibo"        # Times-Bold
LABEL_FONT = "tibi"  # Times-BoldItalic

# Underlines inside the figures (pt): page index -> key -> (x0, x1, y)
IMG = {
    0: {"asexual": (101.2, 192.8, 229.5), "sexual": (313.2, 392.8, 229.0),
        "replicated": (323.2, 414.0, 526.5), "one": (122.8, 147.8, 708.0),
        "two_chrom": (334.8, 365.0, 708.0)},
    1: {"centrosomes": (243.8, 309.8, 263.8), "spindle_s": (432.5, 482.5, 267.0),
        "nucleolus": (158.0, 218.5, 597.8), "spindle_p": (181.4, 227.4, 621.0)},
    2: {"fragments": (217.8, 281.2, 155.2), "kineto": (172.5, 203.5, 205.8),
        "middle": (236.2, 266.2, 352.2), "metaphase": (231.0, 275.0, 373.5),
        "apart": (321.8, 363.5, 601.5)},
    3: {"decondense": (348.0, 395.2, 154.5), "reforms": (357.5, 407.8, 197.8)},
}

ANSWER = {
    "asexual": "Asexual", "sexual": "Sexual", "replicated": "Replicated",
    "one": "One", "two_chrom": "Two",
    "centrosomes": "Centrosomes", "spindle_s": "spindle",
    "nucleolus": "Nucleolus", "spindle_p": "spindle",
    "fragments": "fragments", "kineto": "kineto", "middle": "middle",
    "metaphase": "metaphase", "apart": "apart",
    "decondense": "decondense", "reforms": "reforms",
}

# Typed blanks on page 2 (underscore words in the text layer): answer -> (x0, x1, word-bbox y-centre)
TEXT_BLANKS = [
    ("Mitosis",  75.9, 144.8, 390.0),
    ("two",     313.8, 349.9, 427.9),
    ("daughter", 456.0, 482.9, 427.9),
    ("five",    211.8, 247.9, 450.7),
]

src = pymupdf.open(SRC)
out = pymupdf.open()
for i in range(len(src)):
    out.insert_pdf(src, from_page=i, to_page=i)   # blank
    out.insert_pdf(src, from_page=i, to_page=i)   # answers (marked up below)


def put(page, text, x0, x1, base, size=11.0, slack=0.96):
    """Centre `text` on [x0, x1] with baseline `base`, shrinking to fit."""
    avail = (x1 - x0) * slack
    w = pymupdf.get_text_length(text, fontname=FONT, fontsize=size)
    if w > avail:
        size = max(7.0, size * avail / w)
        w = pymupdf.get_text_length(text, fontname=FONT, fontsize=size)
    x = (x0 + x1) / 2 - w / 2
    page.insert_text((x, base), text, fontname=FONT, fontsize=size, color=RED)
    return pymupdf.Rect(x, base - size * 0.8, x + w, base + size * 0.2)


placed = []
for i in range(len(src)):
    ans = out[2 * i + 1]
    # label, top right (same place as the 12 Oct answer sheet)
    ans.insert_text((516, 30), "ANSWERS", fontname=LABEL_FONT, fontsize=9, color=RED)

    for key, (x0, x1, y) in IMG.get(i, {}).items():
        r = put(ans, ANSWER[key], x0, x1, y - 1.8)
        placed.append((i, ANSWER[key], r))

    if i == 1:
        sp = src[1]
        lines = [(l["bbox"], l["spans"][0]["origin"][1])
                 for b in sp.get_text("dict")["blocks"] if b["type"] == 0 for l in b["lines"]]
        for text, x0, x1, yc in TEXT_BLANKS:
            base = next(o for (bb, o) in lines if bb[1] <= yc <= bb[3]) - 1.8
            if text == "daughter":
                # The blank is only ~27 pt wide, squeezed between 'identical' and 'cells.'.
                # Put the answer just above it, in the empty gap between lines, with a leader mark.
                r = put(ans, text, x0 - 8, x1 + 8, base - 10.5, size=10.0, slack=1.0)
                cx = (x0 + x1) / 2
                ans.draw_line((cx, base - 7.0), (cx, base - 2.0), color=RED, width=0.9)
            else:
                r = put(ans, text, x0, x1, base)
            placed.append((i, text, r))

out.set_metadata({"title": "BB 101 Tutorial: Mitosis (blank page, then answers)",
                  "subject": "Answers based on Campbell Biology, Ch. 12", "author": ""})
out.save(OUT, garbage=3, deflate=True)
print("pages:", len(out), "| answers placed:", len(placed))
for p, t, r in placed:
    print(f"  src page {p+1}: {t:12} rect=({r.x0:6.1f},{r.y0:6.1f},{r.x1:6.1f},{r.y1:6.1f})")
