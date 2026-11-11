"""Build notes.html — short notes and points to remember for the BB 101 end-sem.  Usage: python3 build_notes.py"""
import os

from common import box_flow_svg, cell_cycle_svg, gprotein_cycle_svg, page, selection_svg

HERE = os.path.dirname(os.path.abspath(__file__))

# Denser type than the question booklet: these are revision notes.
NOTES_CSS = """
.flow{ margin-top:14pt; }
body{ font-size:9.5pt; line-height:1.36; }
table{ font-size:8.7pt; margin:3pt 0 6pt; }
th,td{ padding:2.6pt 4.5pt; }
h3{ font-size:11pt; margin:9pt 0 4pt; }
h4{ margin:6pt 0 2pt; }
ul,ol{ margin:1pt 0 4pt; }
.box{ padding:5pt 8pt; margin:5pt 0 6pt; }
"""


def box(kind, title, inner):
    return f"<div class='box {kind}'><span class='bt'>{title}</span>{inner}</div>"


def sec(num, title, sub):
    return f"<h2>{num} · {title}<span class='sub'>{sub}</span></h2>"


MICRO = ("<div style='display:grid;grid-template-columns:repeat(5,1fr);gap:5pt'>"
         + "".join(f"<div style='text-align:center'><img src='../assets/mitosis-{s}.jpg' style='width:100%;border-radius:3pt'>"
                   f"<div class='sans' style='font-size:8.5pt;font-weight:600;color:#1f4e79'>{n}</div></div>"
                   for s, n in [("prophase", "1 Prophase"), ("prometaphase", "2 Prometaphase"), ("metaphase", "3 Metaphase"),
                                ("anaphase", "4 Anaphase"), ("telophase", "5 Telophase + cytokinesis")])
         + "</div><div class='cap'>Lecture micrographs (Campbell Fig. 12.7): chromosomes blue, microtubules green, actin red.</div>")

COVER = f"""
<section class='cover'>
  <div class='band'>
    <div class='kicker'>BB 101 Biology · End-semester examination</div>
    <h1>Short Notes &amp; Points to Remember</h1>
    <p class='lede'>Everything in Lectures 15–23 on a few pages each: definitions, tables, diagrams, numbers, and the traps examiners like.</p>
  </div>
  <div class='meta'>
    <div><b>Syllabus</b>End-sem lecture slides, Lectures 15–23 (255 slides)</div>
    <div><b>Reference</b>Campbell Biology, 10th ed. — Ch. 11–15, 16.1, 21.2, 22–24</div>
    <div><b>Prepared for</b>Tutorial Batch T1</div>
  </div>
  <h3>Contents</h3>
  <table class='keep'>
    <tr><th class='c'>#</th><th>Topic</th><th>Lecture</th><th>Campbell</th></tr>
    <tr><td class='c'>1</td><td>Heredity and Mendel’s laws</td><td>15–16</td><td>14.1</td></tr>
    <tr><td class='c'>2</td><td>Mendel and the gene idea: probability, dominance, pedigrees</td><td>17</td><td>14.2–14.4</td></tr>
    <tr><td class='c'>3</td><td>Cell cycle, mitosis and meiosis</td><td>18</td><td>12, 13</td></tr>
    <tr><td class='c'>4</td><td>Chromosomal basis of inheritance</td><td>19</td><td>15</td></tr>
    <tr><td class='c'>5</td><td>Cell communication</td><td>20</td><td>11</td></tr>
    <tr><td class='c'>6</td><td>Big data in biology and bioinformatics</td><td>21</td><td>16.1, 21.2 + slides</td></tr>
    <tr><td class='c'>7</td><td>Evolution and natural selection</td><td>22</td><td>22, 23 (opening), 24.1</td></tr>
    <tr><td class='c'>8</td><td>Population genetics and Hardy–Weinberg</td><td>22–23</td><td>23</td></tr>
    <tr><td class='c'>9</td><td>Last-minute revision sheet: numbers, names, formulas, traps</td><td>all</td><td>—</td></tr>
  </table>
  {box('tip', 'How to use these notes', '<p>Read one section, then do the matching section (A–H) of the Practice Questions booklet. '
       'Teal boxes are must-remember facts; red boxes are common mistakes. Section 9 is for the night before the exam.</p>')}
  <div class='foot'>Written from the end-sem lecture slides, with explanations checked against Campbell Biology (10th ed.).</div>
</section>"""

S1 = f"""
<section class='page-break'>
{sec(1, 'Heredity and Mendel’s laws', 'Lectures 15–16 · Campbell 14.1')}
<h3>The road to “DNA is the genetic material”</h3>
<table class='keep'><tr><th>Year</th><th>Who</th><th>What</th></tr>
<tr><td>1866</td><td>Gregor Mendel</td><td>Rules of inheritance from thousands of pea crosses (7 characters, 3 : 1 in F<sub>2</sub>)</td></tr>
<tr><td>1928</td><td>Frederick Griffith</td><td>‘Transforming principle’ — something from dead bacteria changes living ones</td></tr>
<tr><td>1944</td><td>Avery, MacLeod &amp; McCarty</td><td>The transforming principle is DNA</td></tr>
<tr><td>1953</td><td>Watson &amp; Crick</td><td>Double-helix structure of DNA</td></tr></table>
<p>DNA is the genetic material of all known organisms (exception: some viruses use RNA). It is a self-driven programme that drives the development and controls the functioning of the organism.</p>

<h3>Key terms</h3>
<table><tr><th style='width:24%'>Term</th><th>Meaning</th></tr>
<tr><td><b>Character</b></td><td>A heritable feature that varies (flower colour).</td></tr>
<tr><td><b>Trait</b></td><td>One variant of a character (purple, white). Can be qualitative (eye colour) or quantitative (height, blood pressure).</td></tr>
<tr><td><b>Heritable trait</b></td><td>Phenotypic character passed from parents to offspring.</td></tr>
<tr><td><b>Phenotype / genotype</b></td><td>Observable property / genetic make-up. <i>PP</i> and <i>Pp</i>: same phenotype (purple), different genotypes.</td></tr>
<tr><td><b>Genome</b></td><td>An organism’s full hereditary information (its DNA).</td></tr>
<tr><td><b>True-breeding</b></td><td>Self-pollination gives only the same variety (homozygous).</td></tr>
<tr><td><b>Hybridization</b></td><td>Crossing two contrasting true-breeding varieties.</td></tr>
<tr><td><b>P, F<sub>1</sub>, F<sub>2</sub></b></td><td>Parents (true-breeding); hybrid offspring; offspring of F<sub>1</sub> self/cross-pollination. F = filial (child).</td></tr>
<tr><td><b>Gene / allele</b></td><td>Mendel’s heritable ‘unit’ / ‘factor’ / an alternative version of a gene.</td></tr></table>

<div class='two'>
<div>
<h4>Why the garden pea? (model-system criteria)</h4>
<ul><li>Available in many variations</li><li>Short generation time</li><li>Many offspring per mating</li>
<li>Easy cross-pollination — pollen-producing and egg-bearing organs well separated</li>
<li>Characters with distinct ‘either-or’ forms</li></ul>
<h4>The 7 characters (Campbell Table 14.1)</h4>
<p>Flower colour, flower position, seed colour, seed shape, pod shape, pod colour, stem length.</p>
</div>
<div>
<h4>The monohybrid cross</h4>
<table class='keep'><tr><th></th><th class='c'>Sperm <i>P</i> (½)</th><th class='c'>Sperm <i>p</i> (½)</th></tr>
<tr><th class='c'>Egg <i>P</i> (½)</th><td class='c'><i>PP</i> purple</td><td class='c'><i>Pp</i> purple</td></tr>
<tr><th class='c'>Egg <i>p</i> (½)</th><td class='c'><i>Pp</i> purple</td><td class='c'><i>pp</i> white</td></tr></table>
<p class='small'>P: purple <i>PP</i> × white <i>pp</i> → F<sub>1</sub>: all purple <i>Pp</i> (no blending) → F<sub>2</sub>: 705 purple : 224 white ≈ <b>3 : 1</b>; genotypes <b>1 : 2 : 1</b>.</p>
</div></div>

<h3>Mendel’s two laws</h3>
<table class='keep'><tr><th style='width:20%'>Law</th><th>Statement</th><th style='width:27%'>Physical basis (meiosis)</th></tr>
<tr><td><b>Segregation</b></td><td>The two alleles of <b>one gene</b> separate during gamete formation, so each gamete carries only one of them (½ <i>P</i>, ½ <i>p</i>).</td><td>Homologous chromosomes separate in anaphase I.</td></tr>
<tr><td><b>Independent assortment</b></td><td>Alleles of <b>different genes</b> sort into gametes independently — provided the genes are on different chromosomes or far apart on the same one. Dihybrid F<sub>2</sub>: <b>9 : 3 : 3 : 1</b>.</td><td>Each homologous pair lines up at metaphase I independently of the other pairs.</td></tr></table>

{box('remember', 'Remember', '<ul><li>The white factor was hidden in F<sub>1</sub>, not destroyed — it came back unchanged in F<sub>2</sub>. That disproves <b>blending</b> and supports the <b>particulate</b> hypothesis (discrete units).</li>'
 '<li>Mendel followed traits to at least F<sub>2</sub> and counted thousands of plants — quantitative analysis is what revealed the pattern.</li>'
 '<li>Independent assortment is why siblings (except identical twins) are never genetically the same.</li></ul>')}
{box('trap', 'Trap', '<p>Segregation = <b>one</b> gene, two alleles. Independent assortment = <b>two or more</b> genes. A ‘trait’ is not the same as a ‘character’.</p>')}
</section>"""

