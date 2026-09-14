# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## What this is

A one-file course in applied statistics for AI evaluation: fourteen
lessons (A–N) on sampling variation, intervals, classification-metric
uncertainty, effect sizes, power, paired comparison, resampling,
aggregation, stratification, clustering, test-set governance, decision
reporting, calibration and drift. Open `index.html` in any browser: no
server, no build, no dependencies, no network. Each lesson has the same
nine parts and a live calculator seeded with its worked example, so the
numbers in the text are the numbers on screen.

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
- **Every number is synthetic and every example says so.** Never present
  a measurement as real, never describe a real evaluation framework,
  dataset or organisation, and never invent an organisational decision.

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

## Adding a lesson

Append to `LESSONS` with the next letter, all nine parts and a calculator
with `expect` values that the prose quotes. Add glossary entries that name
the lesson and, if it introduces a template, a card that points at it.
Update the table in `README.md`. Then `node tools/check.js`.

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
