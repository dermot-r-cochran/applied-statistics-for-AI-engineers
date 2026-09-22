# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## What this is

A one-file course in applied statistics for AI evaluation: fifteen
lessons — an introduction (`INTRO`, why an AI engineer needs this at
all) and A–N on sampling variation, intervals, classification-metric
uncertainty, effect sizes, power, paired comparison, resampling,
aggregation, stratification, clustering, test-set governance, decision
reporting, calibration and drift. Open `index.html` in any browser: no
server, no build, no dependencies, no network. Each lesson has the same
nine parts, a live calculator seeded with its worked example, and a
figure drawn from that calculator, so the numbers in the text, on screen
and in the picture are the same numbers.

**It is about statistics, not about any AI framework or product** —
evaluation metrics and confidence intervals, and the reasoning that goes
with them (Dermot, 2026-09-14). It bears on building a test strategy, but
the subject is the statistics.

It began on 2026-09-14 from a coaching specification Dermot had an AI
assistant draft so that the concepts from a work discussion were not lost;
the spec is preserved in pull request #1's description under "Original
prompt" and is the brief: learner profile, primary goal, teaching approach,
core reasoning rules, method-selection guidance, progression A–L, the
nine-part lesson format, the five-line session note. Lessons M and N were
added for calibration and drift, which the spec's goals name and its
progression did not reach.

## The prime directive

**Everything the reader can meet lives in the data structures at the top
of `index.html`'s script, and the engine below them never needs editing
to add a lesson.** Preserve that; the rules below follow from it, and they
are the `four-islands-quest` rules, which this repository inherits whole:

- **No dependencies, no build step, no network calls, no framework.** Not
  in the page, not in the tools. `tools/check.js` runs on the Node that
  ships with the CI runner and installs nothing. Python belongs in lessons
  only as stdlib snippets a reader can paste, never as a package here.
- **One reviewable file.** The course diffs cleanly in git because it is
  plain literals in one place. Don't split it, minify it, or move content
  into JSON the page fetches.
- **Never rewrite `index.html` programmatically.** Author by hand or with
  an assistant. The check reads the script by loading it into a bare VM
  context — no `document`, so the page never boots — and reads `BOOK`.

## The case, and its name

The examples follow one fictional system, codenamed **Project Frog**: an
AI reviewer of photographic contact sheets whose per-frame output
(identifier, verdict, category, note, reason, evidence, relations) is
scored against the photographer's own decisions. Rows are frames,
documents are contact sheets, projects are trips, scenarios are kinds of
shooting; the reference set is "Reference Set 1", 500 frames from 40
outings across 6 projects. The full description is `CASE` in the data
section and is the single source for it.

**Provenance and rules, all Dermot's, 2026-09-14:**

- The spec was anonymised, generalised and fictionalised from a work
  context. **The name of the framework it replaced is never written in
  this repository** — not in content, commits, pull requests or comments.
  `tools/check.js` fails the build if it appears anywhere; the check
  assembles the string from character codes so it does not contain it.
- "Project Frog" is a codename and means nothing. **It is about AI rather
  than frogs**: no amphibian content, no pond puns. The earlier
  amphibian-monitoring fiction an assistant built was removed on the same
  day.
- Photography was Dermot's suggestion for the case: it has the row /
  document / project structure, rare classes, disagreeing judges, and
  needs no expertise. Creative-writing evaluation (an AI reader of story
  drafts) is the secondary example, used only where text similarity or
  disagreeing editors need it. Keep it secondary.
- **Every worked example is synthetic and says so.** Never present a lesson's own measurement as real, never describe a real evaluation framework, dataset or organisation, and never invent an organisational decision.
- **Reference Set 2 is the one exception, and it is scoped narrowly** (Dermot, 21 September 2026, widening issue #20 from weak frames only to *any relevant frame of mine*): real photographs, real EXIF, a real sharpness score, and real ground truth (kept or not). **There is still no reviewer** — nothing scores these frames, so nothing about an AI system is claimed real. It lives in `data/reference-set-2.csv`, described on the case page and in the README, and is never wired into a lesson's `calc`/`expect`: those stay Reference-Set-1 synthetic, so the check's guarantee that a lesson's numbers reproduce is untouched.

## The lesson format

Nine parts, in this order, every lesson: `question` (the engineering
problem first), `principle`, `maths` (derived, not asserted),
`assumptions` (a list), `example` (synthetic, with the calculator seeded
to it), `pitfall`, `application` (to the case), `diagnostic` (`q` and a
hidden `a`), `exercise`. Prose uses the small markup the engine renders:
blank line between paragraphs, `` `code` `` for mathematics, `**bold**`,
`- ` lists, `| ` tables with the first row as header.

**Every calculator reproduces its worked example.** A lesson's `calc`
declares `inputs` (key, label, default, min, max, step — or `null`s for a
text field), `compute`, `outputs` (key, label, decimals) and `expect`: the
values the example prose quotes, at the default inputs. The check computes
`compute(defaults)`, compares each `expect` to the tolerance of its
displayed decimals, and requires the formatted value to appear in the
example prose. **Change a number in the prose and the check fails until
the calculator agrees, and vice versa.** Resampling calculators are
seeded (`mulberry32`, seed 20240914) so their intervals are reproducible;
get their numbers by running the engine under Node, never by estimating.

Register: expert to expert, plain, no hedging beyond what the statistics
require and no claims beyond what they support. Every lesson points at
at least one other lesson (the check requires it), because the course is
a web, not a list.

## The figures

Added 2026-09-21 at Dermot's direction (*make the tutorial more visual
with diagrams and examples, especially the gentle introduction*). Every
lesson carries a `figure`: `title`, `gentle` (a caption in words for the
gentle page; the check refuses backtick notation in it and requires it to
be substantial), `caption` (for the standard track, notation allowed) and
`draw(v, r)`, a function of the calculator's inputs `v` and its
`compute(v)` result `r` that returns a figure spec, or an array of specs
for stacked panels. The engine's `FIG` (pure section, exported in
`BOOK`) turns a spec into inline SVG as a string, so the check draws
every figure without a DOM and the page redraws one on every input. The
figure is the worked example as a picture: it is drawn from the same
numbers as the calculator, which is what keeps it from ever disagreeing
with the prose, and the check renders it at the defaults and fails on a
spec that does not draw or is not finite.

