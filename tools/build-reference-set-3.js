#!/usr/bin/env node
// LOCAL AUTHORING TOOL. Rebuilds data/reference-set-3.csv from a sibling
// checkout of the photography repository. It is not part of CI and not part of
// tools/check.js, which reads only the committed csv — the sibling is not there
// on a runner. No dependencies, like everything else here.
//
//   node tools/build-reference-set-3.js [path-to-dermot-cochran-photography]
//
// What it emits, and what it deliberately does not. Each row is one
// (photo, label) pair: whether the photographer assigned that subject, and what
// two crude rules said about it. The alt text those rules read is NOT emitted.
// The photo pages are CC BY-NC-ND and this repository is CC BY 4.0, so the prose
// cannot cross; the outcome of applying a rule to it is a fact about the rule,
// not the prose, and every lesson needs the outcome rather than the text.
"use strict";
const fs = require("fs");
const path = require("path");

const root = process.argv[2] || path.resolve(__dirname, "..", "..", "dermot-cochran-photography");
const photoDir = path.join(root, "src", "photos");
if (!fs.existsSync(photoDir)) {
  console.error(`no photo pages at ${photoDir}\npass the path to the photography checkout as the first argument`);
  process.exit(1);
}

// ---- front matter, hand-rolled: the repository has no dependencies ----
function frontMatter(text) {
  // Three photo pages begin with a UTF-8 byte order mark. The site's own parser
  // tolerates it, so it is invisible there; a reader that does not strip it sees
  // no front matter at all and silently loses the photo. Strip it.
  if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);
  if (!text.startsWith("---")) return {};
  const end = text.indexOf("\n---", 3);
  if (end < 0) return {};
  const out = {};
  let key = null;
  for (const line of text.slice(3, end).split("\n")) {
    const item = line.match(/^\s*-\s+(.*)$/);
    if (item && Array.isArray(out[key])) { out[key].push(unquote(item[1])); continue; }
    const m = line.match(/^([a-z_]+):\s*(.*)$/);
    if (!m) continue;
    key = m[1];
    const v = m[2].trim();
    if (v.startsWith("[")) out[key] = v.slice(1, -1).split(",").map(s => unquote(s)).filter(Boolean);
    else if (v === "") out[key] = [];
    else out[key] = unquote(v);
  }
  return out;
}
const unquote = (s) => s.trim().replace(/^["']|["']$/g, "");

// ---- the two rules, deliberately crude; the crudeness is the teaching ----
const STOP = new Set(["and", "or", "in", "the", "of"]);
const words = (s) => s.toLowerCase().split(/[^a-z]+/).filter(Boolean);
const content = (label) => words(label).filter(w => !STOP.has(w) && w.length > 3);
const present = (alt, w) => alt.includes(w.replace(/s$/, ""));
// A: the whole label appears in the alt text.
const ruleA = (alt, label) => alt.includes(label.toLowerCase()) || alt.includes(label.toLowerCase().replace(/s$/, ""));
// B: any content word of the label appears.
const ruleB = (alt, label) => content(label).some(w => present(alt, w));
// The graded score both rules hide: the share of the label's words present.
const score = (alt, label) => { const c = content(label); return c.length ? c.filter(w => present(alt, w)).length / c.length : 0; };

// ---- read ----
const photos = fs.readdirSync(photoDir).filter(f => f.endsWith(".md")).sort().map(f => {
  const d = frontMatter(fs.readFileSync(path.join(photoDir, f), "utf8"));
  d.slug = f.replace(/\.md$/, "");
  return d;
}).filter(p => Array.isArray(p.subjects) && p.subjects.length);

const vocabulary = [...new Set(photos.flatMap(p => p.subjects))].sort();
const country = (location) => String(location || "").split(",").pop().trim();

const csvField = (v) => /[",\n]/.test(String(v)) ? `"${String(v).replace(/"/g, '""')}"` : String(v);
const lines = ["slug,album,category,country,year,label,assigned,rule_a,rule_b,score"];
for (const p of photos) {
  const alt = String(p.alt || "").toLowerCase();
  const truth = new Set(p.subjects);
  for (const label of vocabulary) {
    lines.push([p.slug, p.album, p.category, country(p.location), p.year, label,
      truth.has(label) ? 1 : 0, ruleA(alt, label) ? 1 : 0, ruleB(alt, label) ? 1 : 0,
      score(alt, label).toFixed(3)].map(csvField).join(","));
  }
}

const out = path.resolve(__dirname, "..", "data", "reference-set-3.csv");
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, lines.join("\n") + "\n");

// ---- say what it wrote, so the figures in the prose can be checked by eye too ----
const rows = lines.length - 1;
const n = (f) => lines.slice(1).filter(f).length;
const col = (i) => (l) => l.split(",").slice(-4)[i]; // assigned,rule_a,rule_b,score are the last four
const assigned = (l) => col(0)(l) === "1", a = (l) => col(1)(l) === "1", b = (l) => col(2)(l) === "1";
const tp = (r) => n(l => assigned(l) && r(l)), fp = (r) => n(l => !assigned(l) && r(l)), fn = (r) => n(l => assigned(l) && !r(l));
console.log(`wrote ${path.relative(process.cwd(), out)}`);
console.log(`  ${rows} pairs: ${photos.length} photos x ${vocabulary.length} labels, ${n(assigned)} assigned`);
for (const [name, r] of [["A", a], ["B", b]]) {
  const [T, F, N] = [tp(r), fp(r), fn(r)];
  console.log(`  rule ${name}: TP=${T} FP=${F} FN=${N} precision ${(T / (T + F)).toFixed(3)} recall ${(T / (T + N)).toFixed(3)}`);
}
console.log(`  discordant: b=${n(l => (a(l) === assigned(l)) && (b(l) !== assigned(l)))} c=${n(l => (a(l) !== assigned(l)) && (b(l) === assigned(l)))}`);