S2 = f"""
<section class='flow'>
{sec(2, 'Mendel and the gene idea', 'Lecture 17 · Campbell 14.1–14.4')}
<div class='two'><div>
<h3>Vocabulary</h3>
<ul><li><b>Homozygous</b>: two identical alleles (<i>HH, zz, TT, aa</i>) — true-breeding.</li>
<li><b>Heterozygous</b>: two different alleles (<i>Jj, Bb, Cc</i>) — hybrid.</li>
<li><b>Locus</b>: a gene’s position on a chromosome; alleles sit at the same locus on homologous chromosomes.</li>
<li><b>Punnett square</b>: all combinations of sperm and egg; capital = dominant, lowercase = recessive.</li>
<li><b>Testcross</b> (Campbell): unknown dominant × homozygous recessive. All dominant → <i>PP</i>; 1 : 1 → <i>Pp</i>.</li></ul>
</div><div>
<h3>Why is purple dominant?</h3>
<p>The <i>P</i> allele codes for an <b>active enzyme</b> that makes purple pigment; a change in the DNA sequence of <i>p</i> gives an <b>inactive enzyme</b>.
In <i>Pp</i>, <b>one functional allele suffices</b> to make enough pigment. (The protein need not be an enzyme.)</p>
</div></div>

<h3>Probability rules</h3>
<table class='keep'><tr><th style='width:20%'>Rule</th><th>Use it when…</th><th style='width:34%'>Example (<i>Rr</i> × <i>Rr</i>)</th></tr>
<tr><td><b>Multiplication</b></td><td>Two or more <b>independent</b> events must happen together (“and”).</td><td>P(<i>rr</i>) = ½ × ½ = ¼</td></tr>
<tr><td><b>Addition</b></td><td>An outcome can happen in two or more <b>mutually exclusive</b> ways (“or”).</td><td>P(heterozygote) = ¼ + ¼ = ½</td></tr></table>
{box('tip', 'Method for multi-gene crosses', '<p>Split the cross into one monohybrid cross per gene, find each probability, then multiply. '
 'Slide problem: <i>PpYyRr</i> × <i>Ppyyrr</i>, P(recessive for at least two characters): '
 '<i>ppyyRr</i> 1/16 + <i>ppYyrr</i> 1/16 + <i>Ppyyrr</i> 2/16 + <i>PPyyrr</i> 1/16 + <i>ppyyrr</i> 1/16 = <b>6/16 = 3/8</b>.</p>'
 '<p>Number of gamete types = 2<sup><i>n</i></sup> (<i>n</i> = number of heterozygous genes): <i>AaBbCcDd</i> → 16.</p>')}

<h3>Degrees of dominance and beyond</h3>
<table><tr><th style='width:22%'>Pattern</th><th>What happens</th><th style='width:30%'>Example</th></tr>
<tr><td><b>Complete dominance</b></td><td>Heterozygote looks like the dominant homozygote.</td><td>Purple vs white pea</td></tr>
<tr><td><b>Incomplete dominance</b></td><td>F<sub>1</sub> is intermediate between the parents; F<sub>2</sub> phenotype ratio = genotype ratio 1 : 2 : 1.</td><td>Snapdragons: red × white → pink</td></tr>
<tr><td><b>Codominance</b></td><td>Both alleles affect the phenotype in separate, distinguishable ways.</td><td><i>I<sup>A</sup>I<sup>B</sup></i> → blood group AB</td></tr>
<tr><td><b>Multiple alleles</b></td><td>More than two alleles of a gene in the population.</td><td>ABO: <i>I<sup>A</sup></i>, <i>I<sup>B</sup></i>, <i>i</i></td></tr>
<tr><td><b>Pleiotropy</b></td><td>One gene, many phenotypic effects.</td><td>Sickle-cell allele (Campbell)</td></tr></table>
<p class='small'>Dominance depends on the level at which you look at the phenotype, and says nothing about how common an allele is (polydactyly is dominant but rare).</p>

<div class='two'><div>
<h3>ABO blood groups</h3>
<table class='keep'><tr><th>Genotype</th><th class='c'>Group</th><th>Carbohydrate on RBC</th></tr>
<tr><td><i>I<sup>A</sup>I<sup>A</sup></i> or <i>I<sup>A</sup>i</i></td><td class='c'>A</td><td>A</td></tr>
<tr><td><i>I<sup>B</sup>I<sup>B</sup></i> or <i>I<sup>B</sup>i</i></td><td class='c'>B</td><td>B</td></tr>
<tr><td><i>I<sup>A</sup>I<sup>B</sup></i></td><td class='c'>AB</td><td>both</td></tr>
<tr><td><i>ii</i></td><td class='c'>O</td><td>neither</td></tr></table>
<p class='small'>3 alleles → <b>6 genotypes, 4 phenotypes</b>. <i>I<sup>A</sup></i> and <i>I<sup>B</sup></i> are codominant; both are dominant over <i>i</i>.</p>
</div><div>
<h3>Pedigrees — reading rules</h3>
<ul><li>□ male, ○ female, filled = affected; horizontal line = mating.</li>
<li>Two <b>unaffected</b> parents with an <b>affected</b> child → <b>recessive</b> (both parents carriers, <i>Aa</i> × <i>Aa</i>, risk ¼).</li>
<li>Two <b>affected</b> parents with an <b>unaffected</b> child → <b>dominant</b>.</li>
<li>Lecture examples: widow’s peak = dominant; attached earlobe = recessive; albinism = recessive.</li>
<li>Two carriers: P(affected) = ¼, but P(a <b>normal</b> child is a carrier) = <b>2/3</b>.</li>
<li>Humans: long generations, few offspring, no breeding experiments → we use pedigrees.</li></ul>
</div></div>
</section>"""

