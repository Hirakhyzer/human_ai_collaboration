"""Scenario loading and lightweight validation utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

Scenario = dict[str, Any]

REQUIRED_FIELDS = {
    "id",
    "task",
    "human_role",
    "ai_role",
    "ai_recommendation",
    "human_decision",
    "outcome_quality",
}


def load_scenarios(path: str | Path) -> list[Scenario]:
    """Load collaboration scenarios from a JSON file."""
    scenario_path = Path(path)
    with scenario_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Scenario file must contain a list of scenario objects.")

    scenarios: list[Scenario] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each scenario must be a JSON object.")
        missing = REQUIRED_FIELDS.difference(item)
        if missing:
            raise ValueError(f"Scenario {item.get('id', '<unknown>')} is missing: {sorted(missing)}")
        scenarios.append(item)
    return scenarios


def scenario_table(scenarios: list[Scenario]) -> list[dict[str, str | float]]:
    """Create a simplified table for reports or notebooks."""
    return [
        {
            "id": str(item["id"]),
            "task": str(item["task"]),
            "decision": str(item["human_decision"]),
            "quality": float(item.get("outcome_quality", 0.0)),
            "risk_tags": ", ".join(item.get("risk_tags", [])),
        }
        for item in scenarios
    ]
