"""Build the printable reading list handout: 12 real, current articles on
DNA/RNA developments for the Tutorial 2 group activity, in case groups
don't find their own or want the TA to assign one.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.pdfbase.pdfmetrics import stringWidth

OUTPUT = "BB101_T2_Reading_List.pdf"

ARTICLES = [
    ("Medicine", [
        ("This CRISPR breakthrough turns genes on without cutting DNA",
         "ScienceDaily, Jan 2026",
         "Editing without cutting — a gentler, safer route to treating sickle cell disease by reactivating a dormant gene.",
         "https://www.sciencedaily.com/releases/2026/01/260104202813.htm"),
        ("First-in-human trial of CRISPR gene-editing therapy safely lowered cholesterol, triglycerides",
         "American Heart Association Newsroom, Nov 2025",
         "A one-time CRISPR injection, permanently lowering heart-disease risk. Fifteen patients in.",
         "https://newsroom.heart.org/news/first-in-human-trial-of-crispr-gene-editing-therapy-safely-lowered-cholesterol-triglycerides"),
        ("MIT's new precision gene editing tool could transform medicine",
         "ScienceDaily, Oct 2025",
         "A fix for one of prime editing's biggest weaknesses — accuracy — that could widen what gene therapy can treat.",
         "https://www.sciencedaily.com/releases/2025/10/251010091553.htm"),
    ]),
    ("RNA medicine", [
        ("First mRNA flu shot approved by FDA bodes well for improving drugs of the future",
         "The Conversation",
         "Why the same mRNA platform behind COVID vaccines is now moving into flu, cancer, and rare-disease treatment.",
         "https://theconversation.com/first-mrna-flu-shot-approved-by-fda-bodes-well-for-improving-drugs-of-the-future-though-a-few-hurdles-remain-before-mrna-can-move-beyond-vaccines-289277"),
    ]),
    ("Computing & AI", [
        ("World's first scalable DNA data storage device unveiled by US firm",
         "Interesting Engineering, Dec 2025",
         "Data written into synthetic DNA for archival storage — a medium that can outlast every hard drive by millennia.",
         "https://interestingengineering.com/innovation/world-first-scalable-dna-data-storage"),
        ("DNA data storage: AI method speeds up data retrieval by 3,200 times",
         "Tech Xplore, Mar 2025",
         "The bottleneck in DNA storage was never writing data — it was reading it back out. AI just closed that gap.",
         "https://techxplore.com/news/2025-03-dna-storage-ai-method.html"),
        ("AlphaFold is five years old — these charts show how it revolutionized science",
         "Nature, 2025",
         "An AI that predicts protein shape from sequence alone, now behind roughly 40% of all newly solved structures.",
         "https://www.nature.com/articles/d41586-025-03886-9"),
    ]),
    ("Evolution & origins", [
        ("Landmark ancient-genome study shows surprise acceleration of human evolution",
         "Nature News, Apr 2026",
         "DNA from over 15,000 ancient people shows natural selection sped up, not slowed down, in the last 10,000 years.",
         "https://www.nature.com/articles/d41586-026-01204-5"),
        ("The $10 Billion Company Behind The Dire Wolf Is Now Bringing Back Mammoths",
         "Forbes, Apr 2026",
         "Gene-edited gray wolves engineered to resemble an extinct species — genuine science, or marketing? Good debate fuel.",
         "https://www.forbes.com/sites/jonmarkman/2026/04/09/the-10b-company-behind-the-dire-wolf-is-now-bringing-back-mammoths/"),
    ]),
    ("Synthetic biology & ethics", [
        ("Why a synthetic human genome is still worth building",
         "Nature, Comment",
         "Scientists can now write DNA from scratch, not just read it. Should they — for a human genome?",
         "https://www.nature.com/articles/d41586-026-01725-z"),
        ("23andMe bankruptcy filing sparks privacy fears as DNA data of millions goes up for sale",
         "NBC News, 2025",
         "What happens to your genetic data when the company holding it goes bankrupt? Millions of users just found out.",
         "https://www.nbcnews.com/tech/security/23andme-goes-bankrupt-millions-peoples-dna-data-sale-rcna197874"),
    ]),
    ("Public health", [
        ("New Gene Drive Stops the Spread of Malaria — Without Killing Any Mosquitoes",
         "Singularity Hub, Dec 2025",
         "A self-limiting CRISPR gene drive that blocks malaria transmission instead of wiping out the mosquito population.",
         "https://singularityhub.com/2025/12/18/this-gene-drive-stops-the-spread-of-real-world-malaria-without-killing-any-mosquitoes/"),
    ]),
]

styles = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=16, leading=19,
                             alignment=TA_LEFT, spaceAfter=2, textColor=colors.black),
    "subtitle": ParagraphStyle("subtitle", fontName="Helvetica", fontSize=10.5, leading=13,
                                textColor=colors.HexColor("#404040"), spaceAfter=1),
    "intro": ParagraphStyle("intro", fontName="Helvetica-Oblique", fontSize=9, leading=12.5,
                             textColor=colors.HexColor("#555555"), spaceAfter=10),
    "theme": ParagraphStyle("theme", fontName="Helvetica-Bold", fontSize=10.5, leading=13,
                             textColor=colors.HexColor("#C9691F"), spaceBefore=10, spaceAfter=4,
                             tracking=0.6),
    "artTitle": ParagraphStyle("artTitle", fontName="Helvetica-Bold", fontSize=10.3, leading=13,
                                textColor=colors.black, spaceAfter=1),
    "artMeta": ParagraphStyle("artMeta", fontName="Helvetica-Oblique", fontSize=8.3, leading=10.5,
                               textColor=colors.HexColor("#6A6A6A"), spaceAfter=3),
    "artHook": ParagraphStyle("artHook", fontName="Helvetica", fontSize=9.2, leading=12,
                               textColor=colors.HexColor("#262626"), spaceAfter=2),
    "artUrl": ParagraphStyle("artUrl", fontName="Courier", fontSize=7.6, leading=10,
                              textColor=colors.HexColor("#3454D1"), spaceAfter=9),
}

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=16 * mm, rightMargin=16 * mm, topMargin=14 * mm, bottomMargin=14 * mm,
    title="BB 101 Tutorial 2 — DNA/RNA Reading List",
)

story = []
story.append(Paragraph("BB 101 — Biology  |  DNA &amp; RNA Reading List", styles["title"]))
story.append(Paragraph("Tutorial 2 group activity &nbsp;&middot;&nbsp; Tutorial Batch T1 &nbsp;&middot;&nbsp; TA: Aritra", styles["subtitle"]))
story.append(Paragraph(
    "Twelve real, current pieces on where DNA/RNA science is right now — for groups that don't find their own, "
    "or if you'd rather assign one directly. Pick one per group of 3–4; ~10 minutes to read, ~5 to talk it over "
    "before presenting.", styles["intro"]))

n = 0
for theme, items in ARTICLES:
    story.append(Paragraph(theme.upper(), styles["theme"]))
    for title, meta, hook, url in items:
        n += 1
        story.append(KeepTogether([
            Paragraph(f"{n}.  {title}", styles["artTitle"]),
            Paragraph(meta, styles["artMeta"]),
            Paragraph(hook, styles["artHook"]),
            Paragraph(url, styles["artUrl"]),
        ]))

doc.build(story)
print(f"wrote {OUTPUT}: {n} articles across {len(ARTICLES)} themes")
