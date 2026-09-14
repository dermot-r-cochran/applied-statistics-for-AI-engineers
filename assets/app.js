function toggleById(id, trigger) {
  const el = document.getElementById(id);
  if (!el) return;
  el.hidden = !el.hidden;
  if (trigger) {
    const expanded = !el.hidden;
    trigger.setAttribute("aria-expanded", String(expanded));
  }
}

function checkDiagnostic() {
  const selected = document.querySelector('input[name="diag"]:checked');
  const result = document.getElementById("diag-result");
  if (!result) return;
  if (!selected) {
    result.textContent = "Please select one option before checking.";
    return;
  }
  if (selected.value === "b") {
    result.textContent = "Correct: a smaller sample increases uncertainty, but does not imply upward bias.";
  } else {
    result.textContent = "Not quite: this confuses uncertainty with bias. Small n widens intervals, it does not justify inflating accuracy.";
  }
}

function buildSessionSummary() {
  const coreEl = document.getElementById("core");
  const frgEl = document.getElementById("frg");
  const assumptionEl = document.getElementById("assumption");
  const taskEl = document.getElementById("task");
  const guideEl = document.getElementById("guide");
  const out = document.getElementById("session-output");
  if (!coreEl || !frgEl || !assumptionEl || !taskEl || !guideEl || !out) return;
  const core = coreEl.value.trim();
  const frg = frgEl.value.trim();
  const assumption = assumptionEl.value.trim();
  const task = taskEl.value.trim();
  const guide = guideEl.value.trim();
  out.textContent =
`Core principle
- ${core}

FRG application
- ${frg}

Assumption to check
- ${assumption}

One practice task
- ${task}

Suggested note for statistical interpretation guide
- ${guide}`;
}
