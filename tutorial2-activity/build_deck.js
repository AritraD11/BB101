const pptxgen = require("pptxgenjs");

const V = "6B4E9E";      // haematoxylin violet — primary
const V_DARK = "2A2140"; // deep violet — title/closing bg
const V_SOFT = "EFEAF8"; // pale violet — light card fill
const E = "C9436E";      // eosin coral — accent
const E_SOFT = "FBE9F0";
const INK = "1A1726";
const INK2 = "46405C";
const INK3 = "6E6880";
const GOOD = "1D7A5F";
const GOOD_SOFT = "E2F2EC";
const WHITE = "FFFFFF";
const LINE = "DCD5EC";

const SERIF = "Cambria";
const SANS = "Calibri";

let p = new pptxgen();
p.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const SW = 13.333, SH = 7.5;

function titleBar(slide, text, opts = {}) {
  slide.addText(text, {
    x: 0.6, y: 0.35, w: SW - 1.2, h: 0.7,
    fontFace: SERIF, fontSize: opts.size || 30, bold: true, color: opts.color || INK,
    align: "left", valign: "middle",
  });
}
function eyebrow(slide, text, opts = {}) {
  slide.addText(text.toUpperCase(), {
    x: 0.6, y: 0.08, w: SW - 1.2, h: 0.3,
    fontFace: SANS, fontSize: 11, bold: true, color: opts.color || E,
    charSpacing: 2, align: "left",
  });
}
function pageNum(slide, n) {
  slide.addText(String(n), {
    x: SW - 0.7, y: SH - 0.5, w: 0.4, h: 0.3,
    fontFace: SANS, fontSize: 10, color: INK3, align: "right",
  });
}

// ============================================================ SLIDE 1 — TITLE
{
  const s = p.addSlide();
  s.background = { color: V_DARK };
  s.addText("DNA & RNA", {
    x: 0.9, y: 1.55, w: SW - 1.8, h: 1.3,
    fontFace: SERIF, fontSize: 60, bold: true, color: WHITE, align: "center",
  });
  s.addText("Nature's Code — How Life Stores, Copies & Reads Information", {
    x: 0.9, y: 2.75, w: SW - 1.8, h: 0.6,
    fontFace: SANS, fontSize: 19, color: "D8CCF0", align: "center",
  });

  const tiles = ["Nucleotides", "Nitrogenous Bases", "DNA & RNA", "Replication & Transcription", "Central Dogma & PCR"];
  const gap = 0.22, tw = (SW - 1.8 - gap * (tiles.length - 1)) / tiles.length;
  tiles.forEach((t, i) => {
    s.addShape("roundRect", {
      x: 0.9 + i * (tw + gap), y: 4.05, w: tw, h: 0.95,
      rectRadius: 0.08, fill: { color: "3A2F5C" }, line: { color: "5A4A8A", width: 1 },
    });
    s.addText(t, {
      x: 0.9 + i * (tw + gap) + 0.06, y: 4.05, w: tw - 0.12, h: 0.95,
      fontFace: SANS, fontSize: 12.5, bold: true, color: WHITE, align: "center", valign: "middle",
      breakLine: true,
    });
  });

  s.addText("BB 101 · Tutorial 2", {
    x: 0.9, y: 6.6, w: SW - 1.8, h: 0.4,
    fontFace: SANS, fontSize: 12, color: "9B8DC4", align: "center", charSpacing: 1,
  });
}

