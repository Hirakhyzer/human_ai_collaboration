"""Human-AI Collaboration Lab.

Small research utilities for modeling collaboration scenarios,
computing human-AI workflow metrics, and identifying risk signals.
"""

from .metrics import collaboration_summary
from .risk import risk_frequency, dominant_risks
from .workflow import load_scenarios

__all__ = [
    "collaboration_summary",
    "risk_frequency",
    "dominant_risks",
    "load_scenarios",
]
