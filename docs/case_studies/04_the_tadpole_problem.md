# The Tadpole Problem

## Scenario
Project Frog evaluation contains **1,000 observations** but they come from only **6 projects**.

## Questions to answer
- Are observations independent?
- What is the effective sample size?
- Why can clustering mislead evaluation?

## Concepts to practice
- cluster effects
- dependence
- hierarchical sampling
- effective sample size

## Engineering discussion
A thousand rows can create a false sense of precision when many rows share project-level context. If errors cluster within projects, the effective sample size may be far smaller than the raw count suggests. Engineers should reason at the level that the dependence structure supports and avoid pretending that repeated similar examples add full independent evidence.

## What to inspect next
- project-level performance variation
- average project size and intra-project similarity
- whether inference is supposed to generalize to documents, projects, or both
- sensitivity of conclusions to project-level aggregation

## Trust prompts
- What exactly is being compared?
- What uncertainty is missing or understated?
- What population mismatch could invalidate the result?
- What decision would be premature here?