// ============================================================ SLIDE 2 — NUCLEOTIDES
{
  const s = p.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "Building Blocks");
  titleBar(s, "Structure of Nucleotides");

  const colW = 5.6;
  s.addText([
    { text: "A nucleotide has three parts:\n", options: { bold: true, color: INK, fontSize: 15 } },
  ], { x: 0.6, y: 1.35, w: colW, h: 0.4, fontFace: SANS });

  const parts = [
    ["1. Phosphate group", "The connector — links one nucleotide to the next.", E],
    ["2. Sugar (pentose)", "Ribose (RNA) or deoxyribose (DNA) — the backbone.", GOOD],
    ["3. Nitrogenous base", "A, T, G, C, or U — the actual information.", V],
  ];
  parts.forEach((row, i) => {
    const y = 1.85 + i * 0.85;
    s.addShape("roundRect", { x: 0.6, y, w: colW, h: 0.72, rectRadius: 0.06, fill: { color: V_SOFT }, line: { color: LINE, width: 0.75 } });
    s.addText(row[0], { x: 0.78, y: y + 0.06, w: colW - 0.4, h: 0.3, fontFace: SANS, fontSize: 13, bold: true, color: row[2] });
    s.addText(row[1], { x: 0.78, y: y + 0.35, w: colW - 0.4, h: 0.32, fontFace: SANS, fontSize: 11, color: INK2 });
  });

  s.addShape("roundRect", { x: 0.6, y: 4.65, w: colW, h: 1.55, rectRadius: 0.06, fill: { color: E_SOFT }, line: { color: "EAB9CB", width: 0.75 } });
  s.addText("Nucleoside vs Nucleotide", { x: 0.78, y: 4.75, w: colW - 0.4, h: 0.3, fontFace: SANS, fontSize: 12.5, bold: true, color: E });
  s.addText("A nucleoside is sugar + base only — no phosphate, not yet linked into a chain. Add the phosphate and it becomes a nucleotide, ready to join the strand. NMP / NDP / NTP just mean 1, 2, or 3 phosphates attached.", {
    x: 0.78, y: 5.05, w: colW - 0.4, h: 1.05, fontFace: SANS, fontSize: 10.5, color: INK2, valign: "top",
  });

  s.addImage({ path: "assets/nucleotide_panel.png", x: 6.75, y: 1.3, w: 6.0, h: 6.0 * (1024 / 883), sizing: { type: "contain", w: 6.0, h: 5.75 } });
  pageNum(s, 2);
}

// ============================================================ SLIDE 3 — BASES
{
  const s = p.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "Building Blocks");
  titleBar(s, "Structure of Nitrogenous Bases");

  s.addImage({ path: "assets/bases.png", x: 0.6, y: 1.3, w: 7.3, h: 7.3 * (381 / 564) });

  const rx = 8.3, rw = 4.4;
  s.addShape("roundRect", { x: rx, y: 1.3, w: rw, h: 1.55, rectRadius: 0.06, fill: { color: V_SOFT }, line: { color: LINE, width: 0.75 } });
  s.addText("Purines vs Pyrimidines", { x: rx + 0.2, y: 1.4, w: rw - 0.4, h: 0.3, fontFace: SANS, fontSize: 12.5, bold: true, color: V });
  s.addText("A & G = purines, two rings, “big.”  C, T, U = pyrimidines, one ring, “small.” Big always pairs with small — that’s what keeps the DNA ladder a constant width.", {
    x: rx + 0.2, y: 1.7, w: rw - 0.4, h: 1.1, fontFace: SANS, fontSize: 10.5, color: INK2,
  });

  s.addShape("roundRect", { x: rx, y: 3.05, w: rw, h: 1.85, rectRadius: 0.06, fill: { color: E_SOFT }, line: { color: "EAB9CB", width: 0.75 } });
  s.addText("Pairing Rule", { x: rx + 0.2, y: 3.15, w: rw - 0.4, h: 0.3, fontFace: SANS, fontSize: 12.5, bold: true, color: E });
  s.addText([
    { text: "A — T", options: { bold: true, color: INK } },
    { text: "  (or A—U in RNA), 2 hydrogen bonds\n", options: { color: INK2 } },
    { text: "G — C", options: { bold: true, color: INK } },
    { text: ", 3 hydrogen bonds — slightly stronger", options: { color: INK2 } },
  ], { x: rx + 0.2, y: 3.5, w: rw - 0.4, h: 1.3, fontFace: SANS, fontSize: 11.5, lineSpacing: 20 });

  s.addShape("roundRect", { x: rx, y: 5.1, w: rw, h: 1.5, rectRadius: 0.06, fill: { color: GOOD_SOFT }, line: { color: "B9DDD0", width: 0.75 } });
  s.addText("Why It Matters Later", { x: rx + 0.2, y: 5.2, w: rw - 0.4, h: 0.3, fontFace: SANS, fontSize: 12.5, bold: true, color: GOOD });
  s.addText("G-C rich DNA needs more heat to melt apart than A-T rich DNA — directly relevant to PCR’s temperatures, later in this deck.", {
    x: rx + 0.2, y: 5.5, w: rw - 0.4, h: 1.0, fontFace: SANS, fontSize: 10.5, color: INK2,
  });
  pageNum(s, 3);
}

