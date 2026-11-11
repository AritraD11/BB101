"""Build qa.html (questions + answers) from bank.py.  Usage: python3 build_qa.py"""
import os
import random
import re
from collections import Counter

from bank import AR_KEY, MITOSIS_FIG, MOCK, SECTIONS
from common import page, pedigree_svg

HERE = os.path.dirname(os.path.abspath(__file__))
LET = "abcdefgh"
ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"]
CHIP = {"mcq": ("MCQ", ""), "multi": ("One or more correct", "multi"), "match": ("Match the following", "match"),
        "fill": ("Fill in the blanks", ""), "tf": ("True / False", ""), "ar": ("Assertion – Reason", "ar"),
        "order": ("Arrange in order", ""), "num": ("Numerical", "num"), "short": ("Short answer", "short")}

# Slides per lecture in the end-sem PDF (pages 1-255) -> used for the weightage table
SLIDES = {"A": 58, "B": 24, "C": 23, "D": 17, "E": 49, "F": 29, "G": 35, "H": 20}


def plain(s):
    return re.sub(r"<[^>]+>|&[a-z]+;", "", s)


def blanks(s):
    return re.sub(r"_{4,}", "<span class='blank'></span>", s)


def fig_html(q):
    f = q.get("fig")
    if f == "PEDIGREE":
        return f"<div class='qfig'>{pedigree_svg()}</div>"
    if f == "MITOSIS":
        return f"<div class='qfig'>{MITOSIS_FIG}</div>"
    return f"<div class='qfig'>{f}</div>" if f else ""


def q_html(qid, q, marks=None):
    t = q["t"]
    label, cls = CHIP[t]
    mk = f"<span class='marks'>[{marks} mark{'s' if marks != 1 else ''}]</span>" if marks else ""
    h = [f"<div class='q' id='q-{qid}'><div class='qh'><span class='qn'>{qid}</span><span class='chip {cls}'>{label}</span>{mk}</div>"]
    if t == "ar":
        h.append(f"<div class='ar-box'><div><b>Assertion (A):</b> {q['A']}</div><div><b>Reason (R):</b> {q['R']}</div></div>")
        h.append("<ol class='opts one'>" + "".join(f"<li><span class='L'>({LET[i]})</span>{k}</li>" for i, k in enumerate(AR_KEY)) + "</ol>")
    else:
        h.append(f"<div class='stem'>{blanks(q['q'])}</div>")
    h.append(fig_html(q))
    if t in ("mcq", "multi"):
        one = max(len(plain(o)) for o in q["o"]) > 34
        h.append(f"<ol class='opts{' one' if one else ''}'>" + "".join(
            f"<li><span class='L'>({LET[i]})</span>{o}</li>" for i, o in enumerate(q["o"])) + "</ol>")
    elif t == "match":
        rows = []
        n = max(len(q["L"]), len(q["R"]))
        for i in range(n):
            l = f"<span class='L'>{chr(65 + i)}.</span>{q['L'][i]}" if i < len(q["L"]) else ""
            r = f"<span class='L'>{i + 1}.</span>{q['R'][i]}" if i < len(q["R"]) else ""
            rows.append(f"<tr><td>{l}</td><td>{r}</td></tr>")
        h.append("<table class='mt'><tr><th>Column I</th><th>Column II</th></tr>" + "".join(rows) + "</table>")
    elif t == "order":
        h.append("<ol class='opts one'>" + "".join(f"<li><span class='L'>({ROMAN[i]})</span>{it}</li>" for i, it in enumerate(q["items"])) + "</ol>")
    elif t == "tf":
        h.append("<div class='ar-key'>Write True or False. If false, correct the statement.</div>")
    if t in ("num", "short"):
        h.append("<div class='lines'>" + "<div></div>" * 3 + "</div>")
    h.append("</div>")
    return "".join(h)


