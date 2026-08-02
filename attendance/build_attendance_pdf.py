"""Build the print-ready A4 PDF attendance sheet for BB 101 Tutorial Batch T1.

One page, 31 students, seven blank date columns to fill in by hand.
"""

import sys

import openpyxl
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

SOURCE = sys.argv[1] if len(sys.argv) > 1 else "CourseList_Tutorail.xlsx"
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else "BB101_T1_Attendance.pdf"

N_DATE_COLS = 7

src = openpyxl.load_workbook(SOURCE)["T1"]
roster = []
for row in src.iter_rows(min_row=3, max_row=src.max_row, values_only=True):
    roll, name = row[1], row[2]
    if roll is None or name is None:
        continue
    roster.append((str(roll).strip(), str(name).strip()))

PAGE_W, PAGE_H = A4
M_L = M_R = 10 * mm
M_T = 11 * mm
M_B = 10 * mm
GRID_W = PAGE_W - M_L - M_R

W_SR = 9 * mm
W_ROLL = 24 * mm
W_DATE = 13.5 * mm
W_NAME = GRID_W - W_SR - W_ROLL - N_DATE_COLS * W_DATE

COL_X = [M_L, M_L + W_SR, M_L + W_SR + W_ROLL, M_L + W_SR + W_ROLL + W_NAME]
for i in range(N_DATE_COLS):
    COL_X.append(COL_X[3] + (i + 1) * W_DATE)

ROW_H = 7.0 * mm
HDR_TOP_H = 5.5 * mm
HDR_BOT_H = 8.5 * mm

INK = colors.black
GRID = colors.HexColor("#8C8C8C")
SHADE = colors.HexColor("#DCDCDC")
LIGHT = colors.HexColor("#F4F4F4")

c = canvas.Canvas(OUTPUT, pagesize=A4)
c.setTitle("BB 101 - Tutorial Batch T1 Attendance Sheet")

y = PAGE_H - M_T

# ------------------------------------------------------------------- heading
c.setFont("Helvetica-Bold", 14)
c.drawCentredString(PAGE_W / 2, y, "BB 101  —  BIOLOGY   |   ATTENDANCE SHEET")
y -= 6.0 * mm
c.setFont("Helvetica-Bold", 10.5)
c.drawCentredString(PAGE_W / 2, y, "Tutorial Batch T1        Room: LT 206        TA: Aritra")
y -= 4.6 * mm
c.setFont("Helvetica-Oblique", 8)
c.setFillColor(colors.HexColor("#555555"))
c.drawCentredString(PAGE_W / 2, y, "Mark  P = Present   /   A = Absent")
c.setFillColor(INK)
y -= 4.0 * mm

grid_top = y

# ---------------------------------------------------------------- header row
# top band
c.setFillColor(SHADE)
c.rect(M_L, grid_top - HDR_TOP_H, GRID_W, HDR_TOP_H, stroke=0, fill=1)
c.setFillColor(LIGHT)
c.rect(COL_X[3], grid_top - HDR_TOP_H - HDR_BOT_H, N_DATE_COLS * W_DATE, HDR_BOT_H, stroke=0, fill=1)
c.setFillColor(SHADE)
c.rect(M_L, grid_top - HDR_TOP_H - HDR_BOT_H, W_SR + W_ROLL + W_NAME, HDR_BOT_H, stroke=0, fill=1)
c.setFillColor(INK)

hdr_bot = grid_top - HDR_TOP_H - HDR_BOT_H
mid_y = (grid_top - HDR_TOP_H + hdr_bot) / 2 - 1.2 * mm

c.setFont("Helvetica-Bold", 9)
c.drawCentredString(COL_X[0] + W_SR / 2, mid_y, "Sr.")
c.drawCentredString(COL_X[1] + W_ROLL / 2, mid_y, "Roll No.")
c.drawString(COL_X[2] + 2.5 * mm, mid_y, "Name of Student")
c.drawCentredString(
    COL_X[3] + N_DATE_COLS * W_DATE / 2,
    grid_top - HDR_TOP_H + 1.7 * mm,
    "DATE   (write below)",
)

# ------------------------------------------------------------------ students
row_top = hdr_bot
c.setFont("Helvetica", 9)
for i, (roll, name) in enumerate(roster):
    ry = row_top - i * ROW_H
    base = ry - ROW_H + 2.3 * mm
    if i % 2 == 1:
        c.setFillColor(colors.HexColor("#FAFAFA"))
        c.rect(M_L, ry - ROW_H, GRID_W, ROW_H, stroke=0, fill=1)
        c.setFillColor(INK)
    c.setFont("Helvetica", 9)
    c.drawCentredString(COL_X[0] + W_SR / 2, base, str(i + 1))
    c.drawCentredString(COL_X[1] + W_ROLL / 2, base, roll)
    label = name
    while c.stringWidth(label, "Helvetica", 9) > W_NAME - 5 * mm and len(label) > 4:
        label = label[:-2]
    c.drawString(COL_X[2] + 2.5 * mm, base, label)

grid_bot = row_top - len(roster) * ROW_H

# --------------------------------------------------------------- totals row
tot_top = grid_bot
tot_bot = tot_top - ROW_H
c.setFillColor(SHADE)
c.rect(M_L, tot_bot, GRID_W, ROW_H, stroke=0, fill=1)
c.setFillColor(INK)
c.setFont("Helvetica-Bold", 9)
c.drawRightString(COL_X[3] - 2.5 * mm, tot_bot + 2.3 * mm, "TOTAL PRESENT")

# ------------------------------------------------------------------ gridlines
c.setStrokeColor(GRID)
c.setLineWidth(0.4)
# horizontal: every student row + totals (header split is drawn later, date block only)
for i in range(len(roster) + 1):
    yy = row_top - i * ROW_H
    c.line(M_L, yy, PAGE_W - M_R, yy)
# vertical — stop at the header split so the DATE band and the label block stay clean
for x in COL_X[1:] + [PAGE_W - M_R]:
    c.line(x, tot_bot, x, hdr_bot)

# outer frame + heavier separators
c.setStrokeColor(INK)
c.setLineWidth(1.1)
c.rect(M_L, tot_bot, GRID_W, grid_top - tot_bot, stroke=1, fill=0)
c.line(COL_X[3], tot_bot, COL_X[3], grid_top)
# divider between the two header rows, across the date block only
c.setLineWidth(0.4)
c.setStrokeColor(GRID)
c.line(COL_X[3], grid_top - HDR_TOP_H, PAGE_W - M_R, grid_top - HDR_TOP_H)
c.setStrokeColor(INK)
c.setLineWidth(1.1)
c.line(M_L, hdr_bot, PAGE_W - M_R, hdr_bot)
c.line(M_L, tot_top, PAGE_W - M_R, tot_top)

# --------------------------------------------------------------------- footer
fy = tot_bot - 7 * mm
c.setFont("Helvetica", 8.5)
c.setFillColor(colors.HexColor("#404040"))
c.drawString(M_L, fy, f"Total students on roll: {len(roster)}")
c.drawRightString(PAGE_W - M_R, fy, "TA Signature: __________________________")
c.setFillColor(INK)

c.showPage()
c.save()
print(f"wrote {OUTPUT}: {len(roster)} students, {N_DATE_COLS} date columns, 1 A4 page")
