# Applied Statistics for AI Engineers

## Why Statistics Matters for AI Engineering

AI engineers make decisions based on evidence:

Is a new model actually better?
Is a prompt change meaningful?
Is an evaluation result reliable?
Do we have enough data to justify a release?

Without statistical reasoning, it is easy to mistake random variation for genuine improvement.

This tutorial teaches the practical statistical concepts needed for AI evaluation, experimentation, benchmarking, and evidence-based engineering decisions. The focus is not advanced mathematics, but helping engineers reason correctly about uncertainty, measurement, and model quality.

A course in applied statistics for people who evaluate and ship AI
systems, in one file. Open `index.html` in any browser — no server, no
build, no dependencies, no network — or read it as served from `main` at
https://dermot-r-cochran.github.io/applied-statistics-for-AI-engineers/ ,
which is the same file and nothing else. Progress and the session note
are kept in that browser's localStorage only.

## What it is

Evaluation metrics and confidence intervals, and the reasoning that goes
with them. It is not about any AI framework, library or product; it is
about the statistics that decide whether a number from an evaluation run
means what it is being read to mean. One question runs through every
lesson: **is this a real change in the system, or something else** —
sampling variation, sampling bias, measurement error, a change in the
test set, a change in the class mix, drift, or an aggregation that hides
the story?

It is written for an experienced engineer who has met probability and
statistics before and has practical responsibility for evaluation
harnesses, metric pipelines and release decisions. Foundations are
reactivated rather than taught from zero; every formula is derived far
enough to be re-derived; every assumption is stated; every worked
example is synthetic and says so, apart from one real companion dataset (see
**The case**, below).

## Two tracks

The start page asks four short calibration questions and one about
notation, and suggests a track. The **standard track** is each lesson's
nine parts, expert to expert. The **gentle track** is the same nine
parts with a plain-words page in front of each lesson first: the question
in everyday terms, the one idea, the worked example told in words with
the same numbers, an everyday version of it, and a picture of it. Nothing
is left out of the gentle track; it starts softer. The suggestion is only a suggestion, the track can be switched at
the top of any lesson, and either can be chosen without answering.

## The lessons

Fifteen, in the same nine parts each: the engineering question, the
statistical principle, the essential mathematics, the assumptions, a
worked synthetic example with a live calculator seeded to it and a figure that
follows it, the common misreading, the application to the case, one
diagnostic question with a hidden answer, and one exercise. Each ends
with a four-question exam,
marked in the browser with a reason for every answer; the lessons page
keeps your best score per lesson and a scorecard for the course.

| | Lesson | The question |
| --- | --- | --- |
| INTRO | Why Statistics Matters for AI Engineering | Why does modern AI engineering need statistics before it can trust prompt, model, agent and release comparisons? |
| A | Sampling distributions and standard error | Is a three-point gap a regression or two draws from one system? |
| B | Estimation and confidence intervals | What range is consistent with 9 of 10, and which formula says so? |
| C | Proportion and classification-metric uncertainty | Why is F1 on a rare class so much less certain than accuracy? |
| D | Effect sizes and practical significance | Who decides whether three points matter, and on what scale? |
| E | Hypothesis tests and statistical power | If the regression were real, would this evaluation have noticed? |
| F | Paired comparison of model versions | Both runs scored the same rows; does that change the answer? |
| G | Bootstrap and permutation methods | No formula was derived for this metric; what now? |
| H | Class imbalance and metric aggregation | How does 0.89 accuracy hide 3-in-10 recall on the class that matters? |
| I | Sampling bias, stratification and weighting | The set is 70% safari and production is 40%; what does the headline estimate? |
| J | Clustered and repeated observations | 500 frames from 40 outings: how many independent observations is that? |
| K | Test-set governance and reproducibility | Sixty rows were added and a label changed; whose drop is it? |
| L | Decision-oriented evaluation reporting | One page, one hour, one decision rule. |
| M | Confidence, calibration and combining scores | Does 0.9 mean nine in ten, and is the product the system's confidence? |
| N | Drift and monitoring | The weekly rate fell; what must be established before anyone touches the model? |

