#!/usr/bin/env node
// The CI gate. Loads index.html's script into a bare VM context (no
// document, so the page never boots) and checks the book: every lesson
// has its nine parts, every calculator reproduces the numbers its worked
// example quotes, every card and glossary entry points at a lesson, and
// the repository never uses the name of the framework the case replaced.
// No dependencies; runs on the Node that ships with the CI runner.
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const problems = [];
const fail = (m) => problems.push(m);

// ---- load the data and engine without a DOM -------------------------
const scripts = html.match(/<script>([\s\S]*?)<\/script>/g) || [];
if (scripts.length !== 1) fail(`expected exactly one <script>, found ${scripts.length}`);
const src = scripts[0].replace(/^<script>/, "").replace(/<\/script>$/, "");
const ctx = vm.createContext({ Math, console });
let BOOK;
try { BOOK = vm.runInContext(src + "\nBOOK", ctx); } catch (e) { fail("script failed to load: " + e.message); }

if (BOOK) {
  const { LESSONS, CARDS, GLOSSARY, PARTS, RULES, SESSION_FIELDS, fmt, md } = BOOK;

  // ---- lessons ---------------------------------------------------------
  if (LESSONS.length < 12) fail(`expected at least 12 lessons (A–L), found ${LESSONS.length}`);
  LESSONS.forEach((l, i) => {
    const want = String.fromCharCode(65 + i);
    if (l.id !== want) fail(`lesson ${i} has id ${l.id}, expected ${want}`);
    if (!l.title) fail(`lesson ${l.id} has no title`);
    for (const [key, name] of PARTS) {
      if (key === "diagnostic") {
        if (!l.diagnostic || !l.diagnostic.q || !l.diagnostic.a) fail(`lesson ${l.id}: diagnostic needs q and a`);
      } else if (typeof l[key] !== "string" || l[key].trim().length < 40) fail(`lesson ${l.id}: part "${name}" missing or too short`);
    }
    // markup sanity: balanced backticks and bold markers in every part
    for (const key of Object.keys(l)) {
      const texts = key === "diagnostic" ? [l.diagnostic.q, l.diagnostic.a] : (typeof l[key] === "string" ? [l[key]] : []);
      for (const t of texts) {
        if ((t.match(/`/g) || []).length % 2) fail(`lesson ${l.id}: unbalanced backticks in ${key}`);
        if ((t.match(/\*\*/g) || []).length % 2) fail(`lesson ${l.id}: unbalanced ** in ${key}`);
        try { md(t); } catch (e) { fail(`lesson ${l.id}: ${key} does not render: ${e.message}`); }
      }
    }
    // every lesson refers to at least one other lesson, so the book is a web not a list
    const refs = new Set(); for (const key of ["principle", "maths", "assumptions", "pitfall", "application"]) for (const m of String(l[key]).matchAll(/Lessons? ([A-N])/g)) refs.add(m[1]);
    if (refs.size === 0 && i > 0) fail(`lesson ${l.id} never refers to another lesson`);
    refs.forEach(r => { if (!LESSONS.find(x => x.id === r)) fail(`lesson ${l.id} refers to lesson ${r}, which does not exist`); });

    // ---- calculator reproduces the worked example -----------------------
    const c = l.calc;
    if (!c || !Array.isArray(c.inputs) || !Array.isArray(c.outputs) || typeof c.compute !== "function" || !c.expect) { fail(`lesson ${l.id}: calculator incomplete`); return; }
    const defaults = Object.fromEntries(c.inputs.map(x => [x[0], x[2]]));
    let r; try { r = c.compute(defaults); } catch (e) { fail(`lesson ${l.id}: compute threw: ${e.message}`); return; }
    const decimals = Object.fromEntries(c.outputs.map(o => [o[0], o[2]]));
    for (const [k, want] of Object.entries(c.expect)) {
      if (!(k in decimals)) { fail(`lesson ${l.id}: expect.${k} is not an output`); continue; }
      const got = r[k]; const d = decimals[k]; const tol = 0.5 * Math.pow(10, -d) + 1e-9;
      if (typeof got !== "number" || Math.abs(got - want) > tol) fail(`lesson ${l.id}: ${k} computes to ${fmt(got, d + 2)}, example says ${want}`);
      // the number quoted in the example prose must be the one the calculator produces
      const shown = fmt(want, d); const grouped = shown.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      const prose = l.example.replace(/−/g, "-"); // prose writes a real minus sign; the calculator a hyphen
      if (!prose.includes(shown) && !prose.includes(grouped)) fail(`lesson ${l.id}: example prose does not quote ${k} = ${shown}`);
    }
    if (c.verdictKey && typeof r[c.verdictKey] !== "string") fail(`lesson ${l.id}: verdict output missing`);
  });

  // ---- exams -----------------------------------------------------------
  const { EXAMS } = BOOK;
  LESSONS.forEach(l => {
    const ex = EXAMS && EXAMS[l.id];
    if (!Array.isArray(ex) || ex.length < 4) { fail(`lesson ${l.id}: exam needs at least four questions`); return; }
    ex.forEach((x, i) => {
      const tag = `lesson ${l.id} exam question ${i + 1}`;
      if (!x.q || x.q.length < 20) fail(`${tag}: question missing or too short`);
      if (!Array.isArray(x.o) || x.o.length < 3) fail(`${tag}: needs at least three options`);
      else { if (new Set(x.o).size !== x.o.length) fail(`${tag}: duplicate options`); if (!Number.isInteger(x.a) || x.a < 0 || x.a >= x.o.length) fail(`${tag}: answer index out of range`); }
      if (!x.why || x.why.length < 20) fail(`${tag}: no reason given`);
    });
    // the correct option must not always sit in the same place
    const positions = new Set(ex.map(x => x.a)); if (positions.size < 2) fail(`lesson ${l.id}: every correct answer is in the same position`);
  });
  Object.keys(EXAMS || {}).forEach(id => { if (!LESSONS.find(l => l.id === id)) fail(`exam for lesson ${id}, which does not exist`); });

  // ---- rules, cards, glossary, session -------------------------------
  if (RULES.length !== 9) fail(`expected nine reasoning rules, found ${RULES.length}`);
  CARDS.forEach(c => { if (!LESSONS.find(l => l.id === c.lesson)) fail(`card ${c.id} points at lesson ${c.lesson}`); if (!c.lines || c.lines.length < 5) fail(`card ${c.id} is thin`); });
  GLOSSARY.forEach(g => { if (!/Lessons? [A-N]/.test(g[1])) fail(`glossary entry "${g[0]}" names no lesson`); });
  if (SESSION_FIELDS.length !== 5) fail("the session note has five lines");
  const { READING } = BOOK;
  if (!Array.isArray(READING) || READING.length < 5) fail("the reading list is missing or thin");
  else READING.forEach((r, i) => {
    if (!r.cite || !r.why || !Array.isArray(r.lessons) || !r.lessons.length) fail(`reading entry ${i + 1} needs cite, why and lessons`);
    else r.lessons.forEach(id => { if (!LESSONS.find(l => l.id === id)) fail(`reading entry ${i + 1} points at lesson ${id}`); });
  });
}

// ---- the page is one file with no network --------------------------
if (/<script[^>]+src=/i.test(html) || /fetch\(|XMLHttpRequest|<link[^>]+href="(https?:|\/\/)/i.test(html)) fail("index.html reaches for the network");
if (!/WORLD DATA/.test(html) || !/ENGINE/.test(html)) fail("index.html has lost its two section markers");

// ---- the replaced name never appears ---------------------------------
// The case replaced a real framework whose name is not to appear in this
// repository. The name is assembled here so this file does not contain it.
const banned = String.fromCharCode(70, 82, 71);
const walk = (dir) => fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => {
  if (e.name === ".git" || e.name === "node_modules") return [];
  const p = path.join(dir, e.name); return e.isDirectory() ? walk(p) : [p]; });
for (const f of walk(root)) {
  if (path.resolve(f) === path.resolve(__filename)) continue;
  const text = fs.readFileSync(f, "utf8");
  if (new RegExp("\\b" + banned + "\\b").test(text)) fail(`${path.relative(root, f)} uses the replaced name`);
}

// ---- report ---------------------------------------------------------
if (problems.length) { console.error("check failed:\n  " + problems.join("\n  ")); process.exit(1); }
const n = BOOK ? BOOK.LESSONS.length : 0;
console.log(`ok: ${n} lessons, every calculator reproduces its worked example, ${BOOK ? BOOK.CARDS.length : 0} cards, ${BOOK ? BOOK.GLOSSARY.length : 0} glossary entries, one file, no network, no replaced name`);
