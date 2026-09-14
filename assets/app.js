function toggleById(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.toggle("hidden");
}

function checkDiagnostic() {
  const selected = document.querySelector('input[name="diag"]:checked');
  const result = document.getElementById("diag-result");
  if (!selected || !result) return;
  if (selected.value === "b") {
    result.textContent = "Correct: a smaller sample increases uncertainty, but does not imply upward bias.";
  } else {
    result.textContent = "Not quite: this confuses uncertainty with bias. Small n widens intervals, it does not justify inflating accuracy.";
  }
}

function buildSessionSummary() {
  const core = document.getElementById("core").value.trim();
  const frg = document.getElementById("frg").value.trim();
  const assumption = document.getElementById("assumption").value.trim();
  const task = document.getElementById("task").value.trim();
  const guide = document.getElementById("guide").value.trim();
  const out = document.getElementById("session-output");
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
