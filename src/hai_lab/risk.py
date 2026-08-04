"""Risk analysis helpers for human-AI collaboration scenarios."""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable

Scenario = dict[str, Any]


def risk_frequency(scenarios: Iterable[Scenario]) -> dict[str, int]:
    """Count risk tags across collaboration scenarios."""
    counter: Counter[str] = Counter()
    for scenario in scenarios:
        counter.update(str(tag) for tag in scenario.get("risk_tags", []))
    return dict(counter.most_common())


def dominant_risks(scenarios: Iterable[Scenario], limit: int = 3) -> list[str]:
    """Return the most frequent risk tags."""
    return list(risk_frequency(scenarios).keys())[:limit]


def trust_calibration_flags(scenarios: Iterable[Scenario]) -> list[dict[str, str]]:
    """Identify simple trust-calibration warning signs.

    A scenario is flagged when the human accepted a low-confidence AI output
    or rejected a high-confidence AI output. These flags are not final evidence;
    they are prompts for deeper qualitative review.
    """
    flags: list[dict[str, str]] = []
    for scenario in scenarios:
        confidence = float(scenario.get("ai_confidence", 0.0))
        decision = scenario.get("human_decision")
        scenario_id = str(scenario.get("id", "unknown"))

        if decision == "accepted" and confidence < 0.55:
            flags.append({
                "id": scenario_id,
                "flag": "possible_over_trust",
            })
        elif decision in {"rejected", "overrode"} and confidence > 0.85:
            flags.append({
                "id": scenario_id,
                "flag": "possible_under_trust",
            })
    return flags