def a_html(qid, q):
    t = q["t"]
    ref = f" <span class='ref'>Campbell {q['r']}</span>" if q.get("r") and q["r"] != "—" else ""
    if t == "mcq":
        a = f"({LET[q['a']]}) {q['o'][q['a']]}"
        body = q.get("e", "")
    elif t == "multi":
        a = ", ".join(f"({LET[i]})" for i in q["a"])
        body = q.get("e", "")
    elif t == "match":
        a = ", ".join(f"{chr(65 + i)}–{j + 1}" for i, j in enumerate(q["a"]))
        body = q.get("e", "")
    elif t == "fill":
        a = " &nbsp;|&nbsp; ".join(q["a"])
        body = q.get("e", "")
    elif t == "tf":
        a = "True" if q["a"] else "False"
        body = re.sub(r"^(True|False)\s*[.—–-]?\s*", "", q.get("e", ""))
        body = body[:1].upper() + body[1:]
    elif t == "ar":
        a = f"({LET[q['a']]}) {AR_KEY[q['a']]}"
        body = q.get("e", "")
    elif t == "order":
        a = " → ".join(f"({ROMAN[i]}) {q['items'][i]}" for i in q["a"])
        body = q.get("e", "")
    elif t == "num":
        a = q["a"]
        body = f"<div class='work'>{q['w']}</div>"
    else:  # short
        a = "Model answer"
        body = f"<p>{q['a']}</p>"
    body = f"<p>{body}</p>" if body and not body.startswith(("<p", "<div")) else body
    return (f"<div class='ans'><div class='ans-id'>{qid}</div><div class='e'><span class='a'>{a}</span>{ref}"
            f"{body}</div></div>")


def cover(nq, ntypes):
    toc = [("1", "Exam pattern &amp; strategy — what to expect and how to attack each question type"),
           ("2", "Model question paper — 60 marks, 90 minutes (attempt it under exam conditions)"),
           ("3", "Topic-wise practice — Sections A to H, every lecture of the end-sem syllabus"),
           ("4", "Answers &amp; explanations — with the Campbell section for each question")]
    return f"""
<section class='cover'>
  <div class='band'>
    <div class='kicker'>BB 101 Biology · End-semester examination</div>
    <h1>Practice Questions &amp; Answers</h1>
    <p class='lede'>Lectures 15–23: Mendelian genetics, cell division, chromosomes &amp; inheritance, cell communication,
    big data in biology, evolution and population genetics.</p>
  </div>
  <div class='meta'>
    <div><b>Questions</b>{nq} in total, {ntypes} formats</div>
    <div><b>Reference</b>Campbell Biology, 10th ed. — Ch. 11–15, 16.1, 21.2, 22–24</div>
    <div><b>Prepared for</b>Tutorial Batch T1</div>
  </div>
  <h3>Contents</h3>
  <ul class='toc'>{''.join(f"<li><span class='n'>{n}</span><span>{t}</span></li>" for n, t in toc)}</ul>
  <div class='box tip' style='margin-top:14pt'><span class='bt'>How to use this booklet</span>
    <p>Do the model paper first, timed, without notes. Mark it with Part 4, then go to the topic sections where you lost marks.
    Every answer gives the reason, not just the letter — read the explanation even when you got the question right.</p></div>
  <div class='foot'>Questions are written from the end-sem lecture slides and Campbell Biology (10th ed.). Section numbers such as
  “Campbell 14.1” point to the matching concept in the textbook. Items marked “—” are covered in the lecture slides only.</div>
</section>"""


