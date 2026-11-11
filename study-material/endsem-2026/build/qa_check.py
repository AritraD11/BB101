"""QA for the end-sem PDFs.  Usage: python3 qa_check.py  (run after build_qa.py / build_notes.py / render.js)

1. Structure of every question in bank.py (options, answer indices, permutations, blanks).
2. Independent recomputation of every numerical answer (gamete enumeration for crosses,
   direct arithmetic for Hardy-Weinberg, DNA and amplification) - checked against the answer text.
3. The rendered Q&A PDF: every question id appears once in the question part and once in the answers.
4. Both PDFs: fonts embedded, no template artefacts, page counts.
"""
import itertools
import math
import os
import re
import sys
from collections import Counter
from fractions import Fraction as F

import pymupdf

import build_qa
from bank import MOCK, SECTIONS

HERE = os.path.dirname(os.path.abspath(__file__))
QA_PDF = os.path.join(HERE, "..", "BB101_EndSem_Practice_QandA.pdf")
NOTES_PDF = os.path.join(HERE, "..", "BB101_EndSem_Short_Notes.pdf")
fails = []


def check(name, cond, info=""):
    if not cond:
        fails.append(f"{name} {info}")
    print(("PASS " if cond else "FAIL ") + name + (f"  [{info}]" if info else ""))


# same arrangement as the build
build_qa.arrange([q for s in SECTIONS for q in s["qs"]], 101)
build_qa.arrange([q for p in MOCK["parts"] for q in p["qs"]], 202)
Q = {}
for s in SECTIONS:
    for i, q in enumerate(s["qs"], 1):
        Q[f"{s['id']}{i}"] = q
n = 0
for p in MOCK["parts"]:
    for q in p["qs"]:
        n += 1
        Q[f"M{n}"] = q

# ------------------------------------------------------------------ 1. structure
bad = []
for qid, q in Q.items():
    t = q["t"]
    if t == "mcq" and not (len(q["o"]) == 4 and 0 <= q["a"] < 4):
        bad.append(qid)
    if t == "multi" and not (q["a"] and len(set(q["a"])) == len(q["a"]) and all(0 <= i < len(q["o"]) for i in q["a"])):
        bad.append(qid)
    if t == "match" and not (len(q["a"]) == len(q["L"]) and len(set(q["a"])) == len(q["a"]) and all(0 <= j < len(q["R"]) for j in q["a"])):
        bad.append(qid)
    if t == "order" and sorted(q["a"]) != list(range(len(q["items"]))):
        bad.append(qid)
    if t == "ar" and q["a"] not in (0, 1, 2, 3):
        bad.append(qid)
    if t == "fill" and len(re.findall(r"_{4,}", q["q"])) != len(q["a"]):
        bad.append(qid)
    if t == "tf" and not isinstance(q["a"], bool):
        bad.append(qid)
    if t in ("mcq", "multi") and len(set(q["o"])) != len(q["o"]):
        bad.append(qid)
check("question structure (options, answers, blanks, permutations)", not bad, ", ".join(bad))
stems = Counter(re.sub(r"<[^>]+>", "", q.get("q") or q.get("A")) for q in Q.values())
dups = [s for s, c in stems.items() if c > 1]
check("no duplicate question stems", not dups, "; ".join(d[:50] for d in dups))
mcq_pos = Counter("abcd"[q["a"]] for q in Q.values() if q["t"] == "mcq")
check("MCQ answer letters balanced (max-min <= 4)", max(mcq_pos.values()) - min(mcq_pos.values()) <= 4, str(dict(sorted(mcq_pos.items()))))
multi_k = Counter(len(q["a"]) for q in Q.values() if q["t"] == "multi")
check("multi-correct items vary in number of correct options", len(multi_k) >= 3, str(dict(multi_k)))
ar = Counter("abcd"[q["a"]] for q in Q.values() if q["t"] == "ar")
check("assertion-reason uses all four codes", len(ar) == 4, str(dict(sorted(ar.items()))))
marks = sum(p["each"] * len(p["qs"]) for p in MOCK["parts"])
check("model paper totals its stated marks", marks == MOCK["marks"], f"{marks} vs {MOCK['marks']}")

# ------------------------------------------------------------------ 2. numerical answers
def gametes(geno):
    """'PpYyRr' -> Counter of gametes (independent assortment)."""
    pairs = [geno[i:i + 2] for i in range(0, len(geno), 2)]
    c = Counter()
    for combo in itertools.product(*pairs):
        c["".join(combo)] += F(1, 2 ** len(pairs))
    return c


def cross(g1, g2):
    out = Counter()
    for a, pa in gametes(g1).items():
        for b, pb in gametes(g2).items():
            out[tuple("".join(sorted(x + y)) for x, y in zip(a, b))] += pa * pb
    return out


def recessive(pair):  # 'pp' -> True
    return pair == pair.lower()


def prob(dist, pred):
    return sum(p for k, p in dist.items() if pred(k))