// ============================================================ SLIDE 4 — DNA vs RNA
{
  const s = p.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "Structure");
  titleBar(s, "DNA & RNA: Structure of the Code");

  s.addImage({ path: "assets/dna_rna.png", x: 0.6, y: 1.25, w: 8.1, h: 8.1 * (980 / 1648) });

  const rx = 9.0, rw = 3.75;
  const dnaFacts = ["Double-stranded helix", "Millions of bases long", "Deoxyribose sugar — very stable", "Stays in the nucleus — the archive"];
  const rnaFacts = ["Single-stranded", "A few thousand bases long", "Ribose sugar — less stable, reactive", "Made, used, then discarded"];

  s.addShape("roundRect", { x: rx, y: 1.25, w: rw, h: 2.55, rectRadius: 0.06, fill: { color: V_SOFT }, line: { color: LINE, width: 0.75 } });
  s.addText("DNA", { x: rx + 0.2, y: 1.32, w: rw - 0.4, h: 0.35, fontFace: SERIF, fontSize: 16, bold: true, color: V });
  s.addText(dnaFacts.map((f) => ({ text: f, options: { bullet: { code: "2022" }, breakLine: true } })), {
    x: rx + 0.2, y: 1.72, w: rw - 0.4, h: 2.0, fontFace: SANS, fontSize: 10.5, color: INK2, paraSpaceAfter: 6,
  });

  s.addShape("roundRect", { x: rx, y: 3.95, w: rw, h: 2.55, rectRadius: 0.06, fill: { color: E_SOFT }, line: { color: "EAB9CB", width: 0.75 } });
  s.addText("RNA", { x: rx + 0.2, y: 4.02, w: rw - 0.4, h: 0.35, fontFace: SERIF, fontSize: 16, bold: true, color: E });
  s.addText(rnaFacts.map((f) => ({ text: f, options: { bullet: { code: "2022" }, breakLine: true } })), {
    x: rx + 0.2, y: 4.42, w: rw - 0.4, h: 2.0, fontFace: SANS, fontSize: 10.5, color: INK2, paraSpaceAfter: 6,
  });

  s.addText("DNA is built to last. RNA is built to be disposable. Every difference above exists for that one reason.", {
    x: 0.6, y: 6.65, w: 8.1, h: 0.6, fontFace: SANS, italic: true, fontSize: 11.5, color: INK3,
  });
  pageNum(s, 4);
}

