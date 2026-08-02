# BB 101 — Tutorial Batch T1

TA materials for BB 101 (Biology), Tutorial Batch T1, Room LT 206.

## `attendance/`

Printable attendance sheet for **T1 only** — 31 students, one A4 page,
seven blank date columns to fill in by hand.

| File | Use |
|---|---|
| `BB101_T1_Attendance.pdf` | Print this. One A4 page, portrait, ready as-is. |
| `BB101_T1_Attendance.xlsx` | Same sheet, editable. Type the dates into the header row if you'd rather not write them. Set up for A4 portrait, fit-to-one-page. |
| `CourseList_Tutorail.xlsx` | Source roster (all batches T1–T9). |

Mark `P` / `A` in the date cells. In the `.xlsx`, the **TOTAL PRESENT** row
counts the `P` marks per column automatically and stays blank until a column
is used.

Rebuild after a roster change:

```bash
cd attendance
python3 build_attendance.py     CourseList_Tutorail.xlsx BB101_T1_Attendance.xlsx
python3 build_attendance_pdf.py CourseList_Tutorail.xlsx BB101_T1_Attendance.pdf
```

Both scripts read the `T1` sheet and skip rows with no roll number, so the
sheet tracks the roster automatically. `N_DATE_COLS` at the top of each
script controls how many date columns are drawn.

## `study-material/`

`bb101-tutorial-1-cell-biology.html` — an interactive handbook built from
`BB101Tutorial3Aug.pptx`, written for teaching from an iPad. Open the file in
any browser; it is self-contained with no external assets.

Nine sections: a run-sheet for the 50 minutes, the four ideas in the deck
expanded from first principles, a tappable animal/plant cell diagram, a
**41-question doubt bank** (searchable and filterable) covering the questions
students actually ask, a 10-question quiz built around common misconceptions,
and a numbers-and-names reference.

Interactive pieces worth knowing about before you teach:

- **Surface-area-to-volume slider** (§3) — live SA, volume, ratio and
  diffusion time as you change cell size. The strongest five minutes of the
  tutorial.
- **Tappable cell diagram** (§5) — every organelle gives its function plus
  the doubt most often attached to it. Toggles between animal and plant.
- **Doubt bank search** (§7) — usable live, mid-tutorial.
