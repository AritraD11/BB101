"""Add the 17.08.2026 and 07.09.2026 attendance (read off the marked printout
photo) to the Attendance tab of the TA's real tracker workbook.

The paper sheet has its 7/9 date written two columns after 17/8, with two
empty columns between them. Here the dates run back to back (D, E, F, G) with
no gap. 03.08 and 10.08 are left exactly as they are.

Blank = no mark on the paper (absent), matching how the earlier dates are kept.
"""

import copy
import sys

import openpyxl
from openpyxl.styles import Alignment

FILE = sys.argv[1] if len(sys.argv) > 1 else "BB101_T1_TA_Tracker.xlsx"
FIRST_DATA_ROW = 5   # Sr. 1
DATE_ROW = 4
N_STUDENTS = 31

# Sr. numbers with NO mark on the paper for that date.
ABSENT = {
    "17.08.2026": {1, 3, 5, 12},     # Salvi, Kadem, Chetaansi, Ishank
    "07.09.2026": {1, 2, 15, 27},    # Salvi, Murala, Mayank, Yashita
}
NEW_COLS = {"17.08.2026": 6, "07.09.2026": 7}   # F, G  (D, E already hold 03.08 / 10.08)

wb = openpyxl.load_workbook(FILE)
ws = wb["Attendance"]

assert ws.cell(row=DATE_ROW, column=4).value == "03.08.2026"
assert ws.cell(row=DATE_ROW, column=5).value == "10.08.2026"
assert [ws.cell(row=FIRST_DATA_ROW + i, column=1).value for i in range(N_STUDENTS)] == list(range(1, N_STUDENTS + 1))

for date, col in NEW_COLS.items():
    # header: clone the style of the existing date cell (E4)
    src = ws.cell(row=DATE_ROW, column=5)
    hdr = ws.cell(row=DATE_ROW, column=col, value=date)
    hdr._style = copy.copy(src._style)

    for sr in range(1, N_STUDENTS + 1):
        cell = ws.cell(row=FIRST_DATA_ROW + sr - 1, column=col)
        cell.value = None if sr in ABSENT[date] else "P"
        cell.alignment = Alignment(horizontal="center", vertical="center")

wb.save(FILE)

for col in (4, 5, 6, 7):
    n = sum(1 for sr in range(N_STUDENTS) if ws.cell(row=FIRST_DATA_ROW + sr, column=col).value == "P")
    print(f"{ws.cell(row=DATE_ROW, column=col).value}: {n} present")
