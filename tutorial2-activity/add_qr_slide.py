"""Append a closing slide with the reading-list QR code to a copy of the
Tutorial 2 deck. Matches the deck's own 13.333x7.5in widescreen canvas.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

DECK = "BB101_T2_DNA_Lecture.pptx"
QR = "qr_bare.png"
URL = "https://claude.ai/code/artifact/667ab17c-f452-4b89-8df7-2286ee64214f"

prs = Presentation(DECK)
layout = prs.slide_masters[0].slide_layouts[0]
slide = prs.slides.add_slide(layout)

# Remove any inherited placeholder shapes so the slide starts clean.
for shape in list(slide.shapes):
    shape._element.getparent().remove(shape._element)

SW, SH = prs.slide_width, prs.slide_height  # EMU

INK = RGBColor(0x1A, 0x1A, 0x2E)
SUB = RGBColor(0x55, 0x55, 0x66)

title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), SW - Inches(1.6), Inches(0.9))
tf = title_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "Go Deeper: DNA & RNA Right Now"
run.font.size = Pt(40)
run.font.bold = True
run.font.color.rgb = INK

sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), SW - Inches(1.6), Inches(0.5))
tf2 = sub_box.text_frame
tf2.word_wrap = True
p2 = tf2.paragraphs[0]
p2.alignment = PP_ALIGN.CENTER
run2 = p2.add_run()
run2.text = "Scan for 12 current articles on gene editing, RNA medicine, DNA storage, and more"
run2.font.size = Pt(18)
run2.font.color.rgb = SUB

# QR image, centered, square (bare 602x602 source)
qr_top = Inches(2.25)
qr_side = Inches(3.5)
img = slide.shapes.add_picture(QR, 0, 0, width=qr_side, height=qr_side)
img.left = int((SW - img.width) / 2)
img.top = qr_top

url_box = slide.shapes.add_textbox(Inches(0.8), qr_top + img.height + Inches(0.2), SW - Inches(1.6), Inches(0.4))
tf3 = url_box.text_frame
tf3.word_wrap = True
p3 = tf3.paragraphs[0]
p3.alignment = PP_ALIGN.CENTER
run3 = p3.add_run()
run3.text = URL
run3.font.size = Pt(13)
run3.font.color.rgb = SUB

prs.save(DECK)
print(f"wrote {DECK}: {len(prs.slides)} slides (added QR closing slide)")
