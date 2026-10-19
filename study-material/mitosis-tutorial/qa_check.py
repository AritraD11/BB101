"""QA for the 'blanks then answers' mitosis PDF.

Usage: python3 -I qa_check.py <source.pdf> <blanks_then_answers.pdf>

Checks
  * 8 pages = for each source page: blank copy, then answer copy; page sizes kept
  * blank copies look like the source (<= 3/255 per channel; the renderer shifts a
    few anti-aliased pixels) and carry the same images byte-for-byte
  * answer copies add exactly the 20 expected answers + one 'ANSWERS' label
  * every pixel that differs from the source lies inside an added word (plus a
    small margin for descenders / the leader tick), i.e. nothing else was touched
"""
import hashlib
import sys
from collections import Counter

import numpy as np
import pymupdf

SRC, OUT = sys.argv[1], sys.argv[2]
src, out = pymupdf.open(SRC), pymupdf.open(OUT)
Z = 2
M = pymupdf.Matrix(Z, Z)
ok = True


def chk(name, cond, extra=""):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + name + (" " + extra if extra else ""))


def px(page):
    pm = page.get_pixmap(matrix=M, colorspace=pymupdf.csRGB)
    return np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width, 3).astype(np.int16)


def img_hashes(doc, pno):
    return sorted(hashlib.sha1(doc.extract_image(im[0])["image"]).hexdigest()
                  for im in doc[pno].get_images(full=True))


EXPECT = {
    0: ["Asexual", "Sexual", "Replicated", "One", "Two"],
    1: ["Centrosomes", "spindle", "spindle", "Nucleolus", "Mitosis", "two", "daughter", "five"],
    2: ["fragments", "kineto", "middle", "metaphase", "apart"],
    3: ["decondense", "reforms"],
}

chk("8 pages", len(out) == 8, f"(got {len(out)})")
chk("page sizes kept", all(out[j].rect == src[j // 2].rect for j in range(len(out))))

for i in range(4):
    blank, ans = out[2 * i], out[2 * i + 1]

    # --- blank copy == source
    a, b = px(src[i]), px(blank)
    worst = int(np.abs(a - b).max())
    chk(f"p{2*i+1} blank copy matches source p{i+1}", worst <= 3, f"(max channel diff {worst}/255)")
    chk(f"p{2*i+1} images identical to source", img_hashes(src, i) == img_hashes(out, 2 * i))
    chk(f"p{2*i+1} text layer identical to source", src[i].get_text() == blank.get_text())
    chk(f"p{2*i+1} has no ANSWERS label", "ANSWERS" not in blank.get_text())

    # --- answer copy adds exactly the key
    bw = {(w[4], tuple(round(v, 1) for v in w[:4])) for w in blank.get_text("words")}
    new = [w for w in ans.get_text("words") if (w[4], tuple(round(v, 1) for v in w[:4])) not in bw]
    added = Counter(w[4] for w in new)
    want = Counter(EXPECT[i]) + Counter({"ANSWERS": 1})
    chk(f"p{2*i+2} adds exactly the expected answers", added == want, f"{dict(added)}")

    # --- nothing else touched
    zones = []
    for w in new:
        r = pymupdf.Rect(w[:4])
        zones.append(pymupdf.Rect(r.x0 - 3, r.y0 - 3, r.x1 + 3, r.y1 + 9))
    s, t = px(src[i]), px(ans)
    changed = np.abs(s - t).max(axis=2) > 3   # ignore the <=2/255 renderer noise
    allowed = np.zeros_like(changed)
    for z in zones:
        x0, y0 = max(int(z.x0 * Z), 0), max(int(z.y0 * Z), 0)
        allowed[y0:int(z.y1 * Z) + 1, x0:int(z.x1 * Z) + 1] = True
    stray = int((changed & ~allowed).sum())
    chk(f"p{2*i+2} changes confined to the answer areas", stray == 0, f"({stray} stray px)")

print("ALL OK" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
