"""Build the combined T1 TA tracker workbook: one file, two tabs.

  Attendance        — roster + a date column per Monday tutorial session.
  Extempore Grading  — roster + Group / Understanding / Clarity / Insight / Total.

Run with no arguments to regenerate from the course list, marking every
Monday date supplied in MONDAY_MARKS. Marks for a date not yet run are
left blank for hand entry.
"""

import sys

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.properties import PageSetupProperties

SOURCE = sys.argv[1] if len(sys.argv) > 1 else "CourseList_Tutorail.xlsx"
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else "BB101_T1_TA_Tracker.xlsx"

FONT = "Arial"
thin = Side(style="thin", color="808080")
medium = Side(style="medium", color="000000")
box = Border(left=thin, right=thin, top=thin, bottom=thin)
header_fill = PatternFill("solid", fgColor="D9D9D9")
date_fill = PatternFill("solid", fgColor="F2F2F2")

# ---------------------------------------------------------------- read roster
src = openpyxl.load_workbook(SOURCE)["T1"]
roster = []
for row in src.iter_rows(min_row=3, max_row=src.max_row, values_only=True):
    roll, name = row[1], row[2]
    if roll is None or name is None:
        continue
    roster.append((str(roll).strip(), str(name).strip()))

# Every Monday tutorial session so far. Add a new "DD.MM.YYYY": {...} entry
# each week; leave a date's dict empty ({}) to just add the header ready for
# hand entry. Keyed by Sr. (1-indexed, roster order) -> "P" or "A"; a Sr. not
# listed for a given date is left blank (not inferred as absent).
MONDAY_MARKS = {
    "03.08.2026": {
        i + 1: "P"
        for i in range(31)
        if i + 1 not in (1, 2, 8)  # Salvi Aniket Bharat, Murala Vamshi, Ashish Sinha: unmarked on the sheet
    },
    "10.08.2026": {
        i + 1: "P"
        for i in range(31)
        if i + 1 not in (1, 2, 3)  # Salvi Aniket Bharat, Murala Vamshi, Kadem Akhil: unmarked on the sheet
    },
}
N_DATE_COLS = 7  # blank trailing columns beyond the marked dates, ready for future Mondays

# Group activity groups (10.08.2026). Group 1 was formed by the students
# themselves; Groups 2-3 are a random split of the rest of the roster
# (random.Random(2026), documented so the split is reproducible).
GROUPS = {
    "Group 1  (self-formed)": [11, 14, 16, 18, 20, 21, 26, 27, 29, 30],
    "Group 2  (random)": [1, 2, 3, 5, 6, 7, 13, 15, 22, 24, 28],
    "Group 3  (random)": [4, 8, 9, 10, 12, 17, 19, 23, 25, 31],
}
sr_to_group = {sr: label.split("  ")[0] for label, srs in GROUPS.items() for sr in srs}

# ============================================================== ATTENDANCE
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Attendance"

dates = list(MONDAY_MARKS.keys())
n_cols = max(len(dates) + 2, N_DATE_COLS)  # keep a few spare blank columns ahead
last_col = 3 + n_cols
last_letter = get_column_letter(last_col)

ws.merge_cells(f"A1:{last_letter}1")
ws["A1"] = "BB 101  —  BIOLOGY   |   ATTENDANCE"
ws["A1"].font = Font(name=FONT, size=15, bold=True)
ws["A1"].alignment = Alignment(horizontal="center", vertical="center")

ws.merge_cells(f"A2:{last_letter}2")
ws["A2"] = "Tutorial Batch T1        Room: LT 206        TA: Aritra"
ws["A2"].font = Font(name=FONT, size=11, bold=True)
ws["A2"].alignment = Alignment(horizontal="center", vertical="center")

HDR_TOP, HDR_BOT = 3, 4
for col, label in ((1, "Sr."), (2, "Roll No."), (3, "Name of Student")):
    ws.merge_cells(start_row=HDR_TOP, start_column=col, end_row=HDR_BOT, end_column=col)
    c = ws.cell(row=HDR_TOP, column=col, value=label)
    c.font = Font(name=FONT, size=10, bold=True)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

for col in range(4, last_col + 1):
    c = ws.cell(row=HDR_TOP, column=col, value="DATE" if col == 4 else None)
    c.font = Font(name=FONT, size=10, bold=True)
    c.alignment = Alignment(horizontal="centerContinuous", vertical="center")

for i in range(n_cols):
    col = 4 + i
    c = ws.cell(row=HDR_BOT, column=col)
    c.fill = date_fill
    if i < len(dates):
        c.value = dates[i]
        c.font = Font(name=FONT, size=9, bold=True)
        c.alignment = Alignment(horizontal="center", vertical="center")

