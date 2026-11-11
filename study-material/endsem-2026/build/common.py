"""Shared print stylesheet and small SVG helpers for the end-sem PDFs."""
import math

CSS = r"""
@page { size: A4; margin: 15mm 14mm 17mm 14mm; }
:root{
  --ink:#1b2333; --muted:#5b6475; --line:#d6dbe4;
  --navy:#1f4e79; --navy-t:#eaf1f8;
  --teal:#0f6e66; --teal-t:#e8f4f2;
  --amber:#a8540a; --amber-t:#fcf3e6;
  --red:#b3261e; --red-t:#fbecea;
  --violet:#5b3e96; --violet-t:#f1edf8;
}
*{ box-sizing:border-box; }
html{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body{ margin:0; font-family:"Charter","Bitstream Charter","DejaVu Serif",serif; font-size:10.2pt;
      line-height:1.42; color:var(--ink); background:#fff; }
h1,h2,h3,h4,.sans,th,.tag,.qn,.chip,.ans-id{ font-family:"Inter","DejaVu Sans",sans-serif; }
h1{ font-size:24pt; line-height:1.15; margin:0 0 6pt; color:var(--navy); letter-spacing:-0.01em; }
h2{ font-size:15pt; margin:0 0 8pt; color:#fff; background:var(--navy); padding:7pt 10pt; border-radius:4pt;
    break-after:avoid; }
h2 .sub{ display:block; font-size:9pt; font-weight:500; opacity:.9; margin-top:2pt; }
h3{ font-size:11.5pt; margin:12pt 0 5pt; color:var(--navy); break-after:avoid; border-bottom:1.2pt solid var(--line); padding-bottom:2pt; }
h4{ font-size:10pt; margin:9pt 0 3pt; color:var(--teal); break-after:avoid; }
p{ margin:0 0 6pt; }
ul,ol{ margin:2pt 0 6pt; padding-left:15pt; }
li{ margin:1pt 0; }
sup,sub{ line-height:0; }
.page-break{ break-before:page; }
.muted{ color:var(--muted); }
.small{ font-size:8.8pt; }
table{ border-collapse:collapse; width:100%; margin:4pt 0 8pt; font-size:9.3pt; }
tr{ break-inside:avoid; }
thead{ display:table-header-group; }
table.keep{ break-inside:avoid; }
th{ background:var(--navy-t); color:var(--navy); font-weight:600; font-size:8.8pt; text-align:left; }
th,td{ border:0.7pt solid var(--line); padding:3.5pt 5pt; vertical-align:top; }
td.c, th.c{ text-align:center; }
.box{ border-radius:4pt; padding:6pt 9pt; margin:6pt 0 8pt; break-inside:avoid; }
.box > :last-child{ margin-bottom:0; }
.box .bt{ font-family:"Inter",sans-serif; font-weight:700; font-size:8.6pt; letter-spacing:.04em; text-transform:uppercase; display:block; margin-bottom:2pt; }
.remember{ background:var(--teal-t); border-left:3pt solid var(--teal); }
.remember .bt{ color:var(--teal); }
.trap{ background:var(--red-t); border-left:3pt solid var(--red); }
.trap .bt{ color:var(--red); }
.tip{ background:var(--amber-t); border-left:3pt solid var(--amber); }
.tip .bt{ color:var(--amber); }
.note{ background:var(--violet-t); border-left:3pt solid var(--violet); }
.note .bt{ color:var(--violet); }
.two{ display:grid; grid-template-columns:1fr 1fr; gap:10pt; }
.two > *{ min-width:0; }
.fig{ text-align:center; margin:4pt 0 8pt; break-inside:avoid; }
svg{ max-width:100%; height:auto; }
.fig .cap{ font-size:8.5pt; color:var(--muted); margin-top:2pt; }
.k{ font-weight:700; }
.g{ font-style:italic; }
.ref{ font-family:"Inter",sans-serif; font-size:7.6pt; color:var(--muted); white-space:nowrap; }

/* ---------- cover ---------- */
.cover{ height:262mm; display:flex; flex-direction:column; }
.cover .band{ background:var(--navy); color:#fff; border-radius:6pt; padding:22pt 22pt 18pt; }
.cover .band h1{ color:#fff; font-size:27pt; margin-bottom:8pt; }
.cover .band .kicker{ font-family:"Inter",sans-serif; font-size:10pt; letter-spacing:.12em; text-transform:uppercase; opacity:.85; }
.cover .band .lede{ font-size:11pt; opacity:.95; margin:0; }
.cover .meta{ display:grid; grid-template-columns:repeat(3,1fr); gap:8pt; margin:14pt 0; }
.cover .meta div{ border:0.8pt solid var(--line); border-radius:4pt; padding:7pt 9pt; font-size:9pt; }
.cover .meta b{ display:block; font-family:"Inter",sans-serif; font-size:8pt; color:var(--muted); letter-spacing:.05em; text-transform:uppercase; margin-bottom:1pt; }
.toc{ list-style:none; padding:0; margin:4pt 0; }
.toc li{ display:flex; gap:8pt; padding:5pt 0; border-bottom:0.7pt dotted var(--line); }
.toc .n{ font-family:"Inter",sans-serif; font-weight:700; color:var(--navy); min-width:22pt; }
.cover .foot{ margin-top:auto; font-size:8.6pt; color:var(--muted); }

/* ---------- questions ---------- */
.q{ break-inside:avoid; margin:0 0 9pt; padding:0 0 7pt; border-bottom:0.6pt solid #eceff4; }
.qh{ display:flex; align-items:baseline; gap:6pt; margin-bottom:2pt; }
.qn{ font-weight:700; color:var(--navy); font-size:9.6pt; min-width:24pt; }
.chip{ font-size:6.9pt; font-weight:600; letter-spacing:.05em; text-transform:uppercase; padding:1pt 4.5pt; border-radius:8pt;
       background:var(--navy-t); color:var(--navy); white-space:nowrap; }
.chip.multi{ background:var(--amber-t); color:var(--amber); }
.chip.match{ background:var(--teal-t); color:var(--teal); }
.chip.num{ background:var(--violet-t); color:var(--violet); }
.chip.ar{ background:#eef0f3; color:#3d4656; }
.chip.short{ background:var(--red-t); color:var(--red); }
.marks{ margin-left:auto; font-family:"Inter",sans-serif; font-size:8pt; color:var(--muted); white-space:nowrap; }
.stem{ margin:1pt 0 3pt 30pt; }
.opts{ list-style:none; margin:2pt 0 0 30pt; padding:0; display:grid; grid-template-columns:1fr 1fr; column-gap:14pt; row-gap:1.5pt; }
.opts.one{ grid-template-columns:1fr; }
.opts li{ margin:0; padding-left:17pt; text-indent:-17pt; }
.opts .L{ font-family:"Inter",sans-serif; font-weight:600; color:var(--navy); font-size:8.8pt; display:inline-block; width:17pt; text-indent:0; }
.mt{ margin:3pt 0 0 30pt; width:calc(100% - 30pt); }
.mt td{ width:50%; }
.mt td .L{ font-family:"Inter",sans-serif; font-weight:600; color:var(--navy); font-size:8.8pt; margin-right:4pt; }
.ar-box{ margin:1pt 0 2pt 30pt; }
.ar-box div{ margin:1pt 0; }
.ar-key{ margin:3pt 0 0 30pt; font-size:8.8pt; color:var(--muted); }
.blank{ display:inline-block; min-width:52pt; border-bottom:0.8pt solid var(--ink); height:9pt; margin:0 2pt; }
.lines{ margin:4pt 0 0 30pt; }
.lines div{ border-bottom:0.6pt solid #c9ced8; height:15pt; }
.qfig{ margin:4pt 0 2pt 30pt; }

/* ---------- answers ---------- */
.ans{ break-inside:avoid; margin:0 0 6pt; padding:0 0 5pt; border-bottom:0.6pt solid #eceff4; display:grid; grid-template-columns:30pt 1fr; column-gap:4pt; }
.ans-id{ font-weight:700; color:var(--navy); font-size:9.2pt; }
.ans .a{ font-weight:700; color:var(--red); }
.ans .e{ font-size:9.4pt; }
.ans .e p{ margin:1pt 0 2pt; }
.work{ font-size:9.2pt; background:#f6f7f9; border-radius:3pt; padding:3pt 6pt; margin:2pt 0; }
"""