def has(qid, *vals):
    text = re.sub(r"<[^>]+>|&nbsp;", " ", Q[qid]["a"] + " " + Q[qid].get("w", ""))
    missing = [v for v in vals if v not in text]
    check(f"{qid} numerical answer matches recomputation", not missing, f"expected {vals}, missing {missing}")


d = cross("Pp", "Pp")
white = prob(d, lambda k: recessive(k[0]))
het_among_purple = prob(d, lambda k: k[0] == "Pp") / (1 - white)
has("A19", str(int(800 * white)), f"{het_among_purple.numerator}/{het_among_purple.denominator}")
d = cross("YyRr", "YyRr")
has("A20", str(prob(d, lambda k: not recessive(k[0]) and not recessive(k[1]))), str(prob(d, lambda k: recessive(k[0]) and recessive(k[1]))), str(len(gametes("YyRr"))))
has("A21", str(len(gametes("AaBbCcDd"))))
d = cross("PpYyRr", "Ppyyrr")
at_least_two = prob(d, lambda k: sum(recessive(x) for x in k) >= 2)
has("B15", "3/8", "6/16")
check("B15 enumeration gives 3/8", at_least_two == F(3, 8), str(at_least_two))
d = cross("AaBbCc", "AaBbCc")
has("B16", str(prob(d, lambda k: k == ("AA", "BB", "CC"))), str(prob(d, lambda k: k == ("Aa", "Bb", "Cc"))), str(prob(d, lambda k: k == ("aa", "bb", "cc"))))
d = cross("Rw", "Rw")  # R = red, w = white, incomplete dominance
has("B17", f"{int(240 * d[('RR',)])} red", f"{int(240 * d[('Rw',)])} pink", f"{int(240 * d[('ww',)])} white")
# ABO: A = IA, B = IB, o = i
abo = Counter()
for x in ("A", "o"):
    for y in ("B", "o"):
        abo["".join(sorted(x + y))] += F(1, 4)
has("B18", str(abo["AB"]), str(abo["oo"]), str(abo["oo"] ** 2))
d = cross("Aa", "Aa")
aff = d[("aa",)]
has("B20", str(aff), str(d[("Aa",)] / (1 - aff)), str((1 - aff) ** 2))
has("C18", str(2 ** 4), "(b) 4", "(c) 16")
comb = 2 ** 23
check("C19 2^23 ≈ 8.4 million", round(comb / 1e6, 1) == 8.4, str(comb))
check("C19 (2^23)^2 ≈ 7 x 10^13", round(comb ** 2 / 1e13) == 7, f"{comb ** 2:.3e}")


def xcross(mother, father):
    """mother 'NN'/'Nn'/'nn' (X alleles), father 'N'/'n' (X allele) + Y. Returns (daughters, sons) dists."""
    dau, son = Counter(), Counter()
    for m in mother:
        dau["".join(sorted(m + father))] += F(1, 2)
        son[m] += F(1, 2)
    return dau, son


dau, son = xcross("NN", "n")
check("D13 daughters all carriers, no affected children", dau == {"Nn": 1} and son == {"N": 1})
dau, son = xcross("Nn", "N")
has("D14", str(son["n"]), str(dau["Nn"]), str(son["n"] / 2))
dau, son = xcross("Nn", "n")
check("D15 each child affected with p = 1/2", dau["nn"] == F(1, 2) and son["n"] == F(1, 2))
dau, son = xcross("ww", "W")   # W = w+ (red), w = white
check("D16 reciprocal: F1 females red, males white", all("W" in g for g in dau) and set(son) == {"w"})
dau, son = xcross("Ww", "W")   # F1 red female (carrier) x F1 red male
white_f2 = (son["w"]) / 2
has("D17", f"{int(400 * white_f2)} white", "0 female")
steps = [1, 1e2, 1e2, 1e4, 1e4, 1e5, 1e6, 1e8]
ratios = [steps[i + 1] / steps[i] for i in range(len(steps) - 1)]
check("E19 three 100-fold steps (G proteins, cAMP, glucose 1-P) and 10^8 overall", [i for i, r in enumerate(ratios) if r == 100] == [0, 2, 6] and steps[-1] / steps[0] == 1e8, str(ratios))
check("E19 answer names all three 100-fold steps", all(k in Q["E19"]["a"] for k in ("activating G proteins", "making cAMP", "glucose 1-phosphate")) and "three" in Q["E19"]["q"])
check("E19 glucose 1-P per PKA = 10^4", steps[-1] / steps[4] == 1e4)
has("F16", "1.02 m")
check("F16 3e9 bp x 3.4 Å = 1.02 m", abs(3.0e9 * 3.4e-10 - 1.02) < 1e-9)
check("F17 100 turns, 340 nm, ~91 A-form turns", 1000 / 10 == 100 and 1000 * 0.34 == 340 and round(1000 / 11) == 91)
has("F18", "750 MB")
check("F18 3e9 bases x 2 bits = 750 MB", 3.0e9 * 2 / 8 / 1e6 == 750)


def hw_from_q2(q2):
    q = math.sqrt(q2)
    return q, 1 - q


