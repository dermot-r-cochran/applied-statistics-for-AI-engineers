# AI evaluation review checklist

Use this checklist before major release or governance reviews.

- [ ] The decision and evidence threshold are explicit.
- [ ] The target population and known exclusions are documented.
- [ ] Metric definitions, thresholds, and scoring code are versioned.
- [ ] Ground-truth creation and adjudication rules are documented.
- [ ] Representativeness and subgroup coverage have been reviewed.
- [ ] Dependence and clustering risks have been assessed.
- [ ] Confidence semantics are documented for every score used in decisions.
- [ ] Calibration evidence is reported where scores claim probabilistic meaning.
- [ ] Comparability limits are stated for all reported deltas.
- [ ] Release evidence is classified as support, support with caveats, insufficient, or risk-indicating.
- [ ] Monitoring commitments and triggers are defined.
- [ ] All examples and artifacts remain synthetic and free of proprietary content.