// ============================================================ SLIDE 5 — REPLICATION & TRANSCRIPTION
{
  const s = p.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "Copying the Code");
  titleBar(s, "Replication & Transcription: Two Ways to Copy");

  const colW = 5.9;
  s.addShape("roundRect", { x: 0.6, y: 1.3, w: colW, h: 2.65, rectRadius: 0.06, fill: { color: V_SOFT }, line: { color: LINE, width: 0.75 } });
  s.addText("DNA → DNA   ·   Replication", { x: 0.8, y: 1.4, w: colW - 0.4, h: 0.35, fontFace: SANS, fontSize: 14, bold: true, color: V });
  s.addText([
    "Semiconservative — each new duplex keeps one parental strand.",
    "DNA polymerase reads 3'→5', builds new strand 5'→3'.",
    "Leading strand: continuous. Lagging strand: short Okazaki fragments, sealed by ligase.",
  ].map((t) => ({ text: t, options: { bullet: { code: "2022" }, breakLine: true } })), {
    x: 0.8, y: 1.85, w: colW - 0.4, h: 2.0, fontFace: SANS, fontSize: 11.5, color: INK2, paraSpaceAfter: 10,
  });

  s.addShape("roundRect", { x: 0.6, y: 4.15, w: colW, h: 2.5, rectRadius: 0.06, fill: { color: E_SOFT }, line: { color: "EAB9CB", width: 0.75 } });
  s.addText("DNA → RNA   ·   Transcription", { x: 0.8, y: 4.25, w: colW - 0.4, h: 0.35, fontFace: SANS, fontSize: 14, bold: true, color: E });
  s.addText([
    "Copies out one gene only — not the whole genome.",
    "RNA polymerase reads the template, builds mRNA 5'→3'.",
    "mRNA transcript (5'…AUG…3') carries the code to the ribosome.",
  ].map((t) => ({ text: t, options: { bullet: { code: "2022" }, breakLine: true } })), {
    x: 0.8, y: 4.7, w: colW - 0.4, h: 1.8, fontFace: SANS, fontSize: 11.5, color: INK2, paraSpaceAfter: 10,
  });

  s.addImage({ path: "assets/replication.png", x: 6.85, y: 1.3, w: 5.9, h: 5.9 * (1108 / 1580) });
  s.addText("Reference: the full replication mechanism (not required to memorize step-by-step today).", {
    x: 6.85, y: 5.55, w: 5.9, h: 0.4, fontFace: SANS, italic: true, fontSize: 9, color: INK3,
  });
  pageNum(s, 5);
}

