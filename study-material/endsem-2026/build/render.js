// Render an HTML file to an A4 PDF with Chromium.  Usage: node render.js <in.html> <out.pdf> "<footer title>"
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const [inp, out, title] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + path.resolve(inp), { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: out,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate:
      `<div style="width:100%;font-family:Inter,sans-serif;font-size:7.5px;color:#5b6475;padding:0 14mm;display:flex;justify-content:space-between">` +
      `<span>${title}</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`,
  });
  await browser.close();
  console.log("wrote", out);
})();
