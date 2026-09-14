# Applied Statistics for AI Engineers

Applied Statistics for AI Engineers is a practical Python repository for software engineers, ML engineers, AI engineers, data scientists, and technical leads who need stronger statistical judgment when evaluating AI systems.

The repository teaches how to reason about uncertainty, sampling, measurement, experimentation, monitoring, and evidence-based release decisions. The emphasis is engineering decision making rather than academic derivations.

## Why this repository exists

AI engineers routinely look at dashboards, offline evaluations, online experiments, and model comparisons that appear precise but often hide uncertainty. A metric can move because of noise, bias, sampling changes, leakage, measurement drift, or a genuine product change. This repository is designed to help readers answer the recurring question:

**When should an engineer trust an observed metric?**

## Audience

This material is for readers who already know programming and basic machine learning, but want better statistical intuition for:

- deciding whether a metric change is noise or signal
- understanding what an estimate does and does not prove
- designing better evaluations and experiments
- communicating uncertainty to stakeholders
- making deployment decisions with incomplete evidence

## Teaching approach

Every chapter starts by answering **“Why does an AI engineer need to understand this?”** before introducing formulas. Throughout the repository, examples stay synthetic and fictional. The goal is to generalize the lesson, not the implementation.

## Project Frog

The repository uses a recurring fictional environment called **Project Frog**.

Project Frog is an AI-assisted document analysis and decision-support platform. It processes documents, projects, classifications, evidence, recommendations, explanations, and compliance decisions. It reports synthetic metrics such as:

- accuracy
- precision
- recall
- F1
- agreement rate
- coverage
- evidence quality
- latency
- processing cost

Project Frog is intentionally fictional so the repository can focus on transferable statistical reasoning instead of any proprietary workflow or dataset.

## Learning outcomes

By working through the material, a senior engineer should be able to decide:

- what a reported metric means
- what it does not mean
- which assumptions support the conclusion
- whether two evaluations are actually comparable
- whether observed differences are likely due to noise, bias, leakage, or true change
- whether current evidence supports a deployment or rollback decision
- what additional evidence would reduce uncertainty

## Repository structure

```text
.
├── README.md
├── docs/
├── tutorials/
├── notebooks/
├── examples/
├── src/applied_stats_ai/
└── tests/
```

### Core content

- `docs/`: short, engineering-focused chapters covering the statistical concepts behind trustworthy AI evaluation.
- `tutorials/`: hands-on walkthroughs and Project Frog case studies.
- `examples/`: small synthetic examples that use the package.
- `src/applied_stats_ai/`: reusable Python utilities for uncertainty estimation, model comparison, and experimental design.
- `tests/`: pytest coverage for the public library functions.

## Chapter map

1. Probability foundations  
2. Sampling and variation  
3. Confidence intervals  
4. Hypothesis testing  
5. Effect size  
6. Statistical power  
7. Bootstrap methods  
8. Bayesian reasoning  
9. Classification metrics  
10. Metric uncertainty  
11. Model comparison  
12. Experimental design  
13. A/B testing  
14. Test set design  
15. Sampling bias  
16. Data leakage  
17. Measurement theory  
18. Decision theory  
19. Monitoring under uncertainty

## Getting started

This repository targets **Python 3.12+** and uses **uv** for project management.

```bash
uv sync
uv run ruff check .
uv run pytest
```

To explore the first tutorial notebook:

```bash
uv run jupyter lab tutorials/confidence_intervals/confidence_intervals_for_accuracy.ipynb
```

## First places to start

- Read `docs/03_confidence_intervals.md` to understand interval estimates for Project Frog accuracy.
- Work through `tutorials/confidence_intervals/confidence_intervals_for_accuracy.ipynb`.
- Use the Project Frog case studies in `tutorials/project_frog_case_studies/` to practice making release decisions under uncertainty.

## Development principles

- Educational only
- Synthetic examples only
- Practical engineering decisions over abstract mathematics
- Clear assumptions before conclusions
- Reproducible analysis in Python
