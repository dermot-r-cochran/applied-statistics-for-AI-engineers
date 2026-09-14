const setText = (id, value) => {
  const node = document.getElementById(id);
  if (node) {
    node.textContent = value;
  }
};

const setupTutorial = () => {
  const cards = [...document.querySelectorAll("[data-step-card]")];
  if (!cards.length) {
    return;
  }

  let index = 0;
  const update = () => {
    cards.forEach((card, cardIndex) => {
      card.hidden = cardIndex > index;
    });
    setText("step-progress", `${index + 1} / ${cards.length}`);
  };

  document.getElementById("next-step")?.addEventListener("click", () => {
    index = Math.min(index + 1, cards.length - 1);
    update();
  });

  document.getElementById("reset-steps")?.addEventListener("click", () => {
    index = 0;
    update();
  });

  update();
};

const setupDecisionDemo = () => {
  const threshold = document.getElementById("threshold");
  const score = document.getElementById("score");
  const confidence = document.getElementById("confidence");
  if (!threshold || !score || !confidence) {
    return;
  }

  const render = () => {
    const thresholdValue = Number(threshold.value);
    const scoreValue = Number(score.value);
    const confidenceValue = Number(confidence.value);
    const passes = scoreValue >= thresholdValue;
    const reliable = confidenceValue >= 0.7;

    setText("threshold-value", thresholdValue.toFixed(2));
    setText("score-value", scoreValue.toFixed(2));
    setText("confidence-value", confidenceValue.toFixed(2));
    setText("decision-label", passes ? "Escalate to frog safety review" : "Approve for automated handling");

    const status = document.getElementById("decision-status");
    if (!status) {
      return;
    }

    if (passes && reliable) {
      status.textContent = "The case is high risk and the estimate is stable across repeated samples.";
      status.className = "result-good";
    } else if (passes || reliable) {
      status.textContent = "The case is borderline: collect more labeled data before changing policy.";
      status.className = "result-warn";
    } else {
      status.textContent = "The case is low risk and confidence is weak, so keep the current workflow but continue monitoring.";
      status.className = "";
    }
  };

  [threshold, score, confidence].forEach((input) => input.addEventListener("input", render));
  render();
};

document.addEventListener("DOMContentLoaded", () => {
  setupTutorial();
  setupDecisionDemo();
});
