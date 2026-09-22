#!/usr/bin/env node
// The CI gate. Loads index.html's script into a bare VM context (no
// document, so the page never boots) and checks the book: every lesson
// has its nine parts, every calculator reproduces the numbers its worked
// example quotes, every lesson's figure draws from its calculator's
// defaults with a caption in words, every card and glossary entry points
// at a lesson, and the repository never uses the name of the framework
// the case replaced. Cross-references are counted only where the prose
// writes Lesson or Lessons before the ids, never from a bare backticked
// capital, which in this course is a variable.
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
  const { LESSONS, CARDS, GLOSSARY, PARTS, RULES, SESSION_FIELDS, fmt, md, plain, firstSentence, FIG } = BOOK;
  if (!FIG || typeof FIG.render !== "function") fail("the engine has lost FIG, the figure renderer");
  if (typeof plain !== "function" || typeof firstSentence !== "function") fail("the engine has lost plain/firstSentence, which the lessons page summarises with");

  // ---- lessons ---------------------------------------------------------
  // A cross-reference is the word Lesson(s) and then ids: "Lesson F", "Lessons A
  // and F", "Lessons H to N", backticks optional. A bare `B` is deliberately not
  // one: single capitals are variables in this course's notation (Lesson G's `B`
  // is the bootstrap resample count), so counting them would let a formula satisfy
  // the refers-to-another-lesson gate below, and would raise a phantom dangling
  // reference if a lesson were ever renamed. The id pattern is every capital, not
  // A–N, so that an id which does not exist fails loudly instead of being ignored.
  const ID = "[A-Z]\\b", TAIL = "(?:'s)?", ONE = "`?" + ID + "`?" + TAIL;
  const MENTION = new RegExp("Lessons?\\s+(" + ONE + "(?:\\s*(?:,|and|or|to|through|[-–])\\s*" + ONE + ")*)", "g");
  const EACH = new RegExp("`?(" + ID + ")`?", "g");
  const RANGE = new RegExp("`?(" + ID + ")`?" + TAIL + "\\s*(?:to|through|[-–])\\s*`?(" + ID + ")`?", "g");
  const lessonRefs = (text) => {
    const refs = new Set();
    for (const mention of String(text).matchAll(MENTION)) {
      for (const id of mention[1].matchAll(EACH)) refs.add(id[1]);
      for (const range of mention[1].matchAll(RANGE)) { // "Lessons H to N" names every lesson between them
        const a = range[1].charCodeAt(0), b = range[2].charCodeAt(0);
        for (let c = Math.min(a, b); c <= Math.max(a, b); c++) refs.add(String.fromCharCode(c));
      }
    }
    return refs;
  };
  if (LESSONS.length < 12) fail(`expected at least 12 lessons (A–L), found ${LESSONS.length}`);
  LESSONS.forEach((l, i) => {
    const want = String.fromCharCode(65 + i);
    if (l.id !== want) fail(`lesson ${i} has id ${l.id}, expected ${want}`);
    if (!l.title) fail(`lesson ${l.id} has no title`);
    // the gentle track's plain-words page: present, substantial, and in words (no backtick mathematics)
    if (typeof l.gentle !== "string" || l.gentle.trim().length < 300) fail(`lesson ${l.id}: gentle page missing or too short`);
    else if (l.gentle.includes("`")) fail(`lesson ${l.id}: the gentle page is words, not notation`);
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
    // the figure: the worked example as a picture, drawn from the calculator's defaults, with a caption in words for the gentle page
    const f = l.figure;
    if (!f || typeof f.draw !== "function" || !f.title) fail(`lesson ${l.id}: figure missing (title, gentle, caption, draw)`);
    else {
      if (typeof f.gentle !== "string" || f.gentle.trim().length < 120) fail(`lesson ${l.id}: the figure's gentle caption is missing or too short`);
      else if (f.gentle.includes("`")) fail(`lesson ${l.id}: the figure's gentle caption is words, not notation`);
      if (typeof f.caption !== "string" || f.caption.trim().length < 40) fail(`lesson ${l.id}: the figure's caption is missing or too short`);
      for (const t of [f.gentle, f.caption]) if (typeof t === "string" && ((t.match(/`/g) || []).length % 2 || (t.match(/\*\*/g) || []).length % 2)) fail(`lesson ${l.id}: unbalanced markup in a figure caption`);
      if (l.calc) { try { const d = Object.fromEntries(l.calc.inputs.map(x => [x[0], x[2]])); const out = FIG.render(f.draw(d, l.calc.compute(d)), f.title);
          if (!/<svg /.test(out)) fail(`lesson ${l.id}: the figure drew nothing`); } catch (e) { fail(`lesson ${l.id}: the figure does not draw: ${e.message}`); } }
    }
    // The lessons page shows the first sentence of the question. It must end a
    // sentence, carry no leftover markup, and cut where the sentence really ends:
    // the character after it in the question is whitespace or nothing, which is
    // what a cut inside 0.84 or mid-word fails.
    if (firstSentence && plain) {
      const summary = firstSentence(l.question), body = plain(l.question).trim(), rest = body.slice(summary.length);
      if (/[*`]/.test(summary)) fail(`lesson ${l.id}: the lessons-page summary leaks markup: ${summary}`);
      else if (!/[.?!]$/.test(summary)) fail(`lesson ${l.id}: the lessons-page summary does not end a sentence: ${summary}`);
      else if (rest && !/^\s/.test(rest)) fail(`lesson ${l.id}: the lessons-page summary cuts mid-token: …${summary.slice(-30)}`);
    }
    // every lesson refers to at least one other lesson, so the book is a web not a list
    const refs = new Set(); for (const key of ["principle", "maths", "assumptions", "pitfall", "application"]) for (const ref of lessonRefs(l[key])) refs.add(ref);
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
  if (RULES.length !== 10) fail(`expected ten reasoning rules, found ${RULES.length}`);
  const CAL = BOOK.CALIBRATION;
  if (!CAL || !Array.isArray(CAL.questions) || CAL.questions.length < 3) fail("the start page needs at least three calibration questions");
  else {
    CAL.questions.forEach((x, i) => { if (!x.q || !Array.isArray(x.o) || x.o.length < 3 || !Number.isInteger(x.a) || x.a < 0 || x.a >= x.o.length) fail(`calibration question ${i + 1} is malformed`); });
    if (new Set(CAL.questions.map(x => x.a)).size < 2) fail("every calibration answer is in the same position");
    if (!CAL.self || !Array.isArray(CAL.self.o) || !Number.isInteger(CAL.self.gentleAt)) fail("the calibration's self-report question is malformed");
    if (!Number.isInteger(CAL.passAt) || CAL.passAt < 1 || CAL.passAt > CAL.questions.length) fail("calibration passAt out of range");
    if (!CAL.verdict || !CAL.verdict.gentle || !CAL.verdict.standard) fail("the calibration needs both verdicts");
  }
  // the static figures on the case and start pages draw too
  for (const [name, obj] of [["home", BOOK.SITE], ["case", BOOK.CASE], ["start", CAL]]) { if (!obj || !obj.figure) continue;
    try { if (!/<svg /.test(FIG.render(obj.figure.spec, obj.figure.title))) fail(`the ${name} page's figure drew nothing`); } catch (e) { fail(`the ${name} page's figure does not draw: ${e.message}`); } }
  CARDS.forEach(c => { if (!LESSONS.find(l => l.id === c.lesson)) fail(`card ${c.id} points at lesson ${c.lesson}`); if (!c.lines || c.lines.length < 5) fail(`card ${c.id} is thin`); });
  GLOSSARY.forEach(g => { if (!lessonRefs(g[1]).size) fail(`glossary entry "${g[0]}" names no lesson`); });
  if (SESSION_FIELDS.length !== 5) fail("the session note has five lines");
  const { READING } = BOOK;
  if (!Array.isArray(READING) || READING.length < 5) fail("the reading list is missing or thin");
  else READING.forEach((r, i) => {
    if (!r.cite || !r.why || !Array.isArray(r.lessons) || !r.lessons.length) fail(`reading entry ${i + 1} needs cite, why and lessons`);
    else r.lessons.forEach(id => { if (!LESSONS.find(l => l.id === id)) fail(`reading entry ${i + 1} points at lesson ${id}`); });
  });
}

// ---- exercises ------------------------------------------------------
// Every exercise asks the reader to work on their own evaluation, so every
// one also offers a way through for a reader who has not got one, and says
// what it costs in time. Both are promises to the reader, so both are gated.
if (BOOK) {
  const { LESSONS } = BOOK;
  LESSONS.forEach(l => {
    if (!/\*\*No evaluation of your own\?\*\*/.test(l.exercise))
      fail(`lesson ${l.id}: the exercise offers no way through for a reader without an evaluation of their own`);
    if (!/\*[^*]+\*\s*$/.test(l.exercise))
      fail(`lesson ${l.id}: the exercise does not end with how long it takes`);
  });

  // The fallbacks quote Reference Set 2, and the course's rule is that a
  // number in the prose is checked against what produces it. The calculators
  // cover their own examples; these come from the csv, so they are counted
  // here. Derived figures (the intra-cluster correlation, the design effect)
  // depend on an estimator choice and are deliberately not pinned.
  const csv = path.join(root, "data", "reference-set-2.csv");
  if (!fs.existsSync(csv)) fail("data/reference-set-2.csv is missing, and the exercises quote it");
  else {
    const lines = fs.readFileSync(csv, "utf8").trim().split(/\r?\n/);
    const head = lines[0].split(","), idx = (c) => head.indexOf(c);
    const rows = lines.slice(1).map(l => l.split(","));
    const yes = (v) => /^(true|1|yes)$/i.test((v || "").trim());
    const kept = (r) => yes(r[idx("published")]) || yes(r[idx("master")]);
    const outings = new Map();
    rows.forEach(r => { const o = r[idx("outing")]; const e = outings.get(o) || { n: 0, k: 0 }; e.n++; if (kept(r)) e.k++; outings.set(o, e); });
    const smallest = [...outings.values()].sort((a, b) => a.n - b.n)[0];
    const facts = [
      ["frames", rows.length, 12713],
      ["keepers", rows.filter(kept).length, 41],
      ["outings", outings.size, 33],
      ["frames in the smallest outing", smallest.n, 30],
      ["keepers in the smallest outing", smallest.k, 0],
      ["outings with no keeper", [...outings.values()].filter(o => o.k === 0).length, 23],
      ["rows with no ISO", rows.filter(r => !(r[idx("iso")] || "").trim()).length, 2474],
    ];
    facts.forEach(([what, got, want]) => { if (got !== want) fail(`the exercises say Reference Set 2 has ${want} ${what}; the csv has ${got}`); });
  }
}
// ---- Reference Set 3 -------------------------------------------------
// The same rule as Reference Set 2: a number in the prose is checked against
// what produces it. This set carries a predictor as well as a verdict, so the
// figures quoted are a confusion matrix and a paired table, not just counts.
{
  const csv3 = path.join(root, "data", "reference-set-3.csv");
  if (!fs.existsSync(csv3)) fail("data/reference-set-3.csv is missing, and the case page and four exercises quote it");
  else {
    const split = (line) => { // the album column contains commas, so fields may be quoted
      const out = []; let cur = "", q = false;
      for (const ch of line) {
        if (ch === '"') { q = !q; continue; }
        if (ch === "," && !q) { out.push(cur); cur = ""; continue; }
        cur += ch;
      }
      out.push(cur); return out;
    };
    const lines = fs.readFileSync(csv3, "utf8").trim().split(/\r?\n/);
    const head = split(lines[0]);
    const rows = lines.slice(1).map(l => Object.fromEntries(split(l).map((v, i) => [head[i], v])));
    const yes = (r, k) => r[k] === "1";
    const truth = (r) => yes(r, "assigned"), A = (r) => yes(r, "rule_a"), B = (r) => yes(r, "rule_b");
    const count = (f) => rows.filter(f).length;
    const labels = [...new Set(rows.map(r => r.label))];
    const recallOf = (label) => { const s = rows.filter(r => r.label === label);
      const tp = s.filter(r => truth(r) && A(r)).length, fn = s.filter(r => truth(r) && !A(r)).length;
      return tp + fn ? tp / (tp + fn) : null; };
    const recalls = labels.map(recallOf).filter(x => x !== null);
    const tpA = count(r => truth(r) && A(r)), fnA = count(r => truth(r) && !A(r));
    const bin = (lo, hi) => { const s = rows.filter(r => +r.score >= lo && +r.score < hi);
      return s.length ? s.filter(truth).length / s.length : null; };
    const facts = [
      ["photo-label pairs", rows.length, 6086],
      ["photographs", new Set(rows.map(r => r.slug)).size, 179],
      ["labels", labels.length, 34],
      ["assigned pairs", count(truth), 398],
      ["rule A true positives", tpA, 100],
      ["rule A false positives", count(r => !truth(r) && A(r)), 30],
      ["rule A false negatives", fnA, 298],
      ["discordant pairs", count(r => (A(r) === truth(r)) !== (B(r) === truth(r))), 82],
      ["pairs only rule A gets right", count(r => A(r) === truth(r) && B(r) !== truth(r)), 52],
      ["pairs only rule B gets right", count(r => B(r) === truth(r) && A(r) !== truth(r)), 30],
      ["labels rule A always finds", recalls.filter(x => x === 1).length, 6],
      ["labels rule A never finds", recalls.filter(x => x === 0).length, 16],
    ];
    facts.forEach(([what, got, want]) => { if (got !== want) fail(`the course says Reference Set 3 has ${want} ${what}; the csv has ${got}`); });
    const rates = [
      ["micro recall", tpA / (tpA + fnA), 0.251],
      ["macro recall", recalls.reduce((a, b) => a + b, 0) / recalls.length, 0.316],
      ["the rate in the zero-score bin", bin(0, 0.01), 0.046],
      ["the rate in the part-score bin", bin(0.01, 0.99), 0.359],
      ["the rate in the full-score bin", bin(0.99, 1.01), 0.761],
    ];
    rates.forEach(([what, got, want]) => {
      if (got === null || Math.abs(got - want) > 0.0005) fail(`the course says Reference Set 3's ${what} is ${want}; the csv gives ${got === null ? "an empty bin" : got.toFixed(4)}`);
    });
  }
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
console.log(`ok: ${n} lessons, every calculator reproduces its worked example, every figure draws, ${BOOK ? BOOK.CARDS.length : 0} cards, ${BOOK ? BOOK.GLOSSARY.length : 0} glossary entries, one file, no network, no replaced name`);