// ============================================================ SLIDE 6 — CENTRAL DOGMA (CORRECTED)
{
  const s = p.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "Reading the Code");
  titleBar(s, "Codons & the Central Dogma");

  // --- main flow: DNA -> mRNA -> Protein, with tRNA converging into Translation
  const boxY = 1.35, boxH = 0.95, boxW = 2.55;
  const xDNA = 0.6, xArrow1 = xDNA + boxW, xMRNA = 3.85, xArrow2 = xMRNA + boxW, xPROT = 7.1;

  function flowBox(x, label, seq, color, fill) {
    s.addShape("roundRect", { x, y: boxY, w: boxW, h: boxH, rectRadius: 0.07, fill: { color: fill }, line: { color, width: 1.25 } });
    s.addText(label, { x: x + 0.1, y: boxY + 0.08, w: boxW - 0.2, h: 0.35, fontFace: SANS, fontSize: 11.5, bold: true, color: INK2, align: "center" });
    s.addText(seq, { x: x + 0.1, y: boxY + 0.42, w: boxW - 0.2, h: 0.45, fontFace: "Courier New", fontSize: 15, bold: true, color, align: "center" });
  }
  flowBox(xDNA, "DNA (template)", "3'–T A C–5'", V, V_SOFT);
  flowBox(xMRNA, "mRNA (codon)", "5'–A U G–3'", E, E_SOFT);
  flowBox(xPROT, "Protein", "Met (Start)", GOOD, GOOD_SOFT);

  s.addShape("line", { x: xArrow1, y: boxY + boxH / 2, w: xMRNA - xArrow1, h: 0, line: { color: INK3, width: 1.75, endArrowType: "triangle" } });
  s.addText("Transcription", { x: xArrow1, y: boxY - 0.32, w: xMRNA - xArrow1, h: 0.3, fontFace: SANS, fontSize: 10.5, bold: true, color: INK3, align: "center" });

  s.addShape("line", { x: xArrow2, y: boxY + boxH / 2, w: xPROT - xArrow2, h: 0, line: { color: INK3, width: 1.75, endArrowType: "triangle" } });
  s.addText("Translation", { x: xArrow2, y: boxY - 0.32, w: xPROT - xArrow2, h: 0.3, fontFace: SANS, fontSize: 10.5, bold: true, color: INK3, align: "center" });

  // tRNA as a converging INPUT into translation, not a chained node
  const trnaY = 2.75, trnaX = (xArrow2 + xPROT) / 2 - boxW / 2;
  s.addShape("roundRect", { x: trnaX, y: trnaY, w: boxW, h: 0.85, rectRadius: 0.07, fill: { color: "F3EEEA" }, line: { color: "C9791E", width: 1.25 } });
  s.addText("tRNA (anticodon)", { x: trnaX + 0.1, y: trnaY + 0.05, w: boxW - 0.2, h: 0.3, fontFace: SANS, fontSize: 10.5, bold: true, color: INK2, align: "center" });
  s.addText("3'–U A C–5'", { x: trnaX + 0.1, y: trnaY + 0.36, w: boxW - 0.2, h: 0.4, fontFace: "Courier New", fontSize: 13.5, bold: true, color: "C9791E", align: "center" });

  const midX = trnaX + boxW / 2;
  s.addShape("line", { x: midX, y: trnaY, w: 0, h: boxY + boxH - trnaY, line: { color: "C9791E", width: 1.5, endArrowType: "triangle", dashType: "dash" } });
  s.addText("reads the codon, delivers the matching amino acid", {
    x: trnaX + boxW + 0.15, y: trnaY + 0.12, w: 2.55, h: 0.65, fontFace: SANS, italic: true, fontSize: 9, color: INK3, valign: "middle",
  });

  s.addShape("roundRect", { x: 0.6, y: 3.95, w: 5.15, h: 0.78, rectRadius: 0.05, fill: { color: "FBF0DC" }, line: { color: "E8A34D", width: 0.75 } });
  s.addText("Translation runs mRNA → Protein directly. tRNA is a helper that reads the codon and hands over an amino acid — not an intermediate product.", {
    x: 0.75, y: 3.98, w: 4.9, h: 0.72, fontFace: SANS, fontSize: 9, bold: true, color: "8A5A12", valign: "middle",
  });

  // codon degeneracy table
  const tblY = 4.95;
  s.addText("The Code Is Degenerate", { x: 0.6, y: tblY, w: 5.15, h: 0.3, fontFace: SANS, fontSize: 12.5, bold: true, color: V });
  s.addText("61 sense codons specify only 20 amino acids — most amino acids have more than one codon.", {
    x: 0.6, y: tblY + 0.32, w: 5.15, h: 0.4, fontFace: SANS, fontSize: 9.5, color: INK2,
  });
  const rows = [
    ["Amino acid", "Codons (mRNA)"],
    ["Leucine (Leu)", "UUA · UUG · CUU · CUC · CUA · CUG"],
    ["Serine (Ser)", "UCU · UCC · UCA · UCG · AGU · AGC"],
    ["Methionine (Met)", "AUG (also the start codon)"],
    ["Tryptophan (Trp)", "UGG (only one codon)"],
  ];
  s.addTable(rows.map((r, i) => r.map((c) => ({
    text: c,
    options: {
      fontFace: SANS, fontSize: 8.5, color: i === 0 ? WHITE : INK2, bold: i === 0,
      fill: { color: i === 0 ? V : (i % 2 === 0 ? V_SOFT : WHITE) },
      valign: "middle",
    },
  }))), { x: 0.6, y: tblY + 0.78, w: 5.15, h: 1.55, colW: [1.7, 3.45], border: { type: "solid", color: LINE, pt: 0.5 } });

  // wobble callout
  s.addShape("roundRect", { x: 6.1, y: tblY, w: 6.6, h: 2.35, rectRadius: 0.06, fill: { color: E_SOFT }, line: { color: "EAB9CB", width: 0.75 } });
  s.addText("The Wobble Position", { x: 6.3, y: tblY + 0.1, w: 6.2, h: 0.3, fontFace: SANS, fontSize: 12.5, bold: true, color: E });
  s.addText("Strict pairing governs codon positions 1 & 2. Position 3 tolerates a looser match — e.g. a G on the tRNA pairing with U on the mRNA. Result: one tRNA can recognize more than one codon, so fewer than 61 tRNA types are needed.", {
    x: 6.3, y: tblY + 0.42, w: 6.2, h: 0.85, fontFace: SANS, fontSize: 9.5, color: INK2,
  });

  const wx = 6.5, wgap = 0.55;
  ["C", "U", "U"].forEach((L, i) => {
    s.addShape("roundRect", { x: wx + i * wgap, y: tblY + 1.35, w: 0.42, h: 0.38, rectRadius: 0.04, fill: { color: V }, line: { color: V } });
    s.addText(L, { x: wx + i * wgap, y: tblY + 1.35, w: 0.42, h: 0.38, fontFace: "Courier New", fontSize: 12.5, bold: true, color: WHITE, align: "center", valign: "middle" });
  });
  ["G", "A", "G"].forEach((L, i) => {
    s.addShape("roundRect", { x: wx + i * wgap, y: tblY + 1.82, w: 0.42, h: 0.38, rectRadius: 0.04, fill: { color: "C9791E" }, line: { color: "C9791E" } });
    s.addText(L, { x: wx + i * wgap, y: tblY + 1.82, w: 0.42, h: 0.38, fontFace: "Courier New", fontSize: 12.5, bold: true, color: WHITE, align: "center", valign: "middle" });
  });
  s.addText("codon", { x: wx + 3 * wgap + 0.15, y: tblY + 1.35, w: 1.6, h: 0.38, fontFace: SANS, fontSize: 9, color: INK3, valign: "middle" });
  s.addText("anticodon (wobble)", { x: wx + 3 * wgap + 0.15, y: tblY + 1.82, w: 2.0, h: 0.38, fontFace: SANS, fontSize: 9, color: "8A5A12", valign: "middle", bold: true });
}