def pattern_section(counts_by_sec, type_counts):
    total = sum(SLIDES.values())
    rows = []
    typical = {"A": "Ratios (3:1, 1:2:1, 9:3:3:1), terminology, history, ‘why 3:1?’",
               "B": "Probability numericals, ABO, dominance types, pedigrees",
               "C": "Stage → event matching, chromosome/DNA counting, mitosis vs meiosis",
               "D": "X-linked crosses, Morgan, nondisjunction, syndromes",
               "E": "Signalling types, GPCR/G-protein steps, cAMP pathway, amplification",
               "F": "-omes, prefixes, DNA forms, definitions, AlphaFold",
               "G": "Darwin, finches, species concept, MRSA, observations/inferences",
               "H": "Hardy–Weinberg numericals, drift/gene flow, selection types"}
    for s in SECTIONS:
        sid = s["id"]
        rows.append(f"<tr><td class='c'><b>{sid}</b></td><td>{s['title']}<div class='small muted'>{s['lec']} · {s['camp']}</div></td>"
                    f"<td class='c'>{SLIDES[sid]}</td><td class='c'>{100 * SLIDES[sid] / total:.0f}%</td>"
                    f"<td class='small'>{typical[sid]}</td><td class='c'>{counts_by_sec[sid]}</td></tr>")
    fmt_rows = [
        ("MCQ — single correct", "Facts, definitions, ‘which is NOT…’", "Read the stem twice; underline NOT / EXCEPT. Eliminate the two clearly wrong options first."),
        ("One or more correct", "Whether you know every statement", "Judge each option as its own True/False. Do not assume at least two are right."),
        ("Match the following", "Pairs of terms, stages, scientists, examples", "Start with the pairs you are sure of; Column II may contain an extra (distractor) item."),
        ("Fill in the blanks", "Exact terms (often from a figure)", "Spell the term exactly as in the lecture: <i>prometaphase</i>, <i>hemizygous</i>, <i>plasmodesmata</i>."),
        ("True / False", "Common misconceptions", "One wrong word makes the whole statement false. For ‘false’, write the correction."),
        ("Assertion – Reason", "Cause and effect", "Decide A and R separately first; only then ask “does R explain A?”."),
        ("Numerical", "Crosses, probability, Hardy–Weinberg, counting", "Write genotypes and gametes first; one gene at a time; check that fractions sum to 1."),
        ("Short answer / figure", "Explaining a mechanism; reading a pedigree or micrograph", "3 marks ≈ 3 points. Use the lecture’s key words (e.g. reception, transduction, response)."),
    ]
    patterns = [
        ("Figure-based fill-in and labelling", "The tutorials used blank-filling on lecture figures (Mitosis and Mendel worksheets). Expect labelled diagrams: mitosis stages, Punnett squares, pedigrees, the GPCR cycle.", "C13, C16, B14, E18"),
        ("Ratios and probability", "3 : 1, 1 : 2 : 1, 9 : 3 : 3 : 1, the trihybrid ‘at least two recessive’ problem from the slides, ABO and albinism crosses.", "A19–A21, B15–B20"),
        ("X-linked crosses", "The three colour-blindness crosses (slide 118) and Morgan’s fruit flies are the core of Lecture 19 — expect at least one cross.", "D13–D17"),
        ("Hardy–Weinberg numericals", "Two worked examples were added to the end of the slides (552 pea plants; lizard scales). Know both routes: from <i>q</i><sup>2</sup> and by counting alleles.", "H13–H19"),
        ("Compare and contrast", "Mitosis vs meiosis, natural vs artificial selection, explainable vs interpretable AI, paracrine vs endocrine, the three modes of selection.", "C25, G19, F7, E16, H11"),
        ("Who / when", "Mendel 1866, Griffith 1928, Avery 1944, Watson &amp; Crick 1953, Darwin 1859, Sutherland 1971, Gilman &amp; Rodbell 1994, AlphaFold Nobel 2024, Dayhoff ~1960.", "A9, E13, F3, F10"),
        ("‘Why’ questions from the slides", "“Why is the ratio 3:1?”, “What is the advantage of a cascade?”, “Is widow’s peak dominant or recessive?”, “Why are X-linked disorders more common in males?”", "A22, E24, B14, D18"),
        ("Numbers to remember", "46/23 chromosomes, 2<sup>23</sup> ≈ 8.4 million, 10 bp and 3.4 Å per turn/bp (B-DNA), 7 transmembrane helices, ~60% of drugs, 10<sup>8</sup> amplification, 1200 → 180 finches.", "C19, F5, E19"),
    ]
    tc = ", ".join(f"{CHIP[k][0]} {v}" for k, v in type_counts.most_common())
    return f"""
<section class='page-break'>
<h2>1 · Exam pattern and strategy<span class='sub'>What the end-sem covers, the question formats, and the high-yield question patterns</span></h2>
<h3>1.1 Syllabus weightage</h3>
<p>The end-sem syllabus is the 255-slide lecture PDF (Lectures 15–23). The share of slides is a rough guide to how much each topic matters.
Lecture 16 largely repeats Lecture 15, so Section A’s share is slightly inflated.</p>
<table><tr><th class='c'>Sec.</th><th>Topic</th><th class='c'>Slides</th><th class='c'>Share</th><th>Typical questions</th><th class='c'>Qs here</th></tr>{''.join(rows)}</table>
<div class='box note'><span class='bt'>Reading the table</span><p>Mendel (A–B), cell communication (E) and evolution with population genetics (G–H) together make up nearly three-quarters of the slides — give them most of your revision time.
The numerical questions come mainly from B, D and H.</p></div>
<h3>1.2 Question formats and how to attack them</h3>
<table><tr><th style='width:22%'>Format</th><th style='width:28%'>What it really tests</th><th>Strategy</th></tr>
{''.join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in fmt_rows)}</table>
<p class='small muted'>This booklet contains: {tc}.</p>
<h3>1.3 High-yield question patterns</h3>
<table><tr><th style='width:24%'>Pattern</th><th>What to expect</th><th style='width:16%'>Practise with</th></tr>
{''.join(f"<tr><td><b>{a}</b></td><td>{b}</td><td class='small'>{c}</td></tr>" for a, b, c in patterns)}</table>
<div class='two'>
<div class='box tip'><span class='bt'>In the exam hall</span><ul>
<li>Attempt every MCQ — unless your paper says there is negative marking.</li>
<li>For genetics problems, write the genotypes of the parents and their gametes before anything else.</li>
<li>Draw a 2 × 2 Punnett square per gene; multiply across genes.</li>
<li>Hardy–Weinberg: always start from <i>q</i><sup>2</sup> (the recessive phenotype) — never from the dominant phenotype.</li></ul></div>
<div class='box trap'><span class='bt'>Classic traps</span><ul>
<li>‘Individuals evolve’ — false; populations evolve.</li>
<li>Prophase vs prometaphase: the nuclear envelope breaks up in <b>prometaphase</b>.</li>
<li>G protein ON = GTP, OFF = GDP.</li>
<li>Adenylyl cyclase makes cAMP; phosphodiesterase destroys it.</li>
<li>Sister chromatids separate in anaphase <b>II</b> (and in mitosis), homologues in anaphase <b>I</b>.</li></ul></div>
</div>
</section>"""