for row in (HDR_TOP, HDR_BOT):
    for col in range(1, last_col + 1):
        cell = ws.cell(row=row, column=col)
        cell.border = box
        if cell.fill.fgColor.rgb != "00F2F2F2":
            cell.fill = header_fill

first_data = HDR_BOT + 1
for i, (roll, name) in enumerate(roster):
    r = first_data + i
    sr = i + 1
    ws.cell(row=r, column=1, value=sr).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=r, column=2, value=roll).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=r, column=3, value=name).alignment = Alignment(horizontal="left", vertical="center", indent=1)
    for j, date in enumerate(dates):
        mark = MONDAY_MARKS[date].get(sr)
        if mark:
            mc = ws.cell(row=r, column=4 + j, value=mark)
            mc.alignment = Alignment(horizontal="center", vertical="center")
    for col in range(1, last_col + 1):
        cell = ws.cell(row=r, column=col)
        cell.border = box
        if cell.font.name != FONT or cell.value is None:
            cell.font = Font(name=FONT, size=10)
    ws.row_dimensions[r].height = 19

last_data = first_data + len(roster) - 1

total_row = last_data + 1
ws.merge_cells(start_row=total_row, start_column=1, end_row=total_row, end_column=3)
t = ws.cell(row=total_row, column=1, value="TOTAL PRESENT")
t.font = Font(name=FONT, size=10, bold=True)
t.alignment = Alignment(horizontal="right", vertical="center", indent=1)
for col in range(4, last_col + 1):
    L = get_column_letter(col)
    rng = f"{L}{first_data}:{L}{last_data}"
    c = ws.cell(row=total_row, column=col, value=f'=IF(COUNTA({rng})=0,"",COUNTIF({rng},"P"))')
    c.font = Font(name=FONT, size=10, bold=True)
    c.alignment = Alignment(horizontal="center", vertical="center")
for col in range(1, last_col + 1):
    ws.cell(row=total_row, column=col).border = box
    ws.cell(row=total_row, column=col).fill = header_fill
ws.row_dimensions[total_row].height = 20

sig_row = total_row + 2
ws.merge_cells(start_row=sig_row, start_column=1, end_row=sig_row, end_column=last_col)
s = ws.cell(row=sig_row, column=1, value=f"Total students on roll: {len(roster)}   ·   Mark P / A in the next blank date column each Monday.")
s.font = Font(name=FONT, size=9, color="404040")
s.alignment = Alignment(horizontal="left", vertical="center")

for col in range(1, last_col + 1):
    top = ws.cell(row=HDR_TOP, column=col)
    top.border = Border(left=top.border.left, right=top.border.right, top=medium, bottom=top.border.bottom)
    bot = ws.cell(row=total_row, column=col)
    bot.border = Border(left=bot.border.left, right=bot.border.right, top=bot.border.top, bottom=medium)
for row in range(HDR_TOP, total_row + 1):
    lft = ws.cell(row=row, column=1)
    lft.border = Border(left=medium, right=lft.border.right, top=lft.border.top, bottom=lft.border.bottom)
    rgt = ws.cell(row=row, column=last_col)
    rgt.border = Border(left=rgt.border.left, right=medium, top=rgt.border.top, bottom=rgt.border.bottom)
for row in range(HDR_TOP, total_row + 1):
    c = ws.cell(row=row, column=4)
    c.border = Border(left=medium, right=c.border.right, top=c.border.top, bottom=c.border.bottom)

ws.column_dimensions["A"].width = 4.5
ws.column_dimensions["B"].width = 11.5
ws.column_dimensions["C"].width = 32
for col in range(4, last_col + 1):
    ws.column_dimensions[get_column_letter(col)].width = 8.2

ws.row_dimensions[1].height = 22
ws.row_dimensions[2].height = 18
ws.row_dimensions[HDR_TOP].height = 17
ws.row_dimensions[HDR_BOT].height = 22

ws.page_setup.orientation = "landscape" if n_cols > 7 else "portrait"
ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 1
ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
ws.page_margins.left = ws.page_margins.right = 0.4
ws.page_margins.top = ws.page_margins.bottom = 0.4
ws.page_margins.header = ws.page_margins.footer = 0.2
ws.print_options.horizontalCentered = True
ws.print_title_rows = f"{HDR_TOP}:{HDR_BOT}"
ws.freeze_panes = ws.cell(row=first_data, column=4)

# ========================================================= EXTEMPORE GRADING
wg = wb.create_sheet("Extempore Grading")

