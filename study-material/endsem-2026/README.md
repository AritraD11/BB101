# BB 101 end-sem practice (Lectures 15–23)

Two PDFs for students, built from the end-sem lecture slides (255 slides) with
explanations checked against Campbell Biology, 10th ed.

| File | What it is |
|---|---|
| `BB101_EndSem_Practice_QandA.pdf` | 60 pages. Exam-pattern analysis and strategy; a 60-mark, 90-minute model paper; topic-wise practice (Sections A–H, one per lecture); answers with explanations and the Campbell section for each. 225 questions: MCQ, one-or-more-correct, match the following, fill in the blanks, true/false, assertion–reason, ordering, numericals, short answer, and figure-based items (pedigrees, lecture micrographs). |
| `BB101_EndSem_Short_Notes.pdf` | 15 pages. One section per lecture with key terms, tables, diagrams, “remember” and “trap” boxes, plus a last-minute revision sheet (numbers, names and dates, formulas, ratios, twelve classic traps). |

Rebuild (needs `pymupdf` and the Node `playwright` package):

```bash
cd build
python3 build_qa.py && node render.js qa.html ../BB101_EndSem_Practice_QandA.pdf "BB 101 Biology · End-sem practice — Questions &amp; Answers"
python3 build_notes.py && node render.js notes.html ../BB101_EndSem_Short_Notes.pdf "BB 101 Biology · End-sem short notes"
python3 qa_check.py
```

- `build/bank.py` holds every question, its answer, explanation and Campbell section. The build places MCQ answers in a balanced, seeded order, so letters don’t follow a pattern.
- `build/qa_check.py` checks question structure, recomputes every numerical answer independently (gamete enumeration for crosses, direct arithmetic for Hardy–Weinberg, DNA lengths and the adrenaline cascade), and confirms each question has exactly one entry in the answer key.
- `assets/` holds the five mitosis micrographs, cropped from lecture slides 93–94 (Campbell Fig. 12.7).