// ============================================================ SLIDE 7 — PCR
{
  const s = p.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "The Copy-Paste Tool");
  titleBar(s, "PCR: The Polymerase Chain Reaction");

  const steps = [
    ["1", "Denaturation", "~95 °C", "Heat breaks H-bonds; dsDNA separates into two single strands.", V],
    ["2", "Annealing", "50–65 °C", "Short primers bind complementary sequences flanking the target.", E],
    ["3", "Extension", "~72 °C", "Taq polymerase adds dNTPs 5'→3', synthesizing new strands.", GOOD],
  ];
  const cw = 3.9, gap = 0.25;
  steps.forEach((st, i) => {
    const x = 0.6 + i * (cw + gap);
    s.addShape("roundRect", { x, y: 1.35, w: cw, h: 2.15, rectRadius: 0.07, fill: { color: WHITE }, line: { color: st[4], width: 1.25 } });
    s.addShape("ellipse", { x: x + 0.25, y: 1.55, w: 0.5, h: 0.5, fill: { color: st[4] }, line: { color: st[4] } });
    s.addText(st[0], { x: x + 0.25, y: 1.55, w: 0.5, h: 0.5, fontFace: SANS, fontSize: 16, bold: true, color: WHITE, align: "center", valign: "middle" });
    s.addText(st[1], { x: x + 0.25, y: 2.15, w: cw - 0.5, h: 0.4, fontFace: SERIF, fontSize: 16, bold: true, color: INK });
    s.addText(st[2], { x: x + 0.25, y: 2.55, w: cw - 0.5, h: 0.35, fontFace: "Courier New", fontSize: 13, bold: true, color: st[4] });
    s.addText(st[3], { x: x + 0.25, y: 2.95, w: cw - 0.5, h: 0.5, fontFace: SANS, fontSize: 10, color: INK2 });
  });
  s.addText("Repeat 25–35 times — every molecule made becomes a template for the next cycle.", {
    x: 0.6, y: 3.65, w: cw * 3 + gap * 2, h: 0.35, fontFace: SANS, italic: true, fontSize: 11, color: INK3, align: "center",
  });

  // reagents strip
  const reagents = ["Template DNA", "Forward & reverse primers", "Taq DNA polymerase", "dNTPs", "Mg²⁺ buffer"];
  s.addText("What's in the tube", { x: 0.6, y: 4.25, w: 5.6, h: 0.3, fontFace: SANS, fontSize: 12, bold: true, color: V });
  s.addText(reagents.map((r) => ({ text: r, options: { bullet: { code: "2022" }, breakLine: true } })), {
    x: 0.6, y: 4.6, w: 5.6, h: 2.2, fontFace: SANS, fontSize: 11, color: INK2, paraSpaceAfter: 8,
  });

  // exponential callout
  s.addShape("roundRect", { x: 6.6, y: 4.25, w: 6.1, h: 2.55, rectRadius: 0.07, fill: { color: V_DARK } });
  s.addText("Copy number ≈ 2ⁿ", { x: 6.9, y: 4.42, w: 5.5, h: 0.45, fontFace: SANS, fontSize: 16, bold: true, color: WHITE });
  s.addText("n = number of cycles", { x: 6.9, y: 4.85, w: 5.5, h: 0.3, fontFace: SANS, fontSize: 10.5, color: "C7B8E8" });
  s.addText("35", { x: 6.9, y: 5.2, w: 1.6, h: 0.9, fontFace: SERIF, fontSize: 46, bold: true, color: E });
  s.addText("cycles", { x: 6.9, y: 5.95, w: 1.6, h: 0.3, fontFace: SANS, fontSize: 10, color: "C7B8E8" });
  s.addText("≈ 3.4 × 10¹⁰ copies", { x: 8.6, y: 5.25, w: 3.9, h: 0.5, fontFace: SANS, fontSize: 17, bold: true, color: WHITE });
  s.addText("from a single template molecule — enough to detect DNA present only in trace amounts.", {
    x: 8.6, y: 5.7, w: 3.9, h: 0.9, fontFace: SANS, fontSize: 9.5, color: "C7B8E8",
  });
  pageNum(s, 7);
}

// ============================================================ SLIDE 8 — CLOSING / QR
{
  const s = p.addSlide();
  s.background = { color: V_DARK };
  s.addText("Go Deeper: DNA & RNA Right Now", {
    x: 0.8, y: 0.6, w: SW - 1.6, h: 0.9, fontFace: SERIF, fontSize: 32, bold: true, color: WHITE, align: "center",
  });
  s.addText("Scan for 12 current articles on gene editing, RNA medicine, DNA storage, and more", {
    x: 0.8, y: 1.5, w: SW - 1.6, h: 0.5, fontFace: SANS, fontSize: 15, color: "D8CCF0", align: "center",
  });
  s.addImage({ path: "assets/qr.png", x: (SW - 3.4) / 2, y: 2.2, w: 3.4, h: 3.4 });
  s.addText("https://claude.ai/code/artifact/667ab17c-f452-4b89-8df7-2286ee64214f", {
    x: 0.8, y: 5.75, w: SW - 1.6, h: 0.4, fontFace: "Courier New", fontSize: 12, color: "9B8DC4", align: "center",
  });
}

p.writeFile({ fileName: "BB101_T2_DNA_Lecture_v2.pptx" }).then(() => console.log("wrote pptx"));
