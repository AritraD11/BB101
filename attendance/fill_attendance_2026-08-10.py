"""Record the 10.08.2026 attendance (from the marked printout photo) into the
second date column of the T1 attendance workbook.

Blank in the source list below = no mark on the physical sheet (left as-is,
per TA's call, rather than inferred as absent).

NOTE: the physical sheet's own handwritten "TOTAL PRESENT" for this column
reads 26, but this draft reading (28 marked "P") doesn't reconcile against
that -- P and A look very similar in the photo's handwriting. Flagged for
the TA to confirm which 2 of the 28 below were actually marked "A".
"""

import openpyxl
from openpyxl.styles import Alignment, Font

FILE = "BB101_T1_Attendance.xlsx"
FONT = "Arial"
DATE_COL = 5        # column E = second date column
DATE_ROW = 4         # HDR_BOT row, where a date is handwritten under "DATE"
DATE_LABEL = "10.08.2026"
FIRST_DATA_ROW = 5   # Sr. 1

# Sr. 1-31, in roster order, exactly as marked on the printed sheet.
MARKS = [
    None, None, None, "P", "P", "P", "P", "P", "P", "P",
    "P", "P", "P", "P", "P", "P", "P", "P", "P", "P",
    "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P",
]

wb = openpyxl.load_workbook(FILE)
ws = wb.active

date_cell = ws.cell(row=DATE_ROW, column=DATE_COL, value=DATE_LABEL)
date_cell.font = Font(name=FONT, size=9, bold=True)
date_cell.alignment = Alignment(horizontal="center", vertical="center")

for i, mark in enumerate(MARKS):
    if mark is None:
        continue
    cell = ws.cell(row=FIRST_DATA_ROW + i, column=DATE_COL, value=mark)
    cell.alignment = Alignment(horizontal="center", vertical="center")

wb.save(FILE)
present = sum(1 for m in MARKS if m == "P")
blank = sum(1 for m in MARKS if m is None)
print(f"wrote {DATE_LABEL} into column E: {present} present, {blank} unmarked, {len(MARKS)} total")
