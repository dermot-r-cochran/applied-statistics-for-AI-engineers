# Data Leakage

## Why does an AI engineer need to understand this?
Data leakage creates misleadingly optimistic metrics by letting evaluation data carry information that would not be available in real use. Engineers need to detect it because leakage can look like dramatic progress.

## 1. Engineering Problem
Project Frog suddenly gains several points of accuracy after a data refresh. The problem is checking whether the improvement reflects better modeling or hidden overlap between training and evaluation information.

## 2. Intuition
Leakage is best understood as a shortcut that contaminates the evaluation. It can happen through duplicated records, label-derived features, target-aware preprocessing, or split mistakes.

## 3. Mathematical Foundation
Explain leakage pathways, train-test contamination, temporal leakage, and group leakage. The mathematical lesson is that independence assumptions behind evaluation break when information crosses the boundary.

## 4. Python Example
Create synthetic examples of duplicate projects, project-level overlap, and temporally invalid features. Show how the metric inflates before the leakage is removed.

## 5. Interpretation
Interpret unexpectedly strong results as hypotheses to investigate, not prizes to accept automatically. Good skepticism is a statistical skill.

## 6. Common Mistakes
Mistakes include random row-level splitting when project-level grouping matters, fitting preprocessing on all data, and allowing future-derived signals into current predictions.

## 7. AI Engineering Applications
Use leakage checks in feature engineering, benchmark maintenance, notebook experimentation, and release readiness reviews. Leakage prevention is part of trustworthy measurement.

## 8. Exercises
Describe a Project Frog scenario where document-level splitting would leak project context. Explain how the unit of inference determines the correct split strategy.

## 9. Further Reading
Further reading should include practical leakage case studies and validation checklists.