S3 = f"""
<section class='flow'>
{sec(3, 'Cell cycle, mitosis and meiosis', 'Lecture 18 · Campbell Ch. 12 and 13')}
<div class='two'><div>
<h3>Genetic material in the cell</h3>
<ul><li><b>Genome</b>: one DNA molecule (prokaryotes) or several (eukaryotes).</li>
<li><b>Chromatin</b>: DNA + protein; condenses into visible chromosomes during division.</li>
<li><b>Somatic cells</b>: two sets of chromosomes (2<i>n</i> = 46 in humans; 23 pairs = 22 autosome pairs + XX/XY).</li>
<li><b>Gametes</b>: one set (<i>n</i> = 23).</li>
<li>After S phase each chromosome = two <b>sister chromatids</b> joined at the <b>centromere</b> (the narrow ‘waist’). Once separated, each chromatid is called a chromosome.</li>
<li>Cell division lets cells proliferate — for growth, repair and reproduction.</li></ul>
</div><div class='fig'>{cell_cycle_svg()}</div></div>

<h3>Mitosis — the five stages</h3>
<div class='fig'>{MICRO}</div>
<table><tr><th style='width:16%'>Stage</th><th>What happens (Campbell 12.2)</th></tr>
<tr><td><b>Prophase</b></td><td>Chromatin condenses into chromosomes; nucleoli disappear; mitotic spindle begins to form; centrosomes move apart.</td></tr>
<tr><td><b>Prometaphase</b></td><td><b>Nuclear envelope fragments</b>; kinetochores form at centromeres; some spindle microtubules attach to kinetochores and start moving chromosomes.</td></tr>
<tr><td><b>Metaphase</b></td><td>Chromosomes line up at the <b>metaphase plate</b> — an imaginary plane midway between the two poles.</td></tr>
<tr><td><b>Anaphase</b></td><td>Sister chromatids separate and move to opposite poles; kinetochore microtubules <b>shorten by depolymerizing at their kinetochore ends</b>; the cell elongates.</td></tr>
<tr><td><b>Telophase</b></td><td>Two daughter nuclei form; nuclear envelopes and nucleoli re-form; chromosomes decondense.</td></tr>
<tr><td><b>Cytokinesis</b></td><td>Animal cells: <b>cleavage furrow</b> (contractile ring of actin + myosin). Plant cells: <b>cell plate</b> (vesicles fuse in the middle and build a new wall).</td></tr></table>
<p class='small'><b>Spindle</b> = centrosomes + spindle microtubules + asters (radial arrays of short microtubules). The centrosome duplicates in interphase; the two centrosomes move to opposite ends during prophase and prometaphase. <b>Kinetochores</b> = protein complexes at the centromere.</p>
<h3>Meiosis — one replication, two divisions</h3>
<table class='keep'><tr><th style='width:16%'></th><th>Meiosis I (reduction division)</th><th>Meiosis II (like mitosis)</th></tr>
<tr><td><b>Prophase</b></td><td><b>Synapsis</b> of homologues; <b>crossing over</b> between non-sister chromatids (chiasmata)</td><td>Spindle forms again</td></tr>
<tr><td><b>Metaphase</b></td><td><b>Pairs</b> of homologues line up at the plate</td><td>Single chromosomes line up</td></tr>
<tr><td><b>Anaphase</b></td><td><b>Homologues</b> separate; sister chromatids stay together</td><td><b>Sister chromatids</b> separate</td></tr>
<tr><td><b>Result</b></td><td>2 haploid cells; each chromosome still has two chromatids</td><td>4 haploid cells with unduplicated chromosomes</td></tr></table>

<h3>Mitosis vs meiosis</h3>
<table class='keep'><tr><th style='width:24%'>Property</th><th>Mitosis</th><th>Meiosis</th></tr>
<tr><td>DNA replication</td><td>Once, in interphase before mitosis</td><td>Once, in interphase before meiosis I (none between I and II)</td></tr>
<tr><td>Number of divisions</td><td>One</td><td>Two</td></tr>
<tr><td>Synapsis &amp; crossing over</td><td>Do not occur</td><td>Occur in prophase I</td></tr>
<tr><td>Daughter cells</td><td>Two diploid (2<i>n</i>), identical to the parent</td><td>Four haploid (<i>n</i>), different from the parent and from each other</td></tr>
<tr><td>Role</td><td>Growth, repair, asexual reproduction</td><td>Gametes; genetic diversity in sexual reproduction</td></tr></table>

<div class='two'><div>
<h3>Counting chromosomes and DNA</h3>
<table class='keep'><tr><th>Stage (human)</th><th class='c'>Chromosomes</th><th class='c'>Chromatids</th><th class='c'>DNA</th></tr>
<tr><td>G<sub>1</sub></td><td class='c'>46</td><td class='c'>46</td><td class='c'><i>x</i></td></tr>
<tr><td>G<sub>2</sub> / metaphase</td><td class='c'>46</td><td class='c'>92</td><td class='c'>2<i>x</i></td></tr>
<tr><td>After mitosis (each cell)</td><td class='c'>46</td><td class='c'>46</td><td class='c'><i>x</i></td></tr>
<tr><td>After meiosis I (each cell)</td><td class='c'>23</td><td class='c'>46</td><td class='c'><i>x</i></td></tr>
<tr><td>Gamete (after meiosis II)</td><td class='c'>23</td><td class='c'>23</td><td class='c'><i>x</i>/2</td></tr></table>
<p class='small'>Rule: count chromosomes by counting <b>centromeres</b>.</p>
</div><div>
<h3>Why meiosis matters — sources of variation</h3>
<ul><li><b>Independent assortment</b>: 2<sup><i>n</i></sup> combinations; humans 2<sup>23</sup> ≈ <b>8.4 million</b> per person.</li>
<li><b>Crossing over</b>: recombinant chromosomes with new allele combinations.</li>
<li><b>Random fertilization</b>: 8.4 million × 8.4 million ≈ <b>70 trillion</b> zygote combinations.</li>
<li>Fertilization restores 2<i>n</i>: the zygote carries a maternal and a paternal set.</li></ul>
</div></div>
{box('trap', 'Traps', '<ul><li>The nuclear envelope breaks up in <b>prometaphase</b>, not prophase.</li>'
 '<li>Mitosis divides the <b>nucleus</b>; cytokinesis divides the cytoplasm.</li>'
 '<li>Homologous chromosomes (one from each parent, same genes, maybe different alleles) ≠ sister chromatids (identical copies joined at the centromere).</li>'
 '<li>Anaphase I separates homologues; anaphase II (and mitotic anaphase) separates sister chromatids.</li></ul>')}
</section>"""