def page(title, body, extra_css=""):
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            f"<title>{title}</title><style>{CSS}{extra_css}</style></head><body>{body}</body></html>")


# ---------------------------------------------------------------- SVG helpers
def pedigree_svg():
    """Two small pedigrees: Family 1 (unaffected x unaffected -> affected child),
    Family 2 (affected x affected -> unaffected child). Filled = affected."""
    S = 22  # symbol size

    def sq(x, y, filled):
        return (f"<rect x='{x - S/2}' y='{y - S/2}' width='{S}' height='{S}' "
                f"fill='{'#1b2333' if filled else '#fff'}' stroke='#1b2333' stroke-width='1.6'/>")

    def ci(x, y, filled):
        return (f"<circle cx='{x}' cy='{y}' r='{S/2}' fill='{'#1b2333' if filled else '#fff'}' "
                f"stroke='#1b2333' stroke-width='1.6'/>")

    def family(ox, label, parents, kids):
        # parents: (male_filled, female_filled); kids: list of ('m'|'f', filled)
        y1, y2 = 40, 120
        px1, px2 = ox + 60, ox + 160
        out = [f"<text x='{ox + 110}' y='14' text-anchor='middle' font-family='Inter' font-size='12' font-weight='700' fill='#1f4e79'>{label}</text>",
               sq(px1, y1, parents[0]), ci(px2, y1, parents[1]),
               f"<line x1='{px1 + S/2}' y1='{y1}' x2='{px2 - S/2}' y2='{y1}' stroke='#1b2333' stroke-width='1.6'/>",
               f"<line x1='{(px1 + px2)/2}' y1='{y1}' x2='{(px1 + px2)/2}' y2='{y1 + 40}' stroke='#1b2333' stroke-width='1.6'/>"]
        n = len(kids)
        xs = [ox + 110 + (i - (n - 1) / 2) * 62 for i in range(n)]
        out.append(f"<line x1='{xs[0]}' y1='{y1 + 40}' x2='{xs[-1]}' y2='{y1 + 40}' stroke='#1b2333' stroke-width='1.6'/>")
        for x, (sex, f) in zip(xs, kids):
            out.append(f"<line x1='{x}' y1='{y1 + 40}' x2='{x}' y2='{y2 - S/2}' stroke='#1b2333' stroke-width='1.6'/>")
            out.append(sq(x, y2, f) if sex == "m" else ci(x, y2, f))
        return "".join(out)

    gen = ("<text x='6' y='45' font-family='Inter' font-size='11' font-weight='700' fill='#5b6475'>I</text>"
           "<text x='6' y='125' font-family='Inter' font-size='11' font-weight='700' fill='#5b6475'>II</text>")
    f1 = family(20, "Family 1", (False, False), [("m", False), ("f", True), ("m", False)])
    f2 = family(270, "Family 2", (True, True), [("f", True), ("m", False), ("f", True)])
    key = ("<g font-family='Inter' font-size='10' fill='#1b2333'>"
           "<rect x='520' y='30' width='12' height='12' fill='#fff' stroke='#1b2333' stroke-width='1.3'/><text x='538' y='40'>male</text>"
           "<circle cx='526' cy='58' r='6' fill='#fff' stroke='#1b2333' stroke-width='1.3'/><text x='538' y='62'>female</text>"
           "<rect x='520' y='74' width='12' height='12' fill='#1b2333'/><text x='538' y='84'>affected</text>"
           "<rect x='520' y='96' width='12' height='12' fill='#fff' stroke='#1b2333' stroke-width='1.3'/><text x='538' y='106'>unaffected</text></g>")
    return f"<svg viewBox='0 0 600 140' width='560' height='131' xmlns='http://www.w3.org/2000/svg'>{gen}{f1}{f2}{key}</svg>"