Every lesson carries a **figure**: the worked example as a picture,
drawn by the page from the calculator's own numbers and redrawn whenever
an input changes, so the picture can never disagree with the text. The
two coin-toss humps of Lesson A, the frames of the confusion table, the
disagreements that carry a paired comparison, the mosaic that shows what
an average is made of, the zones a release decision falls into, the
reliability diagram: each is inline SVG with a caption, in words on the
gentle track and in the lesson's notation on the standard one, and the
check draws every one of them in CI.

Alongside them: the **case** the examples follow, ten **core reasoning
rules**, seven **reference cards** (the reference-set manifest, the
minimum-meaningful-effect statement, the comparability checklist, the
confidence semantics card, the one-page report, the diagnosis record,
the review checklist), a
**glossary**, a **further reading** page with the sources behind each
method (none of it required; the lessons derive what they use), and the
five-line **session note** every lesson ends with.

## The case

The examples follow one fictional system throughout, under the codename
**Project Frog**: an AI reviewer of photographic contact sheets, whose
per-frame verdicts, categories, notes, reasons, evidence and links are
scored against the photographer's own decisions. The name is a codename
and means nothing; the system does not exist; every number about it is
synthetic. It was chosen because a contact sheet has exactly the
structure that makes evaluation statistics hard — rows inside documents
inside projects, rare positive classes, judges who disagree, a new
camera that changes the inputs without changing the model — and because
the domain needs no expertise to follow. A second, smaller example, an
AI reader of short-story drafts, appears where text similarity and
disagreeing editors need it. The case is described in full on the site's
**The case** page.

**Reference Set 2**, added 21 September 2026, is real: 12,713 frames from the author's own outings, with real exposure data and a real sharpness score, scored against which frames he actually kept (41 of them, 0.32%). There is still no reviewer — nothing scored these frames, real or fictional — so it is ground truth without a subject, offered for a reader's own arithmetic rather than used in any lesson's worked example. `data/reference-set-2.csv` has every row.

## Repository

- `index.html` — the whole site: a WORLD DATA section holding the
  lessons, case, rules, cards and glossary as plain literals, and an
  ENGINE section that renders them and runs the calculators.
- `data/reference-set-2.csv` — Reference Set 2 (see **The case**): real, not loaded by the page, a companion file for a reader's own computation.
- `tools/check.js` — the CI gate. It loads the script without a DOM and
  checks that every lesson has its nine parts, that every calculator
  reproduces the numbers its worked example quotes, that every figure
  draws from its calculator's defaults with a caption in words, that cards and
  glossary entries point at lessons, and that the page is one file with
  no network. Run it with `node tools/check.js`; it installs nothing.
- `.github/workflows/ci.yml` runs the check on every push and pull
  request; `pages.yml` serves `index.html` from GitHub Pages on every
  push to `main`.

The rules are the ones the author's other one-file tutorial repositories
follow: no dependencies, no build, no network, one reviewable file, never
rewritten programmatically. `CLAUDE.md` has the detail.

## Provenance

The repository began on 14 September 2026 from a coaching specification
drafted with an AI assistant, to keep a set of concepts from a work
discussion before they were lost. The specification's learner profile,
teaching approach, reasoning rules and method-selection guidance still
shape the course. Its original progression A–L now sits behind an
introductory lesson, `INTRO`, and lessons M and N were later added for
calibration and drift, which the specification's goals name but its
progression did not reach. Nothing in the repository describes any real
evaluation framework, dataset or organisation.

## Licence

Engine MIT (`LICENSE`); the lessons, case, cards and glossary CC BY 4.0
(`CONTENT-LICENSE.md`).
