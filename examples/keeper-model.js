#!/usr/bin/env node
// The keeper model: a small logistic regression on Reference Set 2 that
// gives each frame a probability of being kept, checked on outings it never
// saw. It is the worked example behind examples/keeper-model.md, a delegate
// model that a language model built and trained on the photographer's own
// decisions. No dependencies; runs on the Node that ships with the CI runner.
//
//   node examples/keeper-model.js           prints the report
//   node examples/keeper-model.js --check   also checks the write-up quotes
//                                           every figure this run produces
"use strict";
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const lines = fs.readFileSync(path.join(root, "data", "reference-set-2.csv"), "utf8").trim().split(/\r?\n/);
const head = lines[0].split(",");
const rows = lines.slice(1).map(l => Object.fromEntries(l.split(",").map((v, i) => [head[i], v])));
const n = rows.length;
const y = rows.map(r => (r.published === "1" || r.master === "1") ? 1 : 0);
const outing = rows.map(r => r.outing);
const outings = [...new Set(outing)].sort();

// ---- features --------------------------------------------------------
// ISO is blank on some rows: fill with the median ISO and carry a flag, so
// the model can tell a filled value from a recorded one.
const isos = rows.filter(r => r.iso).map(r => +r.iso).sort((a, b) => a - b);
const isoMedian = isos[Math.floor(isos.length / 2)];
const isoMissing = rows.filter(r => !r.iso).length;
const raw = rows.map(r => [
  Math.log(r.iso ? +r.iso : isoMedian), Math.log(+r.shutter_s), Math.log(+r.focal_mm),
  +r.aperture, +r.sharpness, +r.brightness, r.iso ? 0 : 1,
]);
// A keeper is chosen as the best of its group, so each frame's standing
// within its own outing goes in beside the raw sharpness and brightness.
const pct = (col) => {
  const out = new Array(n);
  for (const o of outings) {
    const idx = [...Array(n).keys()].filter(i => outing[i] === o);
    idx.sort((a, b) => raw[a][col] - raw[b][col] || a - b);
    idx.forEach((i, rank) => { out[i] = rank / Math.max(1, idx.length - 1); });
  }
  return out;
};
const sharpPct = pct(4), brightPct = pct(5);
const X = raw.map((f, i) => [...f, sharpPct[i], brightPct[i]]);
const d = X[0].length;