def cell_cycle_svg():
    """Cell-cycle wheel: G1, S, G2 (interphase) and M phase (mitosis + cytokinesis)."""
    cx, cy, R, r = 120, 120, 100, 52
    segs = [("G1", 0.40, "#cfe0f1", "#1f4e79"), ("S", 0.30, "#d7ece8", "#0f6e66"),
            ("G2", 0.20, "#f6e3c8", "#a8540a"), ("M", 0.10, "#f3d3cf", "#b3261e")]
    out, a0 = [], -90.0
    for name, frac, fill, txt in segs:
        a1 = a0 + frac * 360
        large = 1 if frac > 0.5 else 0
        p = lambda a, rad: (cx + rad * math.cos(math.radians(a)), cy + rad * math.sin(math.radians(a)))
        (x0, y0), (x1, y1) = p(a0, R), p(a1, R)
        (x2, y2), (x3, y3) = p(a1, r), p(a0, r)
        out.append(f"<path d='M{x0:.1f},{y0:.1f} A{R},{R} 0 {large} 1 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} "
                   f"A{r},{r} 0 {large} 0 {x3:.1f},{y3:.1f} Z' fill='{fill}' stroke='#fff' stroke-width='2'/>")
        am = (a0 + a1) / 2
        tx, ty = p(am, (R + r) / 2)
        out.append(f"<text x='{tx:.1f}' y='{ty + 5:.1f}' text-anchor='middle' font-family='Inter' font-weight='700' font-size='15' fill='{txt}'>{name}</text>")
        a0 = a1
    out.append(f"<text x='{cx}' y='{cy - 4}' text-anchor='middle' font-family='Inter' font-size='10.5' font-weight='600' fill='#1b2333'>INTERPHASE</text>")
    out.append(f"<text x='{cx}' y='{cy + 10}' text-anchor='middle' font-family='Inter' font-size='9' fill='#5b6475'>G1 + S + G2 (~90%)</text>")
    labels = ("<g font-family='Inter' font-size='11' fill='#1b2333'>"
              "<text x='245' y='52'><tspan font-weight='700' fill='#1f4e79'>G1</tspan> growth</text>"
              "<text x='245' y='80'><tspan font-weight='700' fill='#0f6e66'>S</tspan> DNA synthesis</text>"
              "<text x='257' y='95' font-size='9.5' fill='#5b6475'>chromosomes duplicate</text>"
              "<text x='245' y='123'><tspan font-weight='700' fill='#a8540a'>G2</tspan> prepares to divide</text>"
              "<text x='245' y='151'><tspan font-weight='700' fill='#b3261e'>M</tspan> mitosis</text>"
              "<text x='257' y='166' font-size='9.5' fill='#5b6475'>+ cytokinesis</text>"
              "<text x='245' y='200' font-size='9' fill='#5b6475'>time runs clockwise from the top</text></g>")
    return f"<svg viewBox='0 0 420 240' width='400' height='229' xmlns='http://www.w3.org/2000/svg'>{''.join(out)}{labels}</svg>"


