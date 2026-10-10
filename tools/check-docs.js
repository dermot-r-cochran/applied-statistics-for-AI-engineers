#!/usr/bin/env node
// The documentation gate, beside check.js. Three checks, all on the
// Markdown rather than the page: every relative link in a Markdown file
// resolves to a file in the repository; no Markdown file carries more
// than one front-matter block (what a stray fragment left by a merge
// looks like); and every count the README states — lessons, rules,
// cards, exam and calibration questions, the lesson table, the two
// reference sets' sizes — matches what index.html and the csv files hold.
// check.js pins those numbers to the book and the csv; this pins the
// README to them, so a lesson added without its table row, or a dataset
// rebuilt without its paragraph, fails here rather than drifting.
// No dependencies; runs on the Node that ships with the CI runner.
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const problems = [];
const fail = (m) => problems.push(m);
const rel = (f) => path.relative(root, f).split(path.sep).join("/");

// ---- every Markdown file: one front-matter block at most, links resolve
const walk = (dir) => fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => {
  if (e.name === ".git" || e.name === "node_modules" || e.name === "_site") return [];
  const p = path.join(dir, e.name); return e.isDirectory() ? walk(p) : [p]; });
const mdFiles = walk(root).filter(f => /\.md$/i.test(f));
for (const f of mdFiles) {
  const text = fs.readFileSync(f, "utf8").replace(/\r\n/g, "\n");
  const lines = text.split("\n");
  let blocks = 0, i = 0;
  while (i < lines.length && lines[i].trim() === "---") {
    const close = lines.findIndex((l, j) => j > i && l.trim() === "---");
    if (close < 0) break;
    blocks++; i = close + 1;
    while (i < lines.length && !lines[i].trim()) i++;
  }
  if (blocks > 1) fail(`${rel(f)}: ${blocks} front-matter blocks`);
  const body = text.replace(/```[\s\S]*?```/g, "").replace(/`[^`\n]*`/g, "");
  for (const m of body.matchAll(/\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)/g)) {
    const target = m[1];
    if (/^[a-z][a-z0-9+.-]*:/i.test(target) || target.startsWith("#") || target.startsWith("//")) continue;
    const file = decodeURIComponent(target.split("#")[0].split("?")[0]);
    if (!file) continue;
    if (!fs.existsSync(path.resolve(path.dirname(f), file))) fail(`${rel(f)}: link ${target} resolves to no file`);
  }
}

// ---- the README's counts against the book and the csv files ----------
const WORDS = { one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10, eleven: 11, twelve: 12,
  thirteen: 13, fourteen: 14, fifteen: 15, sixteen: 16, seventeen: 17, eighteen: 18, nineteen: 19, twenty: 20 };
const number = (s) => s === undefined ? NaN : (WORDS[s.toLowerCase()] !== undefined ? WORDS[s.toLowerCase()] : parseInt(s.replace(/,/g, ""), 10));
const readme = fs.readFileSync(path.join(root, "README.md"), "utf8").replace(/\r\n/g, "\n");
const stated = (what, re) => { const m = readme.match(re); if (!m) { fail(`README no longer states ${what}; update the pattern in tools/check-docs.js with the prose`); return NaN; } return number(m[1]); };
const same = (what, got, want) => { if (!Number.isNaN(want) && got !== want) fail(`README says ${want} ${what}; the repository has ${got}`); };

const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const scripts = html.match(/<script>([\s\S]*?)<\/script>/g) || [];
let BOOK;
try { BOOK = vm.runInContext(scripts[0].replace(/^<script>/, "").replace(/<\/script>$/, "") + "\nBOOK", vm.createContext({ Math, console })); }
catch (e) { fail("script failed to load: " + e.message); }
if (BOOK) {
  const { LESSONS, RULES, CARDS, EXAMS, CALIBRATION } = BOOK;
  same("lessons", LESSONS.length, stated("the number of lessons", /\n(\w+), in the same nine parts each/));
  same("core reasoning rules", RULES.length, stated("the number of reasoning rules", /(\w+) \*\*core reasoning\s+rules\*\*/));
  same("reference cards", CARDS.length, stated("the number of reference cards", /(\w+) \*\*reference cards\*\*/));
  same("questions in every exam", Math.min(...LESSONS.map(l => (EXAMS[l.id] || []).length)), stated("the exam's length", /a (\w+)-question exam/));
  same("calibration questions", CALIBRATION.questions.length, stated("the number of calibration questions", /asks (\w+) short calibration questions/));
  // the lesson table: one row per lesson, in order, with the lesson's title (the README may shorten a title at its colon)
  const rows = [...readme.matchAll(/^\| ([A-Z]) \| ([^|]+?) \|/gm)].map(m => [m[1], m[2].trim()]);
  same("rows in the lesson table", rows.length, LESSONS.length);
  rows.forEach(([id, title], i) => {
    const l = LESSONS[i];
    if (!l || l.id !== id) fail(`README lesson table row ${i + 1} is ${id}; the book has ${l ? l.id : "no such lesson"}`);
    else if (title !== l.title && title !== l.title.split(":")[0]) fail(`README lesson table calls ${id} "${title}"; the book calls it "${l.title}"`);
  });
}

const split = (line) => { const out = []; let cur = "", q = false;
  for (const ch of line) { if (ch === '"') { q = !q; continue; } if (ch === "," && !q) { out.push(cur); cur = ""; continue; } cur += ch; }
  out.push(cur); return out; };
const csv = (name) => { const f = path.join(root, "data", name); if (!fs.existsSync(f)) { fail(`data/${name} is missing`); return null; }
  const lines = fs.readFileSync(f, "utf8").trim().split(/\r?\n/); const head = split(lines[0]);
  return lines.slice(1).map(l => Object.fromEntries(split(l).map((v, i) => [head[i], v]))); };
const rs2 = csv("reference-set-2.csv");
if (rs2) {
  const yes = (v) => /^(true|1|yes)$/i.test((v || "").trim());
  same("frames in Reference Set 2", rs2.length, stated("Reference Set 2's size", /\*\*Reference Set 2\*\*[^\n]*?is real: ([\d,]+) frames/));
  same("kept frames in Reference Set 2", rs2.filter(r => yes(r.published) || yes(r.master)).length, stated("Reference Set 2's keepers", /actually kept \((\d+) of them/));
}
const rs3 = csv("reference-set-3.csv");
if (rs3) {
  same("photographs in Reference Set 3", new Set(rs3.map(r => r.slug)).size, stated("Reference Set 3's photographs", /subject tags on (\d+) photographs/));
  same("labels in Reference Set 3", new Set(rs3.map(r => r.label)).size, stated("Reference Set 3's vocabulary", /a (\d+)-label vocabulary/));
  same("pairs in Reference Set 3", rs3.length, stated("Reference Set 3's pairs", /give ([\d,]+) \(photo, label\) pairs/));
  same("assigned pairs in Reference Set 3", rs3.filter(r => r.assigned === "1").length, stated("Reference Set 3's assigned pairs", /pairs, (\d+) of which carry the subject/));
}

// ---- report ---------------------------------------------------------
if (problems.length) { console.error("check-docs failed:\n  " + problems.join("\n  ")); process.exit(1); }
console.log(`ok: ${mdFiles.length} Markdown files, links resolve, one front-matter block at most, README counts match the book and the data`);