W = {"sr": 4.5, "roll": 11.5, "name": 32, "group": 9, "crit": 11, "total": 10}
cols = ["sr", "roll", "name", "group", "und", "clar", "ins", "total"]
headers = ["Sr.", "Roll No.", "Name of Student", "Group", "Underst. /5", "Clarity /5", "Insight /5", "Total /15"]
last_col_g = len(cols)
last_letter_g = get_column_letter(last_col_g)

wg.merge_cells(f"A1:{last_letter_g}1")
wg["A1"] = "BB 101  —  BIOLOGY   |   GROUP ACTIVITY — EXTEMPORE GRADING"
wg["A1"].font = Font(name=FONT, size=15, bold=True)
wg["A1"].alignment = Alignment(horizontal="center", vertical="center")

wg.merge_cells(f"A2:{last_letter_g}2")
wg["A2"] = "Tutorial Batch T1        Room: LT 206        TA: Aritra        Date: 10.08.2026"
wg["A2"].font = Font(name=FONT, size=11, bold=True)
wg["A2"].alignment = Alignment(horizontal="center", vertical="center")

wg.merge_cells(f"A3:{last_letter_g}3")
wg["A3"] = "Each criterion out of 5  ·  Understanding / Clarity / Insight  ·  Total out of 15 (auto-summed)"
wg["A3"].font = Font(name=FONT, size=9, italic=True, color="555555")
wg["A3"].alignment = Alignment(horizontal="center", vertical="center")

HDR_ROW = 4
for col, label in enumerate(headers, start=1):
    c = wg.cell(row=HDR_ROW, column=col, value=label)
    c.font = Font(name=FONT, size=9.5, bold=True)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.fill = header_fill
    c.border = box
wg.row_dimensions[HDR_ROW].height = 26

first_data_g = HDR_ROW + 1
for i, (roll, name) in enumerate(roster):
    r = first_data_g + i
    wg.cell(row=r, column=1, value=i + 1).alignment = Alignment(horizontal="center", vertical="center")
    wg.cell(row=r, column=2, value=roll).alignment = Alignment(horizontal="center", vertical="center")
    wg.cell(row=r, column=3, value=name).alignment = Alignment(horizontal="left", vertical="center", indent=1)
    wg.cell(row=r, column=4, value=sr_to_group.get(i + 1, ""))
    total_cell = wg.cell(row=r, column=8, value=f'=IF(COUNT(E{r}:G{r})=0,"",SUM(E{r}:G{r}))')
    total_cell.font = Font(name=FONT, size=10, bold=True)
    total_cell.alignment = Alignment(horizontal="center", vertical="center")
    for col in range(1, last_col_g + 1):
        cell = wg.cell(row=r, column=col)
        cell.border = box
        if cell.font.name != FONT:
            cell.font = Font(name=FONT, size=10)
        if col in (4, 5, 6, 7):
            cell.alignment = Alignment(horizontal="center", vertical="center")
    wg.row_dimensions[r].height = 19

last_data_g = first_data_g + len(roster) - 1

for col in range(1, last_col_g + 1):
    top = wg.cell(row=HDR_ROW, column=col)
    top.border = Border(left=top.border.left, right=top.border.right, top=medium, bottom=top.border.bottom)
    bot = wg.cell(row=last_data_g, column=col)
    bot.border = Border(left=bot.border.left, right=bot.border.right, top=bot.border.top, bottom=medium)
for row in range(HDR_ROW, last_data_g + 1):
    lft = wg.cell(row=row, column=1)
    lft.border = Border(left=medium, right=lft.border.right, top=lft.border.top, bottom=lft.border.bottom)
    rgt = wg.cell(row=row, column=last_col_g)
    rgt.border = Border(left=rgt.border.left, right=medium, top=rgt.border.top, bottom=rgt.border.bottom)
for row in range(HDR_ROW, last_data_g + 1):
    c = wg.cell(row=row, column=4)
    c.border = Border(left=medium, right=c.border.right, top=c.border.top, bottom=c.border.bottom)

foot_row = last_data_g + 2
wg.merge_cells(start_row=foot_row, start_column=1, end_row=foot_row, end_column=last_col_g)
f1 = wg.cell(row=foot_row, column=1, value=f"Total students on roll: {len(roster)}")
f1.font = Font(name=FONT, size=9, color="404040")
f1.alignment = Alignment(horizontal="left", vertical="center")

foot_row2 = foot_row + 1
wg.merge_cells(start_row=foot_row2, start_column=1, end_row=foot_row2, end_column=last_col_g)
f2 = wg.cell(row=foot_row2, column=1,
             value="Understanding — got the core idea right   ·   Clarity — followable in under 2 min   ·   Insight — a genuine reaction, not a summary")
f2.font = Font(name=FONT, size=8, italic=True, color="555555")
f2.alignment = Alignment(horizontal="left", vertical="center")

