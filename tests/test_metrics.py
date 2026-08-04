from hai_lab.metrics import acceptance_rate, collaboration_summary, override_rate
from hai_lab.risk import dominant_risks, trust_calibration_flags


SCENARIOS = [
    {
        "id": "a",
        "human_decision": "accepted",
        "aligned_with_ai": True,
        "outcome_quality": 0.9,
        "explanation_quality": 0.7,
        "ai_confidence": 0.8,
        "risk_tags": ["automation_bias"],
    },
    {
        "id": "b",
        "human_decision": "revised",
        "aligned_with_ai": False,
        "outcome_quality": 0.7,
        "explanation_quality": 0.4,
        "ai_confidence": 0.5,
        "risk_tags": ["low_explainability"],
    },
]


def test_acceptance_and_override_rates():
    assert acceptance_rate(SCENARIOS) == 0.5
    assert override_rate(SCENARIOS) == 0.5


def test_collaboration_summary():
    summary = collaboration_summary(SCENARIOS)
    assert summary["scenario_count"] == 2
    assert summary["mean_decision_quality"] == 0.8
    assert summary["mean_explanation_quality"] == 0.55


def test_risk_analysis():
    assert dominant_risks(SCENARIOS, limit=1) == ["automation_bias"]
    assert trust_calibration_flags(SCENARIOS) == []