def arrange(questions, seed):
    """Balance the position of the correct option across single-correct MCQs and shuffle
    multi-correct options. Deterministic (seeded); questions flagged 'keep' stay as written."""
    rng = random.Random(seed)
    mcqs = [q for q in questions if q["t"] == "mcq"]
    count = Counter(q["a"] for q in mcqs if q.get("keep"))
    for q in mcqs:
        if q.get("keep"):
            continue
        low = min(count[i] for i in range(4))
        target = rng.choice([i for i in range(4) if count[i] == low])
        right = q["o"][q["a"]]
        others = [o for i, o in enumerate(q["o"]) if i != q["a"]]
        rng.shuffle(others)
        others.insert(target, right)
        q["o"], q["a"] = others, target
        count[target] += 1
    for q in questions:
        if q["t"] == "multi":
            order = list(range(len(q["o"])))
            rng.shuffle(order)
            q["o"] = [q["o"][i] for i in order]
            q["a"] = sorted(order.index(i) for i in q["a"])


def build():
    arrange([q for s in SECTIONS for q in s["qs"]], 101)
    arrange([q for p in MOCK["parts"] for q in p["qs"]], 202)
    all_q = [q for s in SECTIONS for q in s["qs"]] + [q for p in MOCK["parts"] for q in p["qs"]]
    type_counts = Counter(q["t"] for q in all_q)
    counts_by_sec = {s["id"]: len(s["qs"]) for s in SECTIONS}

    parts = [cover(len(all_q), len(type_counts)), pattern_section(counts_by_sec, type_counts)]

    # ---- model paper
    mp = [f"<section class='page-break'><h2>2 · {MOCK['title']}<span class='sub'>Maximum marks: {MOCK['marks']} · Time: {MOCK['time']} · Answer all questions</span></h2>"]
    n = 0
    for p in MOCK["parts"]:
        mp.append(f"<h3>{p['name']} <span class='small muted' style='font-weight:400'>({p['each']} mark{'s' if p['each'] != 1 else ''} each)</span></h3>")
        if p.get("note"):
            mp.append(f"<p class='small muted'>{p['note']}</p>")
        for q in p["qs"]:
            n += 1
            mp.append(q_html(f"M{n}", q, p["each"]))
    mp.append("</section>")
    parts.append("".join(mp))

    # ---- topic sections
    for k, s in enumerate(SECTIONS):
        sec = [f"<section class='page-break'><h2>{'3 · ' if k == 0 else ''}Section {s['id']} — {s['title']}"
               f"<span class='sub'>{s['lec']} · {s['camp']} · {len(s['qs'])} questions</span></h2>"]
        for i, q in enumerate(s["qs"], 1):
            sec.append(q_html(f"{s['id']}{i}", q))
        sec.append("</section>")
        parts.append("".join(sec))

    # ---- answers
    ans = ["<section class='page-break'><h2>4 · Answers and explanations<span class='sub'>Model paper first, then Sections A–H</span></h2>",
           "<h3>Model question paper</h3>"]
    n = 0
    for p in MOCK["parts"]:
        for q in p["qs"]:
            n += 1
            ans.append(a_html(f"M{n}", q))
    for s in SECTIONS:
        ans.append(f"<h3>Section {s['id']} — {s['title']}</h3>")
        for i, q in enumerate(s["qs"], 1):
            ans.append(a_html(f"{s['id']}{i}", q))
    ans.append("</section>")
    parts.append("".join(ans))

    html = page("BB 101 End-Sem Practice — Questions & Answers", "".join(parts))
    with open(os.path.join(HERE, "qa.html"), "w") as f:
        f.write(html)
    print(f"qa.html: {len(all_q)} questions; by type: {dict(type_counts)}; by section: {counts_by_sec}; model paper: {n}")


if __name__ == "__main__":
    build()