wg.column_dimensions["A"].width = W["sr"]
wg.column_dimensions["B"].width = W["roll"]
wg.column_dimensions["C"].width = W["name"]
wg.column_dimensions["D"].width = W["group"]
for col_letter in ("E", "F", "G"):
    wg.column_dimensions[col_letter].width = W["crit"]
wg.column_dimensions["H"].width = W["total"]

wg.row_dimensions[1].height = 22
wg.row_dimensions[2].height = 18
wg.row_dimensions[3].height = 14

wg.page_setup.orientation = "portrait"
wg.page_setup.paperSize = wg.PAPERSIZE_A4
wg.page_setup.fitToWidth = 1
wg.page_setup.fitToHeight = 1
wg.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
wg.page_margins.left = wg.page_margins.right = 0.4
wg.page_margins.top = wg.page_margins.bottom = 0.4
wg.page_margins.header = wg.page_margins.footer = 0.2
wg.print_options.horizontalCentered = True
wg.print_title_rows = f"{HDR_ROW}:{HDR_ROW}"
wg.freeze_panes = wg.cell(row=first_data_g, column=3)


# ================================================================== GROUPS
wgr = wb.create_sheet("Groups")
last_col_gr = 3
last_letter_gr = get_column_letter(last_col_gr)

wgr.merge_cells(f"A1:{last_letter_gr}1")
wgr["A1"] = "BB 101  —  BIOLOGY   |   GROUP ACTIVITY — GROUPS"
wgr["A1"].font = Font(name=FONT, size=15, bold=True)
wgr["A1"].alignment = Alignment(horizontal="center", vertical="center")

wgr.merge_cells(f"A2:{last_letter_gr}2")
wgr["A2"] = "Tutorial Batch T1        Room: LT 206        TA: Aritra        Date: 10.08.2026"
wgr["A2"].font = Font(name=FONT, size=11, bold=True)
wgr["A2"].alignment = Alignment(horizontal="center", vertical="center")

wgr.merge_cells(f"A3:{last_letter_gr}3")
wgr["A3"] = "Group 1 formed by the students themselves; Groups 2-3 assigned at random from the rest of the roster."
wgr["A3"].font = Font(name=FONT, size=9, italic=True, color="555555")
wgr["A3"].alignment = Alignment(horizontal="center", vertical="center")

r = 5
for label, srs in GROUPS.items():
    wgr.merge_cells(start_row=r, start_column=1, end_row=r, end_column=last_col_gr)
    gh = wgr.cell(row=r, column=1, value=f"{label} — {len(srs)} members")
    gh.font = Font(name=FONT, size=11.5, bold=True)
    gh.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    gh.fill = header_fill
    for col in range(1, last_col_gr + 1):
        wgr.cell(row=r, column=col).border = box
    r += 1

    for col, htext in enumerate(("Sr.", "Roll No.", "Name of Student"), start=1):
        c = wgr.cell(row=r, column=col, value=htext)
        c.font = Font(name=FONT, size=9.5, bold=True)
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = box
    r += 1

    for sr in sorted(srs):
        roll, name = roster[sr - 1]
        wgr.cell(row=r, column=1, value=sr).alignment = Alignment(horizontal="center", vertical="center")
        wgr.cell(row=r, column=2, value=roll).alignment = Alignment(horizontal="center", vertical="center")
        wgr.cell(row=r, column=3, value=name).alignment = Alignment(horizontal="left", vertical="center", indent=1)
        for col in range(1, last_col_gr + 1):
            cell = wgr.cell(row=r, column=col)
            cell.border = box
            cell.font = Font(name=FONT, size=10)
        r += 1
    r += 1  # spacer row between groups

wgr.column_dimensions["A"].width = 6
wgr.column_dimensions["B"].width = 13
wgr.column_dimensions["C"].width = 32
wgr.row_dimensions[1].height = 22
wgr.row_dimensions[2].height = 18
wgr.row_dimensions[3].height = 14

wgr.page_setup.orientation = "portrait"
wgr.page_setup.paperSize = wgr.PAPERSIZE_A4
wgr.page_setup.fitToWidth = 1
wgr.page_setup.fitToHeight = 1
wgr.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
wgr.page_margins.left = wgr.page_margins.right = 0.4
wgr.page_margins.top = wgr.page_margins.bottom = 0.4
wgr.page_margins.header = wgr.page_margins.footer = 0.2
wgr.print_options.horizontalCentered = True

wb.save(OUTPUT)
print(f"wrote {OUTPUT}: sheets={wb.sheetnames}, {len(roster)} students, dates={dates}, groups={list(GROUPS)}")