// ---- logistic regression, L2 penalty, intercept unpenalised ----------
// Minimises 0.5·|w|² + C·Σ log-loss on standardised features by Newton's
// method, which converges to the exact optimum, so every run is identical.
// No class weighting: re-weighting would distort the probabilities, and the
// point here is a probability that can be checked.
const C = 1.0;
function solve(A, b) {
  const m = b.length, M = A.map((r, i) => [...r, b[i]]);
  for (let c = 0; c < m; c++) {
    let p = c; for (let r = c + 1; r < m; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
    [M[c], M[p]] = [M[p], M[c]];
    for (let r = 0; r < m; r++) if (r !== c) { const k = M[r][c] / M[c][c]; for (let j = c; j <= m; j++) M[r][j] -= k * M[c][j]; }
  }
  return M.map((r, i) => r[m] / r[i]);
}
const sigmoid = (z) => 1 / (1 + Math.exp(-z));
function fit(train) {
  const mean = new Array(d).fill(0), sd = new Array(d).fill(0);
  for (const i of train) X[i].forEach((v, j) => { mean[j] += v; });
  mean.forEach((_, j) => { mean[j] /= train.length; });
  for (const i of train) X[i].forEach((v, j) => { sd[j] += (v - mean[j]) ** 2; });
  sd.forEach((_, j) => { sd[j] = Math.sqrt(sd[j] / train.length) || 1; });
  const z = (i) => [1, ...X[i].map((v, j) => (v - mean[j]) / sd[j])];
  const Z = train.map(z);
  let w = new Array(d + 1).fill(0);
  for (let it = 0; it < 100; it++) {
    const g = w.map((v, j) => j === 0 ? 0 : v / C);
    const H = w.map((_, a) => w.map((_, b) => (a === b && a > 0) ? 1 / C : 0));
    Z.forEach((x, k) => {
      const p = sigmoid(x.reduce((s, v, j) => s + v * w[j], 0)), e = p - y[train[k]], q = p * (1 - p);
      for (let a = 0; a <= d; a++) { g[a] += e * x[a]; for (let b = 0; b <= d; b++) H[a][b] += q * x[a] * x[b]; }
    });
    const step = solve(H, g);
    w = w.map((v, j) => v - step[j]);
    if (Math.max(...step.map(Math.abs)) < 1e-10) break;
  }
  return (i) => sigmoid(z(i).reduce((s, v, j) => s + v * w[j], 0));
}

// ---- leave-one-outing-out: no frame is scored by a model that saw its outing
const p = new Array(n);
for (const o of outings) {
  const test = [], train = [];
  for (let i = 0; i < n; i++) (outing[i] === o ? test : train).push(i);
  const model = fit(train);
  for (const i of test) p[i] = model(i);
}

// ---- measures --------------------------------------------------------
const kept = y.reduce((a, b) => a + b, 0), base = kept / n;
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
function auc(score) { // Mann–Whitney, ties shared
  const idx = [...Array(n).keys()].sort((a, b) => score[a] - score[b]);
  const rank = new Array(n);
  for (let i = 0; i < n;) { let j = i; while (j + 1 < n && score[idx[j + 1]] === score[idx[i]]) j++;
    for (let k = i; k <= j; k++) rank[idx[k]] = (i + j) / 2 + 1; i = j + 1; }
  const rs = y.reduce((s, v, i) => s + (v ? rank[i] : 0), 0);
  return (rs - kept * (kept + 1) / 2) / (kept * (n - kept));
}
function averagePrecision(score) {
  const idx = [...Array(n).keys()].sort((a, b) => score[b] - score[a]);
  let tp = 0, ap = 0, prevRecall = 0;
  for (let i = 0; i < n;) { let j = i; while (j + 1 < n && score[idx[j + 1]] === score[idx[i]]) j++;
    for (let k = i; k <= j; k++) tp += y[idx[k]];
    const recall = tp / kept; ap += (recall - prevRecall) * tp / (j + 1); prevRecall = recall; i = j + 1; }
  return ap;
}
const brier = (q) => mean(y.map((v, i) => (q[i] - v) ** 2));
const order = [...Array(n).keys()].sort((a, b) => p[a] - p[b] || a - b);
const deciles = []; { let s = 0; for (let b = 0; b < 10; b++) { const len = Math.floor(n / 10) + (b < n % 10 ? 1 : 0); deciles.push(order.slice(s, s + len)); s += len; } }
const ece = deciles.reduce((e, b) => e + b.length / n * Math.abs(mean(b.map(i => p[i])) - mean(b.map(i => y[i]))), 0);
const top = order.slice(-Math.floor(n / 100));
function shortlist(score, k) { // keeps inside the top k% of their own outing
  let hit = 0;
  for (const o of outings) {
    const idx = [...Array(n).keys()].filter(i => outing[i] === o);
    if (!idx.some(i => y[i])) continue;
    idx.sort((a, b) => score[b] - score[a] || a - b);
    hit += idx.slice(0, Math.ceil(idx.length * k / 100)).reduce((s, i) => s + y[i], 0);
  }
  return hit;
}
const sharp = rows.map(r => +r.sharpness), bright = rows.map(r => +r.brightness);

// ---- report ----------------------------------------------------------
const pc = (x, dp) => (100 * x).toFixed(dp) + "%";
const R = {
  frames: n.toLocaleString("en"), kept, outings: outings.length, base: pc(base, 2), isoMissing: isoMissing.toLocaleString("en"),
  auc: auc(p).toFixed(2), ap: averagePrecision(p).toFixed(4), apChance: base.toFixed(4),
  brier: brier(p).toFixed(5), brierBase: brier(p.map(() => base)).toFixed(5),
  meanPred: pc(mean(p), 2), ece: ece.toFixed(5),
  topN: top.length, topPred: pc(mean(top.map(i => p[i])), 2), topKept: top.reduce((s, i) => s + y[i], 0),
  model5: shortlist(p, 5), model10: shortlist(p, 10), model20: shortlist(p, 20),
  sharp5: shortlist(sharp, 5), sharp10: shortlist(sharp, 10), sharp20: shortlist(sharp, 20),
  bright5: shortlist(bright, 5),
};
console.log(`frames ${R.frames}, kept ${R.kept} (${R.base}), outings ${R.outings}, ISO filled on ${R.isoMissing}`);
console.log(`ROC AUC ${R.auc}; average precision ${R.ap} against ${R.apChance} by chance`);
console.log(`Brier ${R.brier} against ${R.brierBase} for always predicting the base rate`);
console.log(`mean predicted ${R.meanPred} against ${R.base} observed; ECE over ten quantile bins ${R.ece}`);
deciles.forEach((b, i) => console.log(`  decile ${String(i + 1).padStart(2)}  predicted ${pc(mean(b.map(j => p[j])), 3)}  observed ${pc(mean(b.map(j => y[j])), 3)}  kept ${b.reduce((s, j) => s + y[j], 0)}`));
console.log(`top 1% (${R.topN} frames): predicted ${R.topPred}, kept ${R.topKept}`);
console.log(`per-outing shortlist, model:     top 5% ${R.model5}, top 10% ${R.model10}, top 20% ${R.model20} of ${kept}`);
console.log(`per-outing shortlist, sharpness: top 5% ${R.sharp5}, top 10% ${R.sharp10}, top 20% ${R.sharp20}; brightness top 5% ${R.bright5}`);

if (process.argv.includes("--check")) {
  // The write-up quotes these; a figure that drifts from the run fails here.
  const doc = fs.readFileSync(path.join(__dirname, "keeper-model.md"), "utf8");
  const quoted = {
    auc: R.auc, ap: R.ap, apChance: R.apChance, brier: R.brier, brierBase: R.brierBase, meanPred: R.meanPred,
    base: R.base, ece: R.ece, topN: `${R.topN} frames`, topPred: R.topPred,
    model5: `| 5% | ${R.model5} |`, model10: `| 10% | ${R.model10} |`, model20: `| 20% | ${R.model20} |`,
    sharp: `| ${R.sharp5} |`, frames: R.frames, isoMissing: R.isoMissing,
  };
  const missing = Object.entries(quoted).filter(([, v]) => !doc.includes(String(v)));
  if (missing.length) { console.error("keeper-model.md does not quote: " + missing.map(([k, v]) => `${k} ${v}`).join("; ")); process.exit(1); }
  console.log("ok: keeper-model.md quotes every figure this run produces");
}
