"""Statistical utilities for applied AI evaluation."""

from .bootstrap import bootstrap_metric
from .comparison import compare_two_models
from .intervals import (
    clopper_pearson_interval,
    confidence_interval_accuracy,
    wilson_interval,
)
from .metrics import confusion_matrix_uncertainty
from .power import minimum_detectable_effect, power_analysis
from .sampling import effective_sample_size

__all__ = [
    "bootstrap_metric",
    "clopper_pearson_interval",
    "compare_two_models",
    "confidence_interval_accuracy",
    "confusion_matrix_uncertainty",
    "effective_sample_size",
    "minimum_detectable_effect",
    "power_analysis",
    "wilson_interval",
]
