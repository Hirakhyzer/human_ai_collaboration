"""Evaluate the sample human-AI collaboration scenarios.

Run from the repository root:

    python examples/evaluate_collaboration.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hai_lab.metrics import collaboration_summary
from hai_lab.risk import dominant_risks, risk_frequency, trust_calibration_flags
from hai_lab.workflow import load_scenarios, scenario_table


def main() -> None:
    data_path = ROOT / "data" / "collaboration_scenarios.json"
    scenarios = load_scenarios(data_path)

    report = collaboration_summary(scenarios)
    report["dominant_risks"] = dominant_risks(scenarios)

    print("\nHuman-AI Collaboration Summary")
    print(json.dumps(report, indent=2))

    print("\nRisk Frequency")
    print(json.dumps(risk_frequency(scenarios), indent=2))

    print("\nTrust Calibration Flags")
    print(json.dumps(trust_calibration_flags(scenarios), indent=2))

    print("\nScenario Table")
    print(json.dumps(scenario_table(scenarios), indent=2))


if __name__ == "__main__":
    main()