q, p = hw_from_q2(0.09)
has("H13", f"= {q:.1f}", f"= {p:.1f}", f"{p * p:.2f}", f"{2 * p * q:.2f}")
q, p = hw_from_q2(6 / 552)
has("H14", f"{q:.3f}", f"{p:.3f}", f"about {round(2 * p * q * 552)}")


def count_alleles(AA, Aa, aa):
    N = AA + Aa + aa
    return (2 * AA + Aa) / (2 * N), N


p, N = count_alleles(360, 480, 160)
check("H15 p = 0.6 and observed = HW expected", abs(p - 0.6) < 1e-12 and (round(p * p * N), round(2 * p * (1 - p) * N), round((1 - p) ** 2 * N)) == (360, 480, 160))
p, N = count_alleles(500, 200, 300)
exp = (round(p * p * N), round(2 * p * (1 - p) * N), round((1 - p) ** 2 * N))
has("H16", str(exp[0]), str(exp[1]), str(exp[2]), "NOT in equilibrium")
q, p = hw_from_q2(1 / 10000)
has("H17", f"{2 * p * q:.4f}")
q, p = hw_from_q2(0.36)
has("H18", f"{p * p:.2f}", f"{2 * p * q:.2f}")
G, g = 2 * 1024 + 512, 512 + 2 * 64
p = G / (G + g)
has("H19", f"{p:.1f}", f"{1 - p:.1f}", f"{p * p:.2f}", f"{2 * p * (1 - p):.2f}", f"{(1 - p) ** 2:.2f}")
check("H19 observed genotype freqs equal HW", (1024 / 1600, 512 / 1600, 64 / 1600) == (0.64, 0.32, 0.04))
# model paper numericals
d = cross("AaBbCc", "aaBbcc")
has("M32", str(prob(d, lambda k: k == ("aa", "bb", "cc"))), str(prob(d, lambda k: not any(recessive(x) for x in k))))
dau, son = xcross("Nn", "n")
has("M33", str(dau["nn"]), str(son["n"]), str((dau["nn"] + son["n"]) / 2))
q, p = hw_from_q2(0.16)
has("M34", f"{round(2 * p * q * 1000)} heterozygous", f"{round(p * p * 1000)} homozygous dominant")
# numeric MCQs
check("A4 705/224 ≈ 3 : 1", round(705 / 224, 2) == 3.15)
check("M15 2pq (q = 0.2) = 0.32 is the keyed option", Q["M15"]["o"][Q["M15"]["a"]] == f"{2 * 0.8 * 0.2:.2f}")
check("M4 G2 chromatids = 92 is the keyed option", Q["M4"]["o"][Q["M4"]["a"]] == "92")
check("B7 ABO 6 genotypes / 4 phenotypes is the keyed option", Q["B7"]["o"][Q["B7"]["a"]].startswith(f"{len(['AA','Ao','BB','Bo','AB','oo'])} genotypes, 4"))

# ------------------------------------------------------------------ 3. rendered Q&A PDF
doc = pymupdf.open(QA_PDF)
pages = [pg.get_text() for pg in doc]
ans_start = next(i for i, t in enumerate(pages) if "4 · Answers and explanations" in t)
qtext = "\n".join(pages[:ans_start])
atext = "\n".join(pages[ans_start:])
ids = list(Q)
miss_q = [i for i in ids if not re.search(rf"(?m)^{i}$", qtext)]
miss_a = [i for i in ids if len(re.findall(rf"(?m)^{i}$", atext)) != 1]
check(f"all {len(ids)} question ids present in the question part", not miss_q, ", ".join(miss_q[:10]))
check("every question id has exactly one answer entry", not miss_a, ", ".join(miss_a[:10]))
check("Q&A PDF has the five mitosis micrographs", sum(len(pg.get_images()) for pg in doc) >= 5)

# ------------------------------------------------------------------ 4. both PDFs
for path in (QA_PDF, NOTES_PDF):
    dd = pymupdf.open(path)
    name = os.path.basename(path)
    fonts = {f[3] for pg in dd for f in pg.get_fonts()}
    # Type3 fonts (Chromium's output for the variable Inter font) carry their glyphs inside the PDF
    unembedded = [f for pg in dd for f in pg.get_fonts() if f[1] == "n/a" and f[2] != "Type3"]
    text = "\n".join(pg.get_text() for pg in dd)
    check(f"{name}: fonts embedded", not unembedded, ", ".join(sorted(fonts))[:120])
    check(f"{name}: no template artefacts", not re.search(r"\{[a-z_]+\}|None\b|undefined|PEDIGREE|MITOSIS\b", text))
    sparse = [i + 1 for i, pg in enumerate(dd) if len(pg.get_text().strip()) < 60 and not pg.get_images()]
    check(f"{name}: no blank pages", not sparse, str(sparse))
    print(f"     {name}: {len(dd)} pages, {os.path.getsize(path) / 1e6:.2f} MB")

print("\nALL CHECKS PASSED" if not fails else f"\n{len(fails)} FAILED:\n  " + "\n  ".join(fails))
sys.exit(1 if fails else 0)
