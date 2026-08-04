"""Metrics for human-AI collaboration experiments."""

from __future__ import annotations

from statistics import mean
from typing import Any, Iterable

Scenario = dict[str, Any]


def _safe_divide(numerator: float, denominator: float) -> float:
    """Return a rounded ratio while avoiding division by zero."""
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


def acceptance_rate(scenarios: Iterable[Scenario]) -> float:
    """Share of scenarios where the human accepted the AI recommendation."""
    items = list(scenarios)
    accepted = sum(1 for item in items if item.get("human_decision") == "accepted")
    return _safe_divide(accepted, len(items))


def override_rate(scenarios: Iterable[Scenario]) -> float:
    """Share of scenarios where the human rejected or revised the AI recommendation."""
    items = list(scenarios)
    overrides = sum(
        1
        for item in items
        if item.get("human_decision") in {"rejected", "revised", "overrode"}
    )
    return _safe_divide(overrides, len(items))


def agreement_rate(scenarios: Iterable[Scenario]) -> float:
    """Share of cases where the final decision aligned with the AI recommendation."""
    items = list(scenarios)
    agreements = sum(
        1
        for item in items
        if item.get("human_decision") == "accepted" or item.get("aligned_with_ai") is True
    )
    return _safe_divide(agreements, len(items))


def mean_decision_quality(scenarios: Iterable[Scenario]) -> float:
    """Average outcome quality across scenarios."""
    scores = [float(item.get("outcome_quality", 0.0)) for item in scenarios]
    return round(mean(scores), 4) if scores else 0.0


def mean_explanation_quality(scenarios: Iterable[Scenario]) -> float:
    """Average explanation quality across scenarios."""
    scores = [float(item.get("explanation_quality", 0.0)) for item in scenarios]
    return round(mean(scores), 4) if scores else 0.0


def collaboration_summary(scenarios: Iterable[Scenario]) -> dict[str, float | int]:
    """Return a compact metric summary for a collaboration study."""
    items = list(scenarios)
    return {
        "scenario_count": len(items),
        "acceptance_rate": acceptance_rate(items),
        "override_rate": override_rate(items),
        "agreement_rate": agreement_rate(items),
        "mean_decision_quality": mean_decision_quality(items),
        "mean_explanation_quality": mean_explanation_quality(items),
    }