def box_flow_svg(steps, width=680, h=64, note=None, colors=None):
    """Horizontal chain of boxes joined by arrows. steps: list of (title, subtitle)."""
    n = len(steps)
    gap = 18
    bw = (width - 10 - gap * (n - 1)) / n
    colors = colors or ["#eaf1f8"] * n
    out = ["<defs><marker id='ah' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto'>"
           "<path d='M0,0 L10,5 L0,10 z' fill='#1f4e79'/></marker></defs>"]
    for i, (t, s) in enumerate(steps):
        x = 5 + i * (bw + gap)
        out.append(f"<rect x='{x:.1f}' y='6' width='{bw:.1f}' height='{h}' rx='6' fill='{colors[i]}' stroke='#1f4e79' stroke-width='1'/>")
        out.append(f"<text x='{x + bw/2:.1f}' y='{6 + h/2 - 3:.1f}' text-anchor='middle' font-family='Inter' font-size='12' font-weight='700' fill='#1b2333'>{t}</text>")
        if s:
            out.append(f"<text x='{x + bw/2:.1f}' y='{6 + h/2 + 14:.1f}' text-anchor='middle' font-family='Inter' font-size='10' fill='#5b6475'>{s}</text>")
        if i < n - 1:
            out.append(f"<line x1='{x + bw + 1:.1f}' y1='{6 + h/2:.1f}' x2='{x + bw + gap - 2:.1f}' y2='{6 + h/2:.1f}' stroke='#1f4e79' stroke-width='1.6' marker-end='url(#ah)'/>")
    H = h + 14
    if note:
        out.append(f"<text x='{width/2}' y='{h + 31}' text-anchor='middle' font-family='Inter' font-size='10.5' fill='#5b6475'>{note}</text>")
        H += 24
    return f"<svg viewBox='0 0 {width} {H}' width='{width}' height='{H}' xmlns='http://www.w3.org/2000/svg'>{''.join(out)}</svg>"