S4 = f"""
<section class='flow'>
{sec(4, 'Chromosomal basis of inheritance', 'Lecture 19 · Campbell Ch. 15')}
<p><b>Chromosome theory of inheritance:</b> Mendelian genes have specific loci on chromosomes, and it is the chromosomes that undergo segregation and independent assortment.
Genes can be seen on isolated chromosomes by tagging them with a fluorescent dye.</p>
<h3>Morgan’s fruit flies (<i>Drosophila melanogaster</i>)</h3>
<table class='keep'><tr><th style='width:22%'>Cross</th><th>Result</th></tr>
<tr><td>P</td><td>Red-eyed (wild-type, <i>w</i><sup>+</sup>) female × white-eyed (mutant, <i>w</i>) male</td></tr>
<tr><td>F<sub>1</sub></td><td>All red-eyed → white is recessive</td></tr>
<tr><td>F<sub>2</sub></td><td>3 red : 1 white, but <b>all white-eyed flies were male</b></td></tr>
<tr><td>Conclusion</td><td>The eye-colour gene is on the <b>X chromosome</b>, with no corresponding locus on the Y.</td></tr></table>

<div class='two'><div>
<h3>Sex chromosomes</h3>
<ul><li>Mammals: larger X, smaller Y. Females XX, males XY.</li>
<li>Only the ends of the Y have regions homologous with the X.</li>
<li><b>SRY</b> (Sex-determining Region of Y): its protein triggers male anatomical features (testes).</li>
<li>Every ovum carries X; sperm are 50% X, 50% Y.</li>
<li>The X carries many genes unrelated to sex; the Y mainly codes for sex determination. Other animals use other systems.</li></ul>
</div><div>
<h3>X-linked recessive inheritance</h3>
<ul><li><b>Sex-linked gene</b>: on a sex chromosome (mostly X-linked; few Y-linked).</li>
<li>Female affected only if homozygous (<i>X<sup>n</sup>X<sup>n</sup></i>); male affected with one copy — he is <b>hemizygous</b>.</li>
<li>So X-linked recessive disorders are much more common in males.</li>
<li>Examples: <b>colour blindness</b> (mostly X-linked), <b>Duchenne muscular dystrophy</b>, <b>haemophilia</b>.</li></ul>
</div></div>
<table class='keep'><tr><th style='width:30%'>Cross</th><th>Daughters</th><th>Sons</th></tr>
<tr><td>Colour-blind father × normal (homozygous) mother<br><i>X<sup>n</sup>Y</i> × <i>X<sup>N</sup>X<sup>N</sup></i></td><td>All carriers, normal vision</td><td>All normal — father gives them his Y</td></tr>
<tr><td>Carrier mother × normal father<br><i>X<sup>N</sup>X<sup>n</sup></i> × <i>X<sup>N</sup>Y</i></td><td>½ carriers, ½ normal</td><td>½ affected, ½ normal</td></tr>
<tr><td>Carrier mother × colour-blind father<br><i>X<sup>N</sup>X<sup>n</sup></i> × <i>X<sup>n</sup>Y</i></td><td>½ affected, ½ carriers</td><td>½ affected, ½ normal (free of the allele)</td></tr></table>

<h3>Errors in chromosome number</h3>
<div class='two'><div>
<ul><li><b>Nondisjunction</b>: homologues (meiosis I) or sister chromatids (meiosis II) fail to separate.</li>
<li>In meiosis I → gametes <i>n</i>+1, <i>n</i>+1, <i>n</i>−1, <i>n</i>−1 (all abnormal).</li>
<li>In meiosis II → <i>n</i>+1, <i>n</i>−1, <i>n</i>, <i>n</i>.</li>
<li><b>Aneuploidy</b>: abnormal number of one chromosome. Trisomic = 2<i>n</i>+1; monosomic = 2<i>n</i>−1.</li>
<li><b>Polyploidy</b>: more than two complete sets (triploid 3<i>n</i>, tetraploid 4<i>n</i>). Common in plants, rare in animals; polyploids look more normal than aneuploids.</li></ul>
</div><div>
<table class='keep'><tr><th>Condition</th><th>Karyotype</th><th>Note</th></tr>
<tr><td>Down syndrome</td><td>Trisomy 21</td><td>Frequency rises with mother’s age</td></tr>
<tr><td>Klinefelter</td><td>XXY</td><td>Male</td></tr>
<tr><td>Turner</td><td>X0</td><td>Female, sterile; only known viable human monosomy</td></tr></table>
</div></div>
{box('remember', 'Remember', '<p>A father passes his X to <b>every daughter</b> and his Y to <b>every son</b>. So a son’s X-linked trait always comes from his mother.</p>')}
</section>"""