Eight kinds, all 640 units wide: `grid` (rows as squares, flat `cells`
or clustered `blocks`; `FIG.cells` scales counts so a million rows still
draws), `intervals` (bars on one axis, with `bands`, `marks` and
stacked `dots`), `curves` (normal sampling distributions with optional
shaded regions), `bars` (widths optional, so a mosaic; a legend replaces
under-bar labels when bars are narrow), `hist`, `xy` (points with error
bars, lines, a diagonal), `steps` (boxes and arrows in rows) and `nest`
(boxes inside boxes). Colour is by class, and the palette was validated
for colour-vision deficiency in both modes: `f1` and `f2` are the two
runs (blue, orange), `f3` a third category, `f0` the neutral majority,
`fx` a darker neutral, and `ok` / `warn` / `bad` the site's status
colours for decision zones. Every class is named on the figure itself,
so nothing is carried by colour alone. A new lesson reuses these kinds;
a new kind is an engine change and goes in `FIG` with the others. The
case page and the start page carry one static figure each (`spec`,
no `draw`), and the check draws those too.

Two rules for authoring one. The gentle caption tells the reader what
the picture shows in the same words the gentle page uses, with the
lesson's numbers; it is not a description of the chart type. And the
figure follows the calculator wherever it can: a panel that uses fixed
example numbers instead (Lesson N's two mosaics) says so in its caption.
Read the figures back in a browser after changing one: layout faults
(clipped legends, colliding labels) are exactly what the check cannot
see.

## The two tracks

Added 2026-09-19 at Dermot's direction (*a lighter, gentler optional
introduction track based on a few calibration questions at the start*).
`CALIBRATION` holds the start page: four scored questions (`q`, `o`, `a`),
one self-report question about notation (`self`, with `gentleAt` the
option index from which "words first" is inferred), `passAt` (the score
below which the gentle track is suggested), the two verdicts and a
static `figure` of the two tracks. Every lesson carries a `gentle` page:
the engineering question in everyday terms, the one idea in bold, the
worked example told in words with the lesson's own numbers, an everyday
version of it (a coin, a café, a smoke detector: an analogy with no
numbers in it, added 2026-09-21), and "so the answer is"; the lesson's
figure renders under it with its `gentle` caption. It is words: the check
refuses backtick notation in it and requires it to be substantial. The
gentle track renders that page above the nine parts and changes nothing
else; the track is a localStorage preference, switchable at the top of
any lesson, and the suggestion never locks anything. Keep the gentle
page's numbers the same as the example's, so the two never disagree.

## Adding a lesson

Append to `LESSONS` with the next letter, all nine parts, a `gentle`
page, a calculator with `expect` values that the prose quotes, and a
`figure` drawn from that calculator. Add glossary entries that name
the lesson and, if it introduces a template, a card that points at it.
Update the table in `README.md`. Then `node tools/check.js`.

`INTRO` is the one lesson not named by a letter, and the only one that
sits ahead of the sequence: it is the course's own introduction, added
2026-09-22, and it carries the same nine parts, gentle page, calculator,
figure and exam as every other. The check derives the expected ids
(`INTRO`, then A, B, C…) from the book rather than a list, so appending
a lesson still needs no edit there. Cross-references are counted only
where the prose writes **Lesson** or **Lessons** before the ids — a
bare backticked capital is a variable in this course's notation, not a
lesson, and reading it as one would both satisfy the
refers-to-another-lesson gate by accident and raise a phantom dangling
reference after a rename.

`EXAMS[id]` is the lesson's exam (added 2026-09-14 at Dermot's direction:
*add an exam and score card at the end of each lesson*): four or more
multiple-choice questions, each `{q, o, a, why}` with `a` the index of the
correct option and `why` shown after marking whatever was chosen. Marked in
the browser; the lessons page keeps the best score per lesson and a
scorecard (pass is three of four or better). The check requires at least
four questions, three distinct options each, a valid answer index, a
reason, and correct answers not all in the same position. Questions test
the lesson's reasoning, not recall of its numbers, and every distractor
should be a mistake a competent engineer actually makes.

`READING` is the further-reading page (added 2026-09-14 at Dermot's
direction): the sources behind each method, each with a one-line reason
and the lessons it serves; the check requires every entry to point at a
real lesson. It is context, not curriculum — the lessons derive what they
use — so add an entry only for a source a lesson actually rests on, cite
it fully, and never add a source you have not verified exists as cited.

## Publishing

`.github/workflows/pages.yml` serves `index.html` from GitHub Pages on
every push to `main`; CI (`ci.yml`) runs the check on every push and pull
request and installs nothing. Content at Dermot's direction opens a pull
request and merges on green; a change to the case, the rules or the
lesson format is his call.

## Licence

Engine MIT (`LICENSE`); the lessons, case, rules, cards and glossary
CC BY 4.0 (`CONTENT-LICENSE.md`).
