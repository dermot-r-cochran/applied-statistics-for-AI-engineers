#!/usr/bin/env node
"use strict";
/* check-page — open the page and read every view without a browser.
 *
 * tools/check.js loads the script into a bare VM context with no
 * `document`, so the page never boots and everything below BOOK (the
 * router, the views, the sidebar, the calculators and their figures, the
 * reveal buttons, the exams and the scorecard, the start page and its
 * track suggestion, the track toggle, the mark-read button, the session
 * note, and localStorage) had no test. This check gives the same script a
 * stub for the browser: the page's own markup parsed into a small
 * document tree (the elements of index.html's body, so main and side
 * are real), an innerHTML that parses what it is given, querySelector
 * over the selectors the page uses, a location whose hash fires
 * hashchange, a localStorage in memory, and a window whose scrollTo only
 * counts. Then it does what a reader does: opens the page, reads every
 * view and every lesson on both tracks, changes calculator inputs and
 * holds the outputs and the figure to the calculator's own compute,
 * shows an answer, sits every exam at the pass mark and below it, marks
 * lessons read, answers the start page either side of its pass mark,
 * writes the session note, and reopens the page on the same store. The
 * stub lives here; the page gets no test hook, and nothing is read out
 * of index.html but its markup. Node only — nothing to install.
 *
 *     node tools/check-page.js
 */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.join(__dirname, "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error("no <script> block in index.html"); process.exit(1); }
const bodyMarkup = (html.match(/<body>([\s\S]*?)<script>/) || [, ""])[1];

let fails = 0, checks = 0;
const fail = (msg) => { fails++; console.error("  FAIL: " + msg); };
const ok = () => { checks++; };

// ---- the stub document ----

const VOID = new Set(["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"]);
const decode = (s) => s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, "\"").replace(/&#39;/g, "'").replace(/&amp;/g, "&");
const encode = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

class Text {
  constructor(s) { this.nodeType = 3; this.text = String(s); this.parent = null; }
  get textContent() { return this.text; }
  serialise() { return encode(this.text); }
}

class El {
  constructor(tag, attrs) {
    this.nodeType = 1; this.tagName = tag.toUpperCase(); this.tag = tag.toLowerCase(); this.attrs = attrs || {};
    this.children = []; this.parent = null; this.listeners = {}; this.checked = false; this._value = undefined;
    const self = this;
    this.classList = {
      contains: (n) => self.className.split(/\s+/).includes(n),
      add: (...ns) => { for (const n of ns) if (!self.classList.contains(n)) self.className = (self.className + " " + n).trim(); },
      remove: (...ns) => { self.className = self.className.split(/\s+/).filter((x) => x && !ns.includes(x)).join(" "); },
      toggle: (n, force) => { const on = force === undefined ? !self.classList.contains(n) : !!force; if (on) self.classList.add(n); else self.classList.remove(n); return on; }
    };
    this.dataset = new Proxy({}, { get: (t, p) => (typeof p === "string" ? self.attrs["data-" + p.replace(/[A-Z]/g, (c) => "-" + c.toLowerCase())] : undefined) });
  }
  get id() { return this.attrs.id || ""; }
  get className() { return this.attrs.class || ""; }
  set className(v) { this.attrs.class = String(v); }
  get hidden() { return "hidden" in this.attrs; }
  set hidden(v) { if (v) this.attrs.hidden = ""; else delete this.attrs.hidden; }
  get type() { return this.attrs.type || (this.tag === "input" ? "text" : ""); }
  get name() { return this.attrs.name || ""; }
  get href() { return this.attrs.href || ""; }
  get value() { if (this._value !== undefined) return this._value; return this.tag === "textarea" ? this.textContent : (this.attrs.value || ""); }
  set value(v) { this._value = String(v); }
  getAttribute(n) { return n in this.attrs ? this.attrs[n] : null; }
  setAttribute(n, v) { this.attrs[n] = String(v); }
  get textContent() { return this.children.map((c) => c.textContent).join(""); }
  set textContent(v) { this.clear(); if (String(v) !== "") this.children.push(Object.assign(new Text(v), { parent: this })); }
  get innerHTML() { return this.children.map((c) => c.serialise()).join(""); }
  set innerHTML(v) { this.clear(); for (const c of parse(String(v))) { c.parent = this; this.children.push(c); } }
  serialise() { const a = Object.entries(this.attrs).map(([k, v]) => v === "" ? " " + k : ` ${k}="${v}"`).join(""); return VOID.has(this.tag) ? `<${this.tag}${a}>` : `<${this.tag}${a}>${this.innerHTML}</${this.tag}>`; }
  clear() { for (const c of this.children) c.parent = null; this.children = []; }
  scrollIntoView() { scrolled.push(this.id || this.tag); }
  focus() {}
  addEventListener(type, fn) { (this.listeners[type] = this.listeners[type] || []).push(fn); }
  // an event dispatched here and bubbling up to the document, as in a browser
  dispatch(type, ev) { const e = Object.assign({ type, target: this, preventDefault() { this.defaulted = true; } }, ev || {}); for (let n = this; n; n = n.parent) for (const fn of (n.listeners[type] || []).slice()) fn(e); return e; }
  // every element in the tree below this one, this one included
  all() { return [this].concat(...this.children.filter((c) => c.nodeType === 1).map((c) => c.all())); }
  querySelectorAll(sel) { return this.all().slice(1).filter((e) => matches(e, sel)); }
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
}

// The markup the page writes is its own templates, so the parser is small:
// tags with quoted or bare attributes, self-closing tags, void elements,
// comments, text. Anything unclosed is closed by its parent's end.
function parse(src) {
  const out = [], stack = [];
  const push = (n) => { const p = stack[stack.length - 1]; if (p) { n.parent = p; p.children.push(n); } else out.push(n); };
  const re = /<!--[\s\S]*?-->|<\/([A-Za-z][\w:-]*)\s*>|<([A-Za-z][\w:-]*)((?:\s+[^\s=>\/]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?)*)\s*(\/?)>|([^<]+)|</g;
  let t;
  while ((t = re.exec(src)) !== null) {
    if (t[0] === "") break;
    if (t[5] !== undefined) { if (t[5]) push(new Text(decode(t[5]))); continue; }
    if (t[1]) { const tag = t[1].toLowerCase(); for (let i = stack.length - 1; i >= 0; i--) if (stack[i].tag === tag) { stack.length = i; break; } continue; }
    if (t[2]) {
      const attrs = {};
      for (const a of t[3].matchAll(/([^\s=\/>]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g)) attrs[a[1]] = decode(a[2] !== undefined ? a[2] : a[3] !== undefined ? a[3] : a[4] !== undefined ? a[4] : "");
      const el = new El(t[2], attrs); push(el);
      if (!t[4] && !VOID.has(el.tag)) stack.push(el);
    }
  }
  return out;
}

// The selectors the page uses: tag, #id, .class, [attr="v"], :checked, and
// the descendant combinator. No commas, no child or sibling combinators.
const matchCompound = (el, c) => {
  const tag = (c.match(/^[a-zA-Z][\w-]*/) || [""])[0];
  if (tag && el.tag !== tag.toLowerCase()) return false;
  for (const p of c.slice(tag.length).matchAll(/#([\w-]+)|\.([\w-]+)|\[([\w-]+)(?:=("[^"]*"|'[^']*'|[^\]]+))?\]|:(\w+)/g)) {
    if (p[1] !== undefined && el.id !== p[1]) return false;
    if (p[2] !== undefined && !el.classList.contains(p[2])) return false;
    if (p[3] !== undefined) { if (!(p[3] in el.attrs)) return false; if (p[4] !== undefined && el.attrs[p[3]] !== p[4].replace(/^["']|["']$/g, "")) return false; }
    if (p[5] !== undefined) { if (p[5] === "checked") { if (!el.checked) return false; } else throw new Error("the stub does not know :" + p[5]); }
  }
  return true;
};
const matches = (el, sel) => {
  const parts = sel.trim().split(/\s+/);
  if (!matchCompound(el, parts[parts.length - 1])) return false;
  let n = el.parent;
  for (let i = parts.length - 2; i >= 0; i--) { while (n && !matchCompound(n, parts[i])) n = n.parent; if (!n) return false; n = n.parent; }
  return true;
};

let scrolled = [];
// a fresh page: the body's markup parsed, the script run against it on the given store, at the given hash
function openPage(store, hash) {
  const body = new El("body"); body.innerHTML = bodyMarkup;
  let h = hash || "", listeners = {}, scrolledTop = 0;
  const window = { scrollTo: () => { scrolledTop++; }, addEventListener: (t, fn) => { (listeners[t] = listeners[t] || []).push(fn); } };
  const location = { get hash() { return h; }, set hash(v) { v = String(v); if (v && v[0] !== "#") v = "#" + v; if (v === h) return; h = v; for (const fn of listeners.hashchange || []) fn({ type: "hashchange" }); } };
  const document = { getElementById: (id) => body.all().find((e) => e.id === id) || null, title: "" };
  const sandbox = { console, document, window, location,
    localStorage: { getItem: (k) => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); }, removeItem: (k) => { delete store[k]; } } };
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);
  // BOOK is a const, so it is read as the script's last expression, as tools/check.js reads it
  const B = vm.runInContext(m[1] + "\nBOOK", sandbox, { filename: "index.html" });
  return { body, B, doc: document, loc: location, go: (to) => { location.hash = to; }, scrolledTop: () => scrolledTop, $: document.getElementById };
}

// ---- the reader's hands ----

const click = (el) => el.dispatch("click");
const texts = (els) => els.map((e) => e.textContent);
const stored = (store, k) => (k in store ? JSON.parse(store[k]) : undefined);
// a radio picked: the others of its name let go, as a browser does
const pick = (form, name, value) => { for (const r of form.querySelectorAll(`input[name="${name}"]`)) r.checked = r.attrs.value === String(value); };
const submit = (form) => form.dispatch("submit");
const norm = (s) => { const d = new El("div"); d.innerHTML = s; return d.innerHTML; };
const defaults = (c) => Object.fromEntries(c.inputs.map((i) => [i[0], i[2]]));
const asStore = (B) => ({ fmt: B.fmt, FIG: B.FIG });

const store = {};
let page;
try { page = openPage(store, ""); } catch (e) {
  fail("the page did not boot: " + (e.stack || e).toString().split("\n").slice(0, 3).join(" | "));
  console.log(checks + " checks, " + fails + " failures"); process.exit(1);
}
let { body, B, doc, go, $ } = page;
if (!B) { fail("the script did not export BOOK"); console.log(checks + " checks, " + fails + " failures"); process.exit(1); }
const { LESSONS, EXAMS, CARDS, GLOSSARY, READING, RULES, CALIBRATION, SESSION_FIELDS, SITE, PARTS, fmt, FIG, firstSentence } = B;
const main = () => $("main"), side = () => $("side");
const h2 = () => { const h = main().querySelector("h2"); return h ? h.textContent : ""; };
const lessonLinks = (el) => el.querySelectorAll("a").map((a) => a.href).filter((h) => h.startsWith("#/lesson/"));
const lessonOf = (href) => href.replace(/^#\/lesson\//, "").split("#")[0];

// ---- the page as it opens, with no hash and nothing saved ----
{
  if (h2() !== SITE.tagline) fail("the page did not open on the home view: " + h2());
  if (doc.title !== SITE.title) fail("the home view's title is " + doc.title);
  const road = main().querySelectorAll("ol.roadmap li");
  if (road.length !== LESSONS.length) fail("the home view lists " + road.length + " lessons of " + LESSONS.length);
  road.forEach((li, i) => { const l = LESSONS[i]; const a = li.querySelector("a");
    if (!a || a.href !== "#/lesson/" + l.id) fail("the home view's row " + (i + 1) + " does not link to Lesson " + l.id);
    const small = li.querySelector("small"); if (!small || small.textContent !== firstSentence(l.question)) fail("Lesson " + l.id + "'s row does not carry the first sentence of its question");
    if (li.querySelector(".exam-score").textContent !== "" || li.textContent.includes("read ")) fail("Lesson " + l.id + "'s row shows a score or a read mark on a fresh store"); });
  if (!main().querySelector(".scorecard") || !main().querySelector(".scorecard").textContent.startsWith("No exams marked yet")) fail("a fresh scorecard does not say no exams marked yet");
  if (!main().querySelector("figure svg")) fail("the home view has no figure");
  const sideLinks = lessonLinks(side());
  if (sideLinks.length !== LESSONS.length) fail("the sidebar lists " + sideLinks.length + " lessons of " + LESSONS.length);
  if (side().querySelector(".now") || side().querySelector(".sideparts")) fail("the sidebar lights a lesson on the home view");
  if (page.scrolledTop() !== 1) fail("opening the page did not scroll to the top");
  ok();
}

// ---- every static view ----
const views = {
  start: () => { const lis = main().querySelectorAll("#start-form li"); if (lis.length !== CALIBRATION.questions.length + 1) fail("the start page asks " + lis.length + " questions, not " + (CALIBRATION.questions.length + 1));
    if (!$("start-rec") || !$("start-rec").hidden) fail("the start page's suggestion is showing before the form is sent");
    if (main().querySelectorAll(".track-btn").length !== 2) fail("the start page does not offer both tracks"); if (!main().querySelector("figure svg")) fail("the start page has no figure"); },
  leaders: () => { const lis = main().querySelectorAll("ol.leaders li"); if (lis.length !== LESSONS.length) fail("the leaders page carries " + lis.length + " questions of " + LESSONS.length);
    lis.forEach((li, i) => { if (!li.textContent.includes(LESSONS[i].business.replace(/\*\*|`/g, "").slice(0, 40))) fail("the leaders page's entry " + (i + 1) + " is not Lesson " + LESSONS[i].id + "'s business question"); }); },
  case: () => { if (!h2().startsWith("The case: " + B.CASE.name)) fail("the case page's heading: " + h2()); if (!main().querySelector("figure svg")) fail("the case page has no figure"); },
  rules: () => { if (main().querySelectorAll(".rule").length !== RULES.length) fail("the rules page carries " + main().querySelectorAll(".rule").length + " rules of " + RULES.length); },
  cards: () => { const cs = main().querySelectorAll(".card"); if (cs.length !== CARDS.length) fail("the cards page carries " + cs.length + " cards of " + CARDS.length);
    cs.forEach((c, i) => { if (c.id !== "card-" + CARDS[i].id) fail("card " + (i + 1) + " has id " + c.id); if (!c.querySelector(`a[href="#/lesson/${CARDS[i].lesson}"]`)) fail("card " + CARDS[i].id + " does not link to Lesson " + CARDS[i].lesson); if (c.querySelectorAll("li").length !== CARDS[i].lines.length) fail("card " + CARDS[i].id + " does not carry all its lines"); }); },
  glossary: () => { if (main().querySelectorAll("dt").length !== GLOSSARY.length) fail("the glossary carries " + main().querySelectorAll("dt").length + " entries of " + GLOSSARY.length); },
  reading: () => { const lis = main().querySelectorAll("ol li"); if (lis.length !== READING.length) fail("the reading page carries " + lis.length + " entries of " + READING.length);
    // the entry's own links come last; a Lesson mention in its reason links too, since every mention does
    lis.forEach((li, i) => { const ids = lessonLinks(li).map(lessonOf).slice(-READING[i].lessons.length); if (ids.join() !== READING[i].lessons.join()) fail("reading entry " + (i + 1) + " links Lessons " + ids.join(", ") + ", not " + READING[i].lessons.join(", ")); }); },
  session: () => { const tas = main().querySelectorAll("textarea"); if (tas.length !== SESSION_FIELDS.length) fail("the session page has " + tas.length + " fields of " + SESSION_FIELDS.length);
    if (!$("s-build") || !$("s-clear") || !$("s-out")) fail("the session page lacks its buttons or its output"); }
};
for (const v of Object.keys(views)) {
  try {
    go("#/" + v);
    if (!h2()) fail(v + ": no heading"); if (doc.title !== SITE.title) fail(v + ": the title is " + doc.title);
    views[v]();
    for (const href of lessonLinks(main())) if (!LESSONS.some((l) => l.id === lessonOf(href))) fail(v + " links to " + href + ", which is no lesson");
    if (side().querySelector(".now")) fail(v + ": the sidebar lights a lesson");
    ok();
  } catch (e) { fail(v + ": " + (e.stack || e).toString().split("\n").slice(0, 3).join(" | ")); }
}
// a route that is nothing, and a lesson that is not one, both land on the home view
try {
  go("#/nothing-here"); if (h2() !== SITE.tagline) fail("an unknown route did not land on the home view: " + h2());
  go("#/lesson/zz"); if (h2() !== SITE.tagline) fail("an unknown lesson did not land on the home view: " + h2());
  ok();
} catch (e) { fail("an unknown route: " + (e.stack || e).toString().split("\n").slice(0, 3).join(" | ")); }

// ---- every lesson, straight in: the parts, the calculator, the figure, the answer, the exam, the mark ----
let expectedTotal = 0;
LESSONS.forEach((l, li) => {
  const where = "Lesson " + l.id;
  try {
    go("#/lesson/" + l.id.toLowerCase()); // the hash may carry the id in either case
    if (h2() !== l.id + ". " + l.title) fail(where + ": the heading is " + h2());
    if (doc.title !== "Lesson " + l.id + " — " + SITE.title) fail(where + ": the title is " + doc.title);
    if (!main().querySelector(".track") || !main().querySelector(".track").textContent.includes("straight in")) fail(where + ": the track line does not say straight in");
    if ($("part-0")) fail(where + ": the words-first page shows on the straight-in track");
    PARTS.forEach((p, i) => { const s = $("part-" + (i + 1)); if (!s || !s.querySelector("h3") || s.querySelector("h3").textContent !== (i + 1) + ". " + p[1]) fail(where + ": part " + (i + 1) + " (" + p[1] + ") is missing or misheaded"); });
    if (!$("part-10") || !$("part-10").classList.contains("exam")) fail(where + ": the exam is not part 10");
    if (!$("part-1").querySelector(".business") || !$("part-1").querySelector(".business").textContent.startsWith("The business question.")) fail(where + ": the business question does not open part 1");
    if (main().querySelectorAll("ul.parts a").length !== PARTS.length + 1) fail(where + ": the parts list does not carry ten links");
    for (const href of lessonLinks(main())) if (!LESSONS.some((x) => x.id === lessonOf(href))) fail(where + " links to " + href + ", which is no lesson");
    // the sidebar lights this lesson and opens its ten parts under it
    const now = side().querySelector(".now");
    if (!now || !now.querySelector("a") || now.querySelector("a").href !== "#/lesson/" + l.id) fail(where + ": the sidebar does not light it");
    else if (now.querySelectorAll(".sideparts a").length !== PARTS.length + 1) fail(where + ": the sidebar does not open its ten parts");
    // the pager: the lesson before and the one after, or the lessons page and the session note at the ends
    const pager = main().querySelector(".pager"); const pl = pager ? pager.querySelectorAll("a").map((a) => a.href) : [];
    if (pl[0] !== (li ? "#/lesson/" + LESSONS[li - 1].id : "#/") || pl[1] !== (li + 1 < LESSONS.length ? "#/lesson/" + LESSONS[li + 1].id : "#/session")) fail(where + ": the pager points at " + pl.join(" and "));
    // the calculator at its defaults: every output is the calculator's own figure, the example's figure is among them, and the figure is drawn from the same numbers
    const calc = $("part-5").querySelector(".calc"); const c = l.calc;
    if (!calc) throw new Error("no calculator in part 5");
    const inputs = calc.querySelectorAll("input");
    if (inputs.length !== c.inputs.length) fail(where + ": the calculator shows " + inputs.length + " inputs of " + c.inputs.length);
    const d = defaults(c), r0 = c.compute(d);
    const outs = () => calc.querySelectorAll(".out b").map((b) => b.textContent);
    const want = (r) => c.outputs.map((o) => fmt(r[o[0]], o[2]));
    if (outs().join("|") !== want(r0).join("|")) fail(where + ": at the defaults the calculator shows " + outs().join(" ") + ", not " + want(r0).join(" "));
    for (const k of Object.keys(c.expect)) { const o = c.outputs.find((x) => x[0] === k); if (!outs().includes(fmt(c.expect[k], o[2]))) fail(where + ": the example's " + k + " is not among the outputs shown"); }
    if (c.verdictKey && calc.querySelector(".verdict").textContent !== r0[c.verdictKey]) fail(where + ": the verdict shown is not the calculator's");
    const fig = $("part-5").querySelector(`figure[data-fig="${l.id}"]`);
    if (!fig || !fig.querySelector("svg")) fail(where + ": part 5 has no live figure");
    else {
      if (norm(fig.querySelector(".fig-svg").innerHTML) !== norm(FIG.render(l.figure.draw(d, r0), l.figure.title))) fail(where + ": the figure at the defaults is not drawn from the calculator");
      if (!fig.querySelector("figcaption").textContent.startsWith(l.figure.title)) fail(where + ": the figure's caption does not open with its title");
    }
    // a changed input: the outputs and the figure follow it, as the page promises. Each number
    // input in turn is moved seven steps within its range and put back; one that moves no
    // output at the displayed decimals (Lesson K's n1) proves nothing, and one that moves the
    // outputs but not the picture (Lesson N's p0: its mosaics are fixed numbers, as the caption
    // says) proves only the outputs. The check stops when both have been seen to follow.
    const fig0 = fig ? norm(fig.querySelector(".fig-svg").innerHTML) : null;
    let outsMoved = false, figMoved = false;
    for (const num of inputs.filter((i) => i.type === "number")) {
      if (outsMoved && (figMoved || !fig)) break;
      const spec = c.inputs.find((i) => i[0] === num.dataset.key); const v = { ...d };
      const step = spec[5] || 1, up = Math.min(spec[4], spec[2] + step * 7); v[spec[0]] = up === spec[2] ? Math.max(spec[3], spec[2] - step * 7) : up;
      if (v[spec[0]] === spec[2]) continue;
      let r1; try { r1 = c.compute(v); } catch (e) { r1 = {}; }
      // a figure that cannot be drawn for the inputs (Lesson B's k past n) says so in its place
      let expectFig = null; if (fig) { try { expectFig = norm(FIG.render(l.figure.draw(v, r1), l.figure.title)); } catch (e) { expectFig = norm(`<p class="mute">The figure cannot be drawn for these inputs.</p>`); } }
      const movesOuts = want(r1).join("|") !== want(r0).join("|"), movesFig = fig && expectFig !== fig0;
      if (!movesOuts && !movesFig) continue;
      num.value = v[spec[0]]; num.dispatch("input");
      if (outs().join("|") !== want(r1).join("|")) fail(where + ": after " + spec[0] + " = " + v[spec[0]] + " the calculator shows " + outs().join(" ") + ", not " + want(r1).join(" "));
      if (fig && norm(fig.querySelector(".fig-svg").innerHTML) !== expectFig) fail(where + ": the figure did not follow " + spec[0] + " = " + v[spec[0]]);
      if (c.verdictKey && calc.querySelector(".verdict").textContent !== r1[c.verdictKey]) fail(where + ": the verdict did not follow " + spec[0] + " = " + v[spec[0]]);
      outsMoved = outsMoved || movesOuts; figMoved = figMoved || movesFig;
      num.value = spec[2]; num.dispatch("input");
    }
    if (!outsMoved) fail(where + ": no number input moves an output at its displayed decimals, so the live calculator is unproven");
    if (fig && !figMoved) fail(where + ": no number input moves the figure, so the live figure is unproven");
    if (outs().join("|") !== want(r0).join("|")) fail(where + ": the inputs put back did not bring the outputs back");
    // the diagnostic's answer: hidden, shown, hidden again
    const btn = $("part-8").querySelector(".reveal-btn"), ans = $("ans-" + l.id);
    if (!btn || !ans) fail(where + ": the diagnostic has no answer to show");
    else {
      if (!ans.hidden || btn.textContent !== "Show an answer") fail(where + ": the answer shows before it is asked for");
      click(btn); if (ans.hidden || btn.textContent !== "Hide the answer" || btn.getAttribute("aria-expanded") !== "true") fail(where + ": Show an answer did not show it");
      if (ans.textContent.trim().length < 40) fail(where + ": the answer shown is thin: " + ans.textContent);
      click(btn); if (!ans.hidden || btn.textContent !== "Show an answer") fail(where + ": Hide the answer did not hide it");
    }
    // the exam: nothing picked marks every question unanswered and quotes the answer; then every answer right passes and the best is kept
    const ex = EXAMS[l.id], form = $("exam-form"), score = $("exam-score");
    if (!form || form.querySelectorAll("li").length !== ex.length) throw new Error("the exam does not carry its " + ex.length + " questions");
    ex.forEach((x, i) => { if (form.querySelectorAll(`input[name="q${i}"]`).length !== x.o.length) fail(where + ": question " + (i + 1) + " offers " + form.querySelectorAll(`input[name="q${i}"]`).length + " answers of " + x.o.length); });
    if (score.textContent !== "") fail(where + ": the exam shows a score before it is marked");
    submit(form);
    if (score.textContent !== "0 of " + ex.length + ". Best: 0 of " + ex.length + ".") fail(where + ": an unanswered exam marks as " + score.textContent);
    const reason = (x) => x.why.replace(/`|\*\*|\*/g, "").slice(0, 30);
    ex.forEach((x, i) => { const q = form.querySelector(`li[data-q="${i}"]`), why = q.querySelector(".why");
      if (!q.classList.contains("wrong") || why.hidden || !why.textContent.startsWith("Unanswered.") || !why.textContent.includes(x.o[x.a].replace(/`|\*\*/g, "")) || !why.textContent.includes(reason(x))) fail(where + ": an unanswered question " + (i + 1) + " does not say so, quote the answer and give the reason: " + why.textContent.slice(0, 80)); });
    let rec = stored(store, "asai:exams"); if (!rec || !rec[l.id] || rec[l.id].best !== 0 || rec[l.id].attempts !== 1) fail(where + ": the unanswered attempt was not kept: " + JSON.stringify(rec && rec[l.id]));
    ex.forEach((x, i) => pick(form, "q" + i, x.a));
    submit(form);
    if (score.textContent !== ex.length + " of " + ex.length + " — passed. Best: " + ex.length + " of " + ex.length + ".") fail(where + ": every answer right marks as " + score.textContent);
    ex.forEach((x, i) => { const q = form.querySelector(`li[data-q="${i}"]`), why = q.querySelector(".why");
      if (!q.classList.contains("right") || q.classList.contains("wrong") || why.hidden || !why.textContent.startsWith("Right.") || !why.textContent.includes(reason(x))) fail(where + ": a right answer to question " + (i + 1) + " is not marked right with its reason: " + why.textContent.slice(0, 80)); });
    rec = stored(store, "asai:exams"); if (!rec[l.id] || rec[l.id].best !== ex.length || rec[l.id].attempts !== 2 || rec[l.id].last !== ex.length) fail(where + ": the pass was not kept as the best: " + JSON.stringify(rec[l.id]));
    expectedTotal += ex.length;
    // the pass mark is three of four or better: one wrong passes, two wrong does not, and the best stays
    const wrong = (i) => (ex[i].a + 1) % ex[i].o.length;
    ex.forEach((x, i) => pick(form, "q" + i, i === 0 ? wrong(0) : x.a));
    submit(form);
    if (score.textContent !== (ex.length - 1) + " of " + ex.length + " — passed. Best: " + ex.length + " of " + ex.length + ".") fail(where + ": one wrong of " + ex.length + " marks as " + score.textContent);
    const w0 = form.querySelector('li[data-q="0"] .why'), q0 = form.querySelector('li[data-q="0"]');
    if (!q0.classList.contains("wrong") || q0.classList.contains("right") || !w0.textContent.startsWith("Not this one.") || !w0.textContent.includes(ex[0].o[ex[0].a].replace(/`|\*\*/g, "")) || !w0.textContent.includes(reason(ex[0]))) fail(where + ": a wrong answer is not marked wrong with the right one quoted and the reason: " + w0.textContent.slice(0, 80));
    pick(form, "q1", wrong(1));
    submit(form);
    if (score.textContent !== (ex.length - 2) + " of " + ex.length + ". Best: " + ex.length + " of " + ex.length + ".") fail(where + ": two wrong of " + ex.length + " marks as " + score.textContent);
    rec = stored(store, "asai:exams"); if (rec[l.id].best !== ex.length || rec[l.id].attempts !== 4 || rec[l.id].last !== ex.length - 2) fail(where + ": the later attempts did not keep the best: " + JSON.stringify(rec[l.id]));
    // the mark-read button
    const md = $("mark-done"); if (!md) fail(where + ": no mark-read button"); else { click(md); if ($("done-msg").textContent !== "Marked.") fail(where + ": marking read did not say so"); }
    if (!(stored(store, "asai:done") || []).includes(l.id)) fail(where + ": marking read was not kept");
    ok();
  } catch (e) { fail(where + ": " + (e.stack || e).toString().split("\n").slice(0, 3).join(" | ")); }
});

// ---- the home view after the exams: every row scored and read, and the scorecard adds up ----
try {
  go("#/");
  const road = main().querySelectorAll("ol.roadmap li");
  road.forEach((li, i) => { const l = LESSONS[i], n = EXAMS[l.id].length, es = li.querySelector(".exam-score");
    if (es.textContent !== "exam " + n + "/" + n || !es.classList.contains("pass")) fail("Lesson " + l.id + "'s row does not show its pass: " + es.textContent + " / " + es.className);
    if (!li.querySelector(".done").textContent.startsWith("read")) fail("Lesson " + l.id + "'s row does not show it read"); });
  const sc = main().querySelector(".scorecard").textContent;
  if (!sc.includes(expectedTotal + " of " + expectedTotal + " across " + LESSONS.length + " exams taken; " + LESSONS.length + " passed") || !sc.includes("0 not yet taken")) fail("the scorecard does not add up: " + sc);
  if (side().querySelectorAll(".done").length !== LESSONS.length) fail("the sidebar does not tick every lesson read");
  ok();
} catch (e) { fail("the home view after the exams: " + (e.stack || e).toString().split("\n").slice(0, 3).join(" | ")); }

// ---- the fragment: a part named in the hash is scrolled to ----
try {
  scrolled = []; go("#/lesson/C#part-3");
  if (scrolled[scrolled.length - 1] !== "part-3") fail("a hash naming part 3 did not scroll to it: " + scrolled.join(", "));
  if (h2() !== "C. " + LESSONS[2].title) fail("the fragment route did not open Lesson C");
  ok();
} catch (e) { fail("the fragment: " + (e.stack || e).toString().slice(0, 300)); }

// ---- the track: the toggle on a lesson switches it, and every lesson's words-first page carries its words and its figure in words ----
try {
  go("#/lesson/A");
  click(main().querySelector(".track-toggle"));
  if (stored(store, "asai:track") !== "gentle") fail("the track toggle did not save words first");
  if (!main().querySelector(".track").textContent.includes("words first")) fail("after the toggle the track line does not say words first");
  LESSONS.forEach((l) => {
    const where = "Lesson " + l.id + ", words first";
    go("#/lesson/" + l.id);
    const g = $("part-0");
    if (!g || !g.classList.contains("gentle")) { fail(where + ": no words-first page"); return; }
    if (main().querySelectorAll("section").indexOf(g) !== 0) fail(where + ": the words-first page is not first");
    const plain = l.gentle.replace(/\*\*|\*/g, "").split(/\n\s*\n/)[0];
    if (!g.textContent.includes(plain.slice(0, 60))) fail(where + ": the page does not carry the lesson's words");
    if (g.querySelector("code")) fail(where + ": the words-first page carries notation");
    const fig = g.querySelector("figure");
    if (!fig || !fig.querySelector("svg")) fail(where + ": the words-first page has no figure");
    else { if (!fig.querySelector("figcaption").textContent.includes(l.figure.gentle.replace(/\*\*|\*/g, "").slice(0, 60))) fail(where + ": the figure's caption is not the one in words"); if (fig.attrs["data-fig"]) fail(where + ": the words-first figure is the live one, so it would move with the calculator"); }
    if (!$("part-9")) fail(where + ": the nine parts do not follow");
  });
  go("#/lesson/A"); click(main().querySelector(".track-toggle"));
  if (stored(store, "asai:track") !== "standard" || $("part-0")) fail("the toggle did not switch back to straight in");
  ok();
} catch (e) { fail("the track: " + (e.stack || e).toString().split("\n").slice(0, 3).join(" | ")); }

// ---- the start page: a low score suggests words first, a full score straight in, and the buttons set the track ----
try {
  const c = CALIBRATION, q = c.questions;
  go("#/start");
  let form = $("start-form");
  q.forEach((x, i) => pick(form, "q" + i, (x.a + 1) % x.o.length)); pick(form, "self", 0);
  scrolled = []; submit(form);
  const rec = $("start-rec");
  if (rec.hidden || !rec.textContent.startsWith("0 of " + q.length + ".")) fail("a start form with every answer wrong reads: " + rec.textContent.slice(0, 60));
  if (!rec.textContent.includes(c.verdict.gentle.replace(/\*\*|\*/g, "").slice(0, 40))) fail("a low score did not bring the words-first verdict");
  if (scrolled[scrolled.length - 1] !== "start-rec") fail("the suggestion was not scrolled to");
  let btns = rec.querySelectorAll(".track-btn");
  if (btns.length !== 2 || btns[0].dataset.track !== "gentle" || btns[0].textContent !== "Words first") fail("a low score does not offer words first first: " + texts(btns).join(" | "));
  let cal = stored(store, "asai:calib"); if (!cal || cal.score !== 0 || cal.wordsFirst !== false) fail("the low score was not kept: " + JSON.stringify(cal));
  click(btns[0]);
  if (stored(store, "asai:track") !== "gentle" || h2() !== SITE.tagline) fail("the words-first button did not set the track and go home");
  if (!main().querySelector(".track").textContent.includes("words first")) fail("the home view's track line does not say words first");
  go("#/start"); form = $("start-form");
  if (!main().textContent.includes("Last time: 0 of " + q.length)) fail("the start page does not remember the last score");
  q.forEach((x, i) => pick(form, "q" + i, x.a)); pick(form, "self", c.self.gentleAt);
  submit(form);
  if ($("start-rec").hidden || !$("start-rec").textContent.startsWith(q.length + " of " + q.length + ", and words first.")) fail("a full score with words first asked reads: " + $("start-rec").textContent.slice(0, 60));
  cal = stored(store, "asai:calib"); if (cal.score !== q.length || cal.wordsFirst !== true) fail("the self-report was not kept: " + JSON.stringify(cal));
  btns = $("start-rec").querySelectorAll(".track-btn"); if (btns[0].dataset.track !== "gentle") fail("words first asked for is not offered first");
  // the pass mark itself: one short of it suggests words first, reaching it suggests straight in
  const scoring = (n) => q.forEach((x, i) => pick(form, "q" + i, i < n ? x.a : (x.a + 1) % x.o.length));
  scoring(c.passAt - 1); pick(form, "self", 0); submit(form);
  if (!$("start-rec").textContent.startsWith((c.passAt - 1) + " of " + q.length + ".") || $("start-rec").querySelectorAll(".track-btn")[0].dataset.track !== "gentle") fail("one short of the pass mark does not suggest words first: " + $("start-rec").textContent.slice(0, 60));
  scoring(c.passAt); pick(form, "self", 0); submit(form);
  if (!$("start-rec").textContent.startsWith(c.passAt + " of " + q.length + ".") || $("start-rec").querySelectorAll(".track-btn")[0].dataset.track !== "standard") fail("the pass mark does not suggest straight in: " + $("start-rec").textContent.slice(0, 60));
  q.forEach((x, i) => pick(form, "q" + i, x.a)); pick(form, "self", 0);
  submit(form);
  btns = $("start-rec").querySelectorAll(".track-btn");
  if (!$("start-rec").textContent.startsWith(q.length + " of " + q.length + ".") || btns[0].dataset.track !== "standard" || btns[0].textContent !== "Straight in") fail("a full score does not offer straight in first: " + $("start-rec").textContent.slice(0, 60));
  if (!$("start-rec").textContent.includes(c.verdict.standard.replace(/\*\*|\*/g, "").slice(0, 40))) fail("a full score did not bring the straight-in verdict");
  click(btns[0]);
  if (stored(store, "asai:track") !== "standard" || h2() !== SITE.tagline) fail("the straight-in button did not set the track and go home");
  ok();
} catch (e) { fail("the start page: " + (e.stack || e).toString().split("\n").slice(0, 3).join(" | ")); }

// ---- the session note: typed, built, kept, cleared ----
try {
  go("#/session");
  const tas = main().querySelectorAll("textarea");
  tas.forEach((t, i) => { t.value = "line " + (i + 1); t.dispatch("input"); });
  const saved = stored(store, "asai:session");
  if (!saved || SESSION_FIELDS.some((f, i) => saved[f[0]] !== "line " + (i + 1))) fail("typing in the session note was not kept: " + JSON.stringify(saved));
  click($("s-build"));
  const out = $("s-out").textContent.split("\n");
  if (out.length !== SESSION_FIELDS.length || SESSION_FIELDS.some((f, i) => out[i] !== f[1] + ": line " + (i + 1))) fail("the note built reads: " + $("s-out").textContent);
  click($("s-clear"));
  if (tas.some((t) => t.value !== "") || JSON.stringify(stored(store, "asai:session")) !== "{}" || $("s-out").textContent !== "") fail("Clear did not clear the note");
  tas.forEach((t, i) => { t.value = "kept " + (i + 1); t.dispatch("input"); });
  ok();
} catch (e) { fail("the session note: " + (e.stack || e).toString().split("\n").slice(0, 3).join(" | ")); }

// ---- the page reopened on the same browser: the scores, the marks, the track and the note are still there ----
try {
  go("#/lesson/A"); click(main().querySelector(".track-toggle")); // left on words first, so the reopen has a track to remember
  page = openPage(store, "#/lesson/B"); ({ body, B, doc, go, $ } = page);
  if (h2() !== "B. " + LESSONS[1].title) fail("reopening on a lesson's hash did not open it: " + h2());
  if (!main().querySelector(".track").textContent.includes("words first") || !$("part-0")) fail("a reopened page forgot the track");
  click(main().querySelector(".track-toggle"));
  if (!main().textContent.includes("Best so far: " + EXAMS.B.length + " of " + EXAMS.B.length + " in 4 attempts")) fail("a reopened lesson does not show its best score");
  if (!side().querySelector(".now .done")) fail("a reopened page does not tick the lesson read");
  go("#/");
  const sc = main().querySelector(".scorecard").textContent;
  if (!sc.includes(expectedTotal + " of " + expectedTotal + " across " + LESSONS.length + " exams taken")) fail("a reopened page lost the scorecard: " + sc);
  go("#/session");
  const tas = main().querySelectorAll("textarea");
  if (SESSION_FIELDS.some((f, i) => tas[i].value !== "kept " + (i + 1))) fail("a reopened session note lost its lines: " + texts(tas).join(" | "));
  // a store the page cannot read falls back, and never throws
  store["asai:track"] = "{not json"; store["asai:exams"] = "[1,";
  page = openPage(store, "#/lesson/A"); ({ body, B, doc, go, $ } = page);
  if (h2() !== "A. " + LESSONS[0].title || !main().querySelector(".track").textContent.includes("straight in")) fail("a corrupt store did not fall back to the defaults");
  ok();
} catch (e) { fail("the reopened page: " + (e.stack || e).toString().split("\n").slice(0, 3).join(" | ")); }

console.log(checks + " checks, " + fails + " failures");
process.exit(fails ? 1 : 0);