S5 = f"""
<section class='flow'>
{sec(5, 'Cell communication', 'Lecture 20 · Campbell Ch. 11')}
<p><b>Why it matters:</b> fight-or-flight. Seeing a predator → adrenal glands secrete <b>adrenaline</b> (epinephrine) → muscles work harder, heart beats faster, breathing speeds up. Cells must communicate and coordinate.</p>
<div class='two'><div>
<h3>Signalling is ancient and universal</h3>
<ul><li><i>Myxococcus xanthus</i> (soil bacterium): starving cells send a chemical signal → aggregate → <b>fruiting bodies</b> with spores.</li>
<li><b>Quorum sensing</b>: bacteria sense local population density from the concentration of signalling molecules.</li>
<li><b>Yeast mating</b> (<i>Saccharomyces cerevisiae</i>): type a secretes <b>a factor</b> → binds receptors on α cells; α secretes α factor → receptors on a cells → cells fuse → <b>a/α diploid</b> (can do mitosis or meiosis).</li>
<li>Mechanisms are evolutionarily conserved — the same ones recur from microbes to humans.</li></ul>
</div><div>
<h3>Local vs long-distance signalling</h3>
<table class='keep'><tr><th>Type</th><th>How</th></tr>
<tr><td>Cell junctions</td><td>Direct cytoplasm-to-cytoplasm: <b>gap junctions</b> (animals), <b>plasmodesmata</b> (plants)</td></tr>
<tr><td>Cell–cell recognition</td><td>Membrane-bound surface molecules; embryonic development, immune response</td></tr>
<tr><td>Paracrine</td><td>Local regulators (e.g. <b>growth factors</b>) act on nearby cells</td></tr>
<tr><td>Synaptic</td><td>Electrical signal → <b>neurotransmitter</b> across synapse → electrical signal</td></tr>
<tr><td>Endocrine (long-distance)</td><td><b>Hormones</b> travel in blood; act only on cells with receptors</td></tr></table>
</div></div>

<h3>Three stages: reception → transduction → response</h3>
<div class='fig'>{box_flow_svg([('Reception', 'signal binds receptor'), ('Transduction', 'relay molecules, cascade'), ('Response', 'enzyme · genes · cytoskeleton')],
 width=640, note='Doorbell analogy: knock received (discriminator) → message carried inside (transducer) → action triggered (amplifier)')}</div>
<p><b>Transduce</b> = to convert energy or a message into another form. Binding changes the receptor’s <b>shape</b>; the shape change is passed on, often through several relay molecules.
Responses: (1) catalysis by an enzyme, (2) activation of specific genes, (3) rearrangement of the cytoskeleton.</p>

<div class='two'><div>
<h3>G proteins — molecular switches</h3>
<div class='fig'>{gprotein_cycle_svg()}</div>
<ul class='small'><li>Large, ubiquitous family; ATP = energy currency, GTP = used in signal transduction.</li>
<li>Built-in GTPase = built-in control: the response is <b>transient</b>.</li>
<li>Nobel 1994: <b>Alfred Gilman &amp; Martin Rodbell</b> — discovery of G proteins.</li></ul>
</div><div>
<h3>GPCRs — G protein-coupled receptors</h3>
<ul><li><b>Seven transmembrane domains</b>; extremely widespread (development, vision, taste, smell…).</li>
<li>~<b>60% of all medicines</b> target GPCRs (β-blockers, albuterol, antipsychotics…).</li>
<li>Involved in cholera, pertussis, botulism. Cholera toxin locks a G protein ON → cAMP stays high → salt and water secretion (Campbell 11.3).</li></ul>
<h4>Activation steps</h4>
<ol class='small'><li>Ligand binds the GPCR outside the cell.</li><li>Receptor changes shape.</li><li>Inactive G protein (GDP) binds inside.</li>
<li>GDP swapped for GTP → G protein active, leaves the receptor, activates an enzyme.</li><li>GTP hydrolysed → G protein off; ligand binding is reversible.</li></ol>
</div></div>
<h3>The adrenaline → cAMP pathway (Sutherland, Nobel 1971)</h3>
<div class='fig'>{box_flow_svg([('Adrenaline', '1st messenger'), ('GPCR', 'reception'), ('G protein', 'GDP → GTP'), ('Adenylyl cyclase', 'ATP → cAMP'), ('cAMP', '2nd messenger'), ('PKA', 'protein kinase A'), ('Response', 'glycogen breakdown')],
 width=900, h=60, note='Phosphodiesterase switches the signal off: cAMP → AMP')}</div>
<div class='two'><div>
<h4>Amplification (Campbell Fig. 11.16)</h4>
<table class='keep'><tr><th>Step</th><th class='c'>Molecules</th></tr>
<tr><td>Adrenaline bound to GPCR (reception)</td><td class='c'>1</td></tr>
<tr><td>Active G proteins</td><td class='c'>10<sup>2</sup></td></tr>
<tr><td>Active adenylyl cyclase</td><td class='c'>10<sup>2</sup></td></tr>
<tr><td>Cyclic AMP</td><td class='c'>10<sup>4</sup></td></tr>
<tr><td>Active protein kinase A</td><td class='c'>10<sup>4</sup></td></tr>
<tr><td>Active phosphorylase kinase</td><td class='c'>10<sup>5</sup></td></tr>
<tr><td>Active glycogen phosphorylase</td><td class='c'>10<sup>6</sup></td></tr>
<tr><td>Glucose 1-phosphate released (response)</td><td class='c'>10<sup>8</sup></td></tr></table>
</div><div>
{box('remember', 'Advantage of a cascade (slide: “What is the advantage?”)',
 '<ul><li><b>Amplification</b> — one hormone molecule → ~10<sup>8</sup> product molecules.</li>'
 '<li><b>Regulation</b> — many points where the signal can be tuned or stopped.</li>'
 '<li><b>Coordination / branching</b> — one signal can trigger several responses.</li></ul>')}
{box('trap', 'Traps', '<ul><li>G protein ON = <b>GTP</b>; OFF = GDP.</li><li><b>Adenylyl cyclase</b> makes cAMP from ATP; <b>phosphodiesterase</b> destroys it (→ AMP).</li>'
 '<li>Adrenaline never enters the cell — it is the <b>first</b> messenger; cAMP is the second.</li></ul>')}
</div></div>
<p class='small muted'>Engineering link from the lecture: signalling is a feedback-and-control system (Systems &amp; Control Engineering, IIT Bombay) — sensor (receptor), transducer, amplifier, actuator, and a built-in switch-off.</p>
</section>"""

