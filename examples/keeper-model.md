# The keeper model: a delegate model, built by a language model

A worked example of a model built in a particular way: a language model
designed, wrote, trained and checked a small model, which then makes its
narrow judgement quickly, cheaply and with a probability that can be
tested. Here that is a logistic regression on **Reference Set 2** that gives
each frame a probability of being kept. It is real data and a real model,
so its numbers are real. The photographer's own decisions are the labels,
and nothing in it is Proofsheet.

`examples/keeper-model.js` is the whole of it, with no dependencies.
`node examples/keeper-model.js` prints the report. `--check` also confirms
that this page quotes every figure the run produces, and CI runs it that
way.

## What the language model did, and what it did not

A language model (Claude, working in a coding session at the author's
request on 25 and 26 October 2026) did the parts that take judgement and
code:

- **chose the label:** kept means published or kept as a master;
- **chose the features:** ISO, shutter speed and focal length on log
  scales; aperture; the sharpness and brightness scores; a flag for a
  missing ISO; and each frame's sharpness and brightness percentile within
  its own outing;
- **chose the validation:** every outing held out in turn;
- **chose the measures:** discrimination, calibration and a shortlist test;
- **wrote and ran the code,** and read the results.

It did **not** supply the labels. Every one of the 41 keeps is a decision
the photographer made, at the time, for his own reasons. That is the
condition that makes a delegate model worth more than the model that built
it. A delegate trained on a language model's own guesses can at best copy
those guesses, mistakes included. Trained on outcomes from outside, its
probability can be checked against something.

The order of events matters for reading the numbers. Two feature sets were
tried, and this one was kept after the other's results were seen. One
choice made after looking is a small forking path, not a large one. It is
still a reason to read the margins below as a little optimistic (Lesson K).

## The result

**12,713** frames from 33 outings; 41 kept, a base rate of **0.32%**. ISO is
blank on **2,474** frames; it is filled with the median and flagged. Each
probability comes from a model fitted to the other 32 outings.

| Measure | The model | For comparison |
| --- | --- | --- |
| ROC AUC | 0.53 | 0.5 is chance |
| Average precision | 0.0039 | 0.0032 by chance |
| Brier score | 0.00322 | 0.00321 for always saying the base rate |
| Mean predicted | 0.33% | 0.32% observed |
| Calibration error, ten quantile bins | 0.00183 | |

**Calibrated, and saying almost nothing.** The average prediction matches
the base rate, and the calibration error is tiny. The Brier score is no
better than a model that gives every frame 0.32%, and the ranking across
outings is barely better than chance. This is the trap Lesson M describes:
a model can be well calibrated simply by never leaving the base rate. Its
highest-scored 1% (127 frames) averaged 1.37% predicted and held none of
the keeps. The decile table that `node examples/keeper-model.js` prints
shows the same thing bin by bin. At this base rate each decile holds about
four keeps, so no single bin's gap is evidence on its own (Lesson C).

**Within an outing, it earns its keep.** Asked a smaller question, "which
frames of *this* outing are worth a first look?", the model does better.
The table counts keeps found in the top slice of their own outing, with
ranking by raw sharpness alone as the baseline:

| Shortlist | Keeps found (of 41) | By chance | Sharpness alone |
| --- | --- | --- | --- |
| 5% | 9 | 2 | 3 |
| 10% | 11 | 4 | 6 |
| 20% | 13 | 8 | 11 |

A 5% shortlist finds about four times what chance would. Brightness alone
finds 1. With 41 keeps the counts are small, and a Wilson interval on 9 of 41
runs from about 0.12 to 0.37 (Lesson B). The frames also cluster
by outing, so the 41 are not 41 independent observations (Lesson J).

## What it shows

Exposure and sharpness cannot say what the photographer keeps. His choices
turn on subject, moment and composition, and none of those are in these
columns. A better model would need better evidence, not more fitting: the
subject labels of **Reference Set 3**, or features read from the images
themselves.

There is a general lesson for any delegate model. The builder's fluency
says nothing about the delegate's worth. What tells you its worth is the
held-out evidence: a calibration curve, a comparison with the trivial model
and with the obvious single feature, and a test of the narrower use it was
built for. On this evidence the keeper model is useful as a per-outing
first sort. It has not earned the right to say how likely any frame is to
be kept.

## Reproducing it

The fit is an L2-penalised logistic regression (`C = 1`, intercept
unpenalised, no class weighting) on standardised features. It is solved by
Newton's method, so it converges to the exact optimum and every run gives
the same numbers. Average precision is computed step-wise over distinct
thresholds, and AUC by the Mann–Whitney count with ties shared. Ties in a
percentile go to the earlier row. The run takes a few seconds.