def gprotein_cycle_svg():
    out = ["<defs><marker id='ag' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto'>"
           "<path d='M0,0 L10,5 L0,10 z' fill='#1b2333'/></marker></defs>",
           "<rect x='4' y='58' width='128' height='54' rx='8' fill='#eef0f3' stroke='#5b6475'/>",
           "<text x='68' y='81' text-anchor='middle' font-family='Inter' font-weight='700' font-size='12.5'>G protein–GDP</text>",
           "<text x='68' y='99' text-anchor='middle' font-family='Inter' font-size='11' fill='#5b6475'>OFF</text>",
           "<rect x='208' y='58' width='128' height='54' rx='8' fill='#d7ece8' stroke='#0f6e66'/>",
           "<text x='272' y='81' text-anchor='middle' font-family='Inter' font-weight='700' font-size='12.5'>G protein–GTP</text>",
           "<text x='272' y='99' text-anchor='middle' font-family='Inter' font-size='11' fill='#0f6e66'>ON</text>",
           "<path d='M100,56 C140,22 200,22 240,56' fill='none' stroke='#1b2333' stroke-width='1.6' marker-end='url(#ag)'/>",
           "<text x='170' y='14' text-anchor='middle' font-family='Inter' font-size='11'>activated GPCR:</text>",
           "<text x='170' y='28' text-anchor='middle' font-family='Inter' font-size='11'>GDP out, GTP in</text>",
           "<path d='M240,114 C200,148 140,148 100,114' fill='none' stroke='#1b2333' stroke-width='1.6' marker-end='url(#ag)'/>",
           "<text x='170' y='160' text-anchor='middle' font-family='Inter' font-size='11'>own GTPase: GTP → GDP + P<tspan font-size='8' dy='3'>i</tspan></text>"]
    return f"<svg viewBox='0 0 340 168' width='340' height='168' xmlns='http://www.w3.org/2000/svg'>{''.join(out)}</svg>"


def selection_svg():
    """Three panels: directional, disruptive, stabilizing. Dashed = original, solid = after selection."""
    def gauss(mu, sd, amp, x0, w, base, h):
        pts = []
        for i in range(61):
            t = i / 60
            xv = t * 10
            yv = amp * math.exp(-((xv - mu) ** 2) / (2 * sd * sd))
            pts.append(f"{x0 + t * w:.1f},{base - yv * h:.1f}")
        return " ".join(pts)

    def bimodal(x0, w, base, h):
        pts = []
        for i in range(61):
            t = i / 60
            xv = t * 10
            yv = 0.75 * math.exp(-((xv - 3.2) ** 2) / 1.4) + 0.75 * math.exp(-((xv - 6.8) ** 2) / 1.4)
            pts.append(f"{x0 + t * w:.1f},{base - yv * h:.1f}")
        return " ".join(pts)

    panels = [("Directional", "one extreme favoured; mean shifts", gauss(6.6, 1.5, 1.0, 0, 150, 100, 70)),
              ("Disruptive (diversifying)", "both extremes favoured", bimodal(0, 150, 100, 70)),
              ("Stabilizing", "intermediates favoured; variation shrinks", gauss(5, 0.95, 1.0, 0, 150, 100, 70))]
    out = []
    for i, (t, s, solid) in enumerate(panels):
        ox = 10 + i * 190
        orig = gauss(5, 1.5, 0.85, 0, 150, 100, 70)
        out.append(f"<g transform='translate({ox},20)'>"
                   f"<rect x='0' y='0' width='150' height='100' fill='#f6f7f9'/>"
                   f"<polyline points='{orig}' fill='none' stroke='#8a93a3' stroke-width='1.6' stroke-dasharray='4 3'/>"
                   f"<polyline points='{solid}' fill='none' stroke='#1f4e79' stroke-width='2.2'/>"
                   f"<line x1='0' y1='100' x2='150' y2='100' stroke='#1b2333'/>"
                   f"<text x='75' y='116' text-anchor='middle' font-family='Inter' font-size='8.5' fill='#5b6475'>phenotype →</text>"
                   f"<text x='75' y='134' text-anchor='middle' font-family='Inter' font-size='10.5' font-weight='700'>{t}</text>"
                   f"<text x='75' y='148' text-anchor='middle' font-family='Inter' font-size='8.8' fill='#5b6475'>{s}</text></g>")
    legend = ("<g font-family='Inter' font-size='9' fill='#1b2333'>"
              "<line x1='160' y1='8' x2='185' y2='8' stroke='#8a93a3' stroke-width='1.6' stroke-dasharray='4 3'/><text x='190' y='11'>original population</text>"
              "<line x1='300' y1='8' x2='325' y2='8' stroke='#1f4e79' stroke-width='2.2'/><text x='330' y='11'>after selection</text></g>")
    return f"<svg viewBox='0 0 580 172' width='540' height='160' xmlns='http://www.w3.org/2000/svg'>{legend}{''.join(out)}</svg>"