S6 = f"""
<section class='flow'>
{sec(6, 'Big data in biology and bioinformatics', 'Lecture 21 · slides; Campbell 16.1, 21.2')}
<div class='two'><div>
<h3>-ome and -omics</h3>
<table class='keep'><tr><th>Suffix</th><th>Meaning</th></tr><tr><td>-ome</td><td>The complete set</td></tr><tr><td>-omics</td><td>The study of an -ome</td></tr></table>
<table class='keep'><tr><th>-ome</th><th>Complete set of…</th></tr>
<tr><td>Genome</td><td>DNA (hereditary information)</td></tr><tr><td>Transcriptome</td><td>RNA transcripts</td></tr>
<tr><td>Proteome</td><td>Proteins</td></tr><tr><td>Metabolome</td><td>Small-molecule metabolites</td></tr>
<tr><td>Lipidome / Glycome</td><td>Lipids / sugars (glycans)</td></tr><tr><td>Epigenome</td><td>Epigenetic marks</td></tr>
<tr><td>Microbiome</td><td>Microbial community and its genes</td></tr></table>
<p class='small'>-Omics are <b>complementary</b> to one-protein-at-a-time studies: different information, different questions.</p>
</div><div>
<h3>Why ‘big data’?</h3>
<ul><li>High-throughput -omics; data generation has become <b>affordable</b>.</li>
<li>Advances in many fields: chemistry (ddNTPs, dyes), physics (optics), engineering (automation), computer science (algorithms).</li>
<li>Genomics (PLoS Biol 2015): ~<b>1 zetta-base</b> acquired per year, <b>2–40 exabytes</b> of storage — compared with astronomy, Twitter, YouTube.</li>
<li>Data types: images/video, text, numbers, audio (even plants ‘cry’ when stressed).</li>
<li>Same-day whole-genome sequencing is now being tried in critical care (NEJM, 2025).</li></ul>
<table class='keep'><tr><th>Prefix</th><th class='c'>Power</th><th>Prefix</th><th class='c'>Power</th></tr>
<tr><td>kilo</td><td class='c'>10<sup>3</sup></td><td>peta</td><td class='c'>10<sup>15</sup></td></tr>
<tr><td>mega</td><td class='c'>10<sup>6</sup></td><td>exa</td><td class='c'>10<sup>18</sup></td></tr>
<tr><td>giga</td><td class='c'>10<sup>9</sup></td><td>zetta</td><td class='c'>10<sup>21</sup></td></tr>
<tr><td>tera</td><td class='c'>10<sup>12</sup></td><td></td><td></td></tr></table>
</div></div>

<h3>DNA double helix: A, B and Z forms</h3>
<table class='keep'><tr><th>Parameter</th><th class='c'>A-DNA</th><th class='c'>B-DNA (common)</th><th class='c'>Z-DNA</th></tr>
<tr><td>Handedness</td><td class='c'>right</td><td class='c'>right</td><td class='c'><b>left</b></td></tr>
<tr><td>Base pairs per turn</td><td class='c'>11</td><td class='c'><b>10</b></td><td class='c'>12</td></tr>
<tr><td>Rotation per base pair</td><td class='c'>33°</td><td class='c'>36°</td><td class='c'>−30°</td></tr>
<tr><td>Rise per base pair</td><td class='c'>2.55 Å</td><td class='c'><b>3.4 Å</b></td><td class='c'>3.7 Å</td></tr>
<tr><td>Helix diameter</td><td class='c'>23 Å</td><td class='c'><b>20 Å</b></td><td class='c'>18 Å</td></tr></table>
<p class='small'>B-DNA: one turn = 10 × 3.4 Å = 3.4 nm; width 2 nm (Campbell 16.1). Human haploid genome ≈ 3 × 10<sup>9</sup> bp × 0.34 nm ≈ 1 m; a diploid cell holds ≈ 2 m of DNA.</p>

<div class='two'><div>
<h3>Bioinformatics</h3>
<ul><li><b>Broad definition</b>: analyse biological data to extract patterns and generate hypotheses (blind men and the elephant: each discipline sees only a part).</li>
<li><b>Beginning (~1960)</b>: Margaret Dayhoff, Richard Eck, Robert Ledley — computer-aided analysis of protein sequences → <b>Protein Information Resource (PIR)</b>.</li>
<li><b>Higgs &amp; Attwood</b>: (1) computational methods for studying the structure, function and evolution of genes, proteins and genomes; (2) methods to manage and analyse information from genomics and high-throughput experiments.</li>
<li><b>Goals</b>: predict biological processes in health and disease; integrate gene/protein information; build and improve tools; better data management, search and retrieval. Success ultimately depends on our knowledge of biology.</li></ul>
</div><div>
<h3>Three fields meet</h3>
<table class='keep'><tr><th>Field</th><th>Contributes</th></tr>
<tr><td>Statistics</td><td>Data analysis, choice of metrics, pattern extraction, validity of inferences</td></tr>
<tr><td>Computer science</td><td>Algorithms; storage and retrieval (query optimisation, transmission, archiving)</td></tr>
<tr><td>Biology (domain knowledge)</td><td>Interpretation, hypothesis testing, context for data generation; the why, how and what; ground-truth data</td></tr></table>
<h4>Why compare sequences?</h4>
<ul class='small'><li>Infer function from a better-characterised sequence</li><li>Find evolutionary relationships</li>
<li>Find similar regions (catalytic or binding sites)</li></ul>
<h4>Applications</h4>
<ul class='small'><li>Database similarity search; structure prediction; annotation</li><li>Assembling reads into genomes</li>
<li>Mapping reads to a reference (‘resequencing’): SNPs, indels</li><li>ChIP-Seq: transcription-factor binding sites</li></ul>
</div></div>

<div class='two'><div>
<h3>AI/ML: the black box</h3>
<p>Big data → AI/ML algorithm → prediction. A <b>black box</b> is a system whose internal workings are hidden. Biologists ask: <i>why</i> this prediction, and what is the underlying biological pattern?</p>
<ul><li><b>Explainable methods</b>: post hoc understanding of what a trained model has learnt.</li>
<li><b>Interpretable models</b>: intelligible by design (parameters and architecture are understandable).</li></ul>
</div><div>
<h3>Protein structure</h3>
<ul><li>Atomic detail: <b>X-ray crystallography</b>, <b>NMR</b>, <b>electron microscopy</b> (~1 Å upward). AFM covers nm-scale; <b>light microscopy</b> works at cell scale and cannot see atoms.</li>
<li><b>AlphaFold</b>: amino-acid sequence + evolutionary history + known 3D structures → deep neural networks → atomic-level 3D structure; very high, independently verified accuracy; huge savings in time, people and cost.</li>
<li><b>Nobel Chemistry 2024</b>: David Baker, Demis Hassabis, John Jumper.</li></ul>
</div></div>
</section>"""

S7 = f"""
<section class='flow'>
{sec(7, 'Evolution and natural selection', 'Lecture 22 · Campbell Ch. 22, 23 (opening), 24.1')}
<p><b>Evolution</b>: the process of change that has transformed life on Earth from its early beginnings to its present diversity. It underpins work on virus evolution, cancer progression and drug resistance.</p>
<div class='two'><div>
<h3>Darwin</h3>
<ul><li>Before Darwin: species were seen as created by God and unchanging.</li>
<li>Voyage on <b>HMS Beagle</b>; specimens from all over the world, especially islands (isolated populations) — the <b>Galápagos</b> (finches, tortoises, iguanas).</li>
<li><i>On the Origin of Species by Means of Natural Selection</i>, <b>1859</b>.</li>
<li>Three observations: the <b>unity</b> of life, the <b>diversity</b> of life, and the <b>match</b> between organisms and their environments.</li>
<li>Today’s organisms descend from ancestral species (descent with modification); the mechanism is <b>natural selection</b>.</li></ul>
</div><div>
<h3>Biological species concept</h3>
<p>A group of populations whose members can <b>interbreed in nature</b> and produce <b>viable, fertile offspring</b> — but not with members of other such groups.</p>
<ul class='small'><li>Male donkey × female horse = <b>mule</b>; female donkey × male horse = <b>hinny</b>. Both sterile → separate species.</li>
<li>Organisms that only divide to multiply (asexual) are excluded.</li></ul>
<h3>Galápagos finches</h3>
<table class='keep'><tr><th>Finch</th><th>Beak</th><th>Food</th></tr>
<tr><td>Cactus ground finch</td><td>Long, sharp</td><td>Cactus flowers, pulp</td></tr>
<tr><td>Green warbler finch</td><td>Narrow, pointed</td><td>Insects</td></tr>
<tr><td>Large ground finch</td><td>Large, short</td><td>Seeds from the ground</td></tr></table>
</div></div>
<p><b>Adaptation</b>: inherited characteristics that enhance survival and reproduction in specific environments.</p>

<h3>Darwin’s observations and inferences (Concept 22.2)</h3>
<table class='keep'><tr><th style='width:50%'>Observations</th><th>Inferences</th></tr>
<tr><td>#1 Members of a population vary in their inherited traits (e.g. ladybird beetle colour/camouflage).</td><td>#1 Individuals whose traits give a higher chance of surviving and reproducing leave more offspring.</td></tr>
<tr><td>#2 All species produce more offspring than the environment can support; many fail to survive (puffball spore cloud). Malthus: populations grow exponentially, food linearly.</td><td>#2 This unequal ability to survive and reproduce leads to the accumulation of favourable traits in the population over generations.</td></tr></table>
<p class='small'>The four components: <b>variation</b>, <b>inheritance</b>, <b>high rate of population growth</b>, <b>differential survival and reproduction</b>. Source of variation: DNA polymerase errs ~1 in 10<sup>4</sup>–10<sup>5</sup> nucleotides; 10<sup>5</sup>–10<sup>6</sup> errors for a diploid mammalian cell; most are repaired, some remain.</p>

<div class='two'><div>
<h3>Evolution observed: the medium ground finch</h3>
<ul><li>Daphne Major, Galápagos; drought of 1977.</li>
<li>Small, soft seeds scarce; large, hard seeds plentiful.</li>
<li>~1200 birds → ~180 survived (deep-beaked birds could crack hard seeds).</li>
<li>Average beak depth rose in the next generation (≈ 9 → ≈ 9.7 mm on the slide’s graph).</li>
<li><b>Individual finches did NOT evolve</b> — no beak grew. The <b>proportion</b> of large-beaked birds rose: the population evolved.</li></ul>
</div><div>
<h3>Evolution observed: MRSA</h3>
<ul><li><i>Staphylococcus aureus</i>: penicillin resistance 1945; methicillin resistance 1961 — each about two years after wide use.</li>
<li>Methicillin inhibits a protein bacteria use to build cell walls; MRSA uses a different protein, survives and out-reproduces the others.</li>
<li>The drug does not cause the mutation — it selects for it. (Also: Harvard’s ‘mega-plate’ Petri dish experiment.)</li></ul>
</div></div>
{box('remember', 'Three key points about natural selection', '<ol><li>Selection acts on individuals, but <b>populations evolve</b>.</li>'
 '<li>It can only amplify or diminish <b>heritable</b> traits that already <b>differ</b> among individuals.</li>'
 '<li>Environments vary in place and time, so a trait that helps in one place or time may be useless or harmful in another.</li></ol>')}
<table class='keep'><tr><th>Natural selection</th><th>Artificial selection</th></tr>
<tr><td>Nature ‘decides’; works on individuals; e.g. finch beaks</td><td>Humans decide; selective breeding; inbreeding occurs; e.g. Dalmatians</td></tr></table>
<p class='small'>Darwin’s argument: if humans can cause big changes in a short time, nature can do so over a long time.</p>
</section>"""

S8 = f"""
<section class='flow'>
{sec(8, 'Population genetics and Hardy–Weinberg', 'Lectures 22–23 · Campbell Ch. 23')}
<p>Darwin could not explain how variation is maintained; Mendel’s discrete genes (not blending) provided the answer. Population genetics is the foundation for studying evolution.</p>
<div class='two'><div>
<h3>The Hardy–Weinberg theorem</h3>
<p>Allele and genotype frequencies in a gene pool <b>remain constant</b> from generation to generation unless acted on by agents other than sexual recombination (gene shuffling in meiosis). Such a population is <b>not evolving</b>.</p>
<div class='box note'><span class='bt'>Formulas (one gene, two alleles A and a)</span>
<p><i>p</i> = freq(A), <i>q</i> = freq(a) &nbsp;&nbsp; <b><i>p</i> + <i>q</i> = 1</b></p>
<p><b><i>p</i><sup>2</sup> + 2<i>pq</i> + <i>q</i><sup>2</sup> = 1</b> &nbsp;→&nbsp; AA, Aa, aa</p></div>
</div><div>
<h3>Five conditions for equilibrium</h3>
<table class='keep'><tr><th>Condition</th><th>If violated →</th></tr>
<tr><td>Extremely large population</td><td>Genetic drift</td></tr>
<tr><td>No gene flow</td><td>Gene flow</td></tr>
<tr><td>No mutations</td><td>Mutation</td></tr>
<tr><td>Random mating</td><td>Sexual selection / inbreeding</td></tr>
<tr><td>No natural selection</td><td>Natural selection</td></tr></table>
<p class='small'><b>Microevolution</b> = generation-to-generation change in a population’s allele frequencies.</p>
</div></div>

{box('tip', 'Solving a Hardy–Weinberg problem', '<ol><li>Find <i>q</i><sup>2</sup> = fraction showing the <b>recessive</b> phenotype (the only class you can read directly).</li>'
 '<li><i>q</i> = √(<i>q</i><sup>2</sup>); <i>p</i> = 1 − <i>q</i>.</li><li>Heterozygotes = 2<i>pq</i>; homozygous dominant = <i>p</i><sup>2</sup>; multiply by N for numbers.</li>'
 '<li>If genotype counts are given, <b>count alleles</b> instead: <i>p</i> = (2·AA + Aa)/(2N). Compare observed with <i>p</i><sup>2</sup> : 2<i>pq</i> : <i>q</i><sup>2</sup> to test equilibrium.</li></ol>')}

<table class='keep'><tr><th style='width:30%'>Worked example</th><th>Working</th><th style='width:22%'>Answer</th></tr>
<tr><td>Slide: <i>q</i><sup>2</sup> = 0.09</td><td><i>q</i> = 0.3, <i>p</i> = 0.7; <i>p</i><sup>2</sup> = 0.49, 2<i>pq</i> = 0.42</td><td>0.49 : 0.42 : 0.09</td></tr>
<tr><td>Slide: 552 plants, 546 purple</td><td><i>q</i><sup>2</sup> = 6/552 = 0.0109 → <i>q</i> = 0.104</td><td><i>q</i> ≈ 0.1, <i>p</i> ≈ 0.9</td></tr>
<tr><td>Slide: lizards 1024 <i>GG</i>, 512 <i>Gg</i>, 64 <i>gg</i></td><td><i>G</i> = 2×1024 + 512 = 2560; <i>g</i> = 512 + 2×64 = 640; total 3200</td><td><i>p</i> = 0.8, <i>q</i> = 0.2; 0.64 : 0.32 : 0.04</td></tr>
<tr><td>Campbell: PKU, 1 in 10,000</td><td><i>q</i> = 0.01, <i>p</i> = 0.99; 2<i>pq</i> = 0.0198</td><td>≈ 2% carriers</td></tr></table>

<h3>Causes of microevolution (lecture list)</h3>
<table><tr><th style='width:22%'>Cause</th><th>What it does</th></tr>
<tr><td><b>Mutation</b></td><td>Changes in DNA (point mutations, gene duplication) alter or create new alleles.</td></tr>
<tr><td><b>Sexual recombination</b></td><td>Rearranges alleles into fresh combinations every generation.</td></tr>
<tr><td><b>Natural selection</b></td><td>Individuals with certain heritable traits survive and reproduce at higher rates.</td></tr>
<tr><td><b>Genetic drift</b></td><td>Chance changes in allele frequencies; strongest in small populations. <b>Bottleneck effect</b> (drastic reduction in size) and <b>founder effect</b> (a few individuals colonise a new area). Slide example: <i>p</i> = 0.7 → 0.5 → 1.0 (allele <i>r</i> lost by chance).</td></tr>
<tr><td><b>Gene flow</b></td><td>Movement of alleles by migration of fertile individuals or gametes (wind-blown pollen); reduces differences between populations.</td></tr></table>
{box('note', 'Slides vs Campbell', '<p>The slides list sexual recombination as a cause; Campbell 10th ed. names <b>natural selection, genetic drift and gene flow</b> as the three mechanisms that directly change allele frequencies, with mutation and recombination as sources of variation. Recombination makes new combinations but, by itself, does not change allele frequencies (that is what Hardy–Weinberg says).</p>')}

<h3>Fitness and modes of selection</h3>
<p><b>Fitness</b>: the contribution an individual makes to the gene pool of the next generation (relative to others). Natural selection alters the frequency distribution of heritable traits in three ways:</p>
<div class='fig'>{selection_svg()}</div>
<table class='keep'><tr><th>Mode</th><th>Example on the slide</th></tr>
<tr><td>Directional</td><td>Beak sizes of finches during wet/dry seasons in the Galápagos</td></tr>
<tr><td>Disruptive (diversifying)</td><td>Small beaks for small seeds; large beaks for large seeds</td></tr>
<tr><td>Stabilizing</td><td>Average human birth weight</td></tr></table>
</section>"""

S9 = f"""
<section class='page-break'>
{sec(9, 'Last-minute revision sheet', 'Numbers, names, formulas, ratios and traps on two pages')}
<div class='two'><div>
<h3>Numbers</h3>
<table class='keep'>
<tr><td>Human chromosomes</td><td>2<i>n</i> = 46, <i>n</i> = 23; 92 chromatids in G<sub>2</sub></td></tr>
<tr><td>Independent assortment (humans)</td><td>2<sup>23</sup> ≈ 8.4 million; × fertilization ≈ 70 trillion</td></tr>
<tr><td>Mendel’s F<sub>2</sub></td><td>705 : 224 ≈ 3.15 : 1</td></tr>
<tr><td>ABO</td><td>3 alleles, 6 genotypes, 4 phenotypes</td></tr>
<tr><td>Interphase</td><td>~90% of the cell cycle</td></tr>
<tr><td>B-DNA</td><td>10 bp/turn, 3.4 Å/bp, 20 Å wide, right-handed</td></tr>
<tr><td>Z-DNA</td><td>12 bp/turn, left-handed; A-DNA 11 bp/turn</td></tr>
<tr><td>GPCR</td><td>7 transmembrane domains; ~60% of drugs</td></tr>
<tr><td>Adrenaline cascade</td><td>1 → 10<sup>8</sup> glucose 1-phosphate</td></tr>
<tr><td>Genomics data (2015)</td><td>~1 zetta-base/yr; 2–40 exabytes stored</td></tr>
<tr><td>DNA polymerase error rate</td><td>~1 in 10<sup>4</sup>–10<sup>5</sup> nucleotides</td></tr>
<tr><td>Daphne Major drought (1977)</td><td>~1200 → ~180 finches</td></tr></table>
<h3>Ratios</h3>
<table class='keep'>
<tr><td>Monohybrid F<sub>2</sub></td><td>3 : 1 (phenotype), 1 : 2 : 1 (genotype)</td></tr>
<tr><td>Dihybrid F<sub>2</sub></td><td>9 : 3 : 3 : 1</td></tr>
<tr><td>Testcross <i>Pp</i> × <i>pp</i></td><td>1 : 1</td></tr>
<tr><td>Incomplete dominance F<sub>2</sub></td><td>1 red : 2 pink : 1 white</td></tr>
<tr><td>Morgan F<sub>2</sub></td><td>3 red : 1 white (all white = male)</td></tr>
<tr><td>Trihybrid slide problem</td><td>3/8</td></tr></table>
</div><div>
<h3>Names and dates</h3>
<table class='keep'>
<tr><td>Mendel</td><td>1866 — laws of inheritance</td></tr>
<tr><td>Darwin</td><td>1859 — <i>Origin of Species</i>; HMS Beagle</td></tr>
<tr><td>Griffith</td><td>1928 — transforming principle</td></tr>
<tr><td>Avery, MacLeod, McCarty</td><td>1944 — DNA is the transforming principle</td></tr>
<tr><td>Watson &amp; Crick</td><td>1953 — double helix</td></tr>
<tr><td>Morgan</td><td>X-linked white-eye gene in <i>Drosophila</i></td></tr>
<tr><td>Earl Sutherland</td><td>Nobel 1971 — hormone action, cAMP</td></tr>
<tr><td>Gilman &amp; Rodbell</td><td>Nobel 1994 — G proteins</td></tr>
<tr><td>Dayhoff, Eck, Ledley</td><td>~1960 — bioinformatics; PIR</td></tr>
<tr><td>Baker, Hassabis, Jumper</td><td>Nobel Chemistry 2024 — protein design, AlphaFold</td></tr>
<tr><td>Malthus</td><td>Populations grow exponentially, food linearly</td></tr>
<tr><td>Peter &amp; Rosemary Grant (Campbell)</td><td>Medium ground finch, Daphne Major</td></tr></table>
<h3>Formulas</h3>
<table class='keep'>
<tr><td>Gamete types</td><td>2<sup><i>n</i></sup> (<i>n</i> heterozygous genes)</td></tr>
<tr><td>“and” / “or”</td><td>multiply / add</td></tr>
<tr><td>Hardy–Weinberg</td><td><i>p</i> + <i>q</i> = 1; <i>p</i><sup>2</sup> + 2<i>pq</i> + <i>q</i><sup>2</sup> = 1</td></tr>
<tr><td>Allele counting</td><td><i>p</i> = (2·AA + Aa) / 2N</td></tr>
<tr><td>DNA length</td><td>bp × 0.34 nm (B-DNA)</td></tr></table>
</div></div>
{box('trap', 'Twelve classic traps', '<ol>'
 '<li>Character (flower colour) ≠ trait (purple).</li>'
 '<li>Segregation = one gene; independent assortment = different genes.</li>'
 '<li>P(normal child of two carriers is a carrier) = 2/3, not 1/2.</li>'
 '<li>Codominance (AB) ≠ incomplete dominance (pink).</li>'
 '<li>Nuclear envelope breaks up in prometaphase.</li>'
 '<li>No DNA replication between meiosis I and II.</li>'
 '<li>Anaphase I: homologues separate; anaphase II: sister chromatids.</li>'
 '<li>Sons get their X from their mother — never X-linked traits from their father.</li>'
 '<li>G protein: GTP = ON; adenylyl cyclase makes cAMP; phosphodiesterase breaks it.</li>'
 '<li>-Omics complement, not replace, single-molecule studies.</li>'
 '<li>Individuals don’t evolve; populations do. Selection only acts on existing heritable variation.</li>'
 '<li>Hardy–Weinberg: start from the recessive phenotype (<i>q</i><sup>2</sup>), never from the dominant one.</li></ol>')}
</section>"""


def build():
    html = page("BB 101 End-Sem — Short Notes", COVER + S1 + S2 + S3 + S4 + S5 + S6 + S7 + S8 + S9, NOTES_CSS)
    with open(os.path.join(HERE, "notes.html"), "w") as f:
        f.write(html)
    print("notes.html written")


if __name__ == "__main__":
    build()
