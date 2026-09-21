from pathlib import Path

from agents.bankassist.evaluation import evaluate_dataset


def test_golden_dataset_policy_outcomes():
    path = Path(__file__).parents[2] / "evaluation" / "golden_dataset.jsonl"
    metrics = evaluate_dataset(path)
    assert metrics["correctness"] == 1.0
    assert metrics["groundedness"] == 1.0
    assert metrics["policy_compliance"] == 1.0
    assert metrics["retrieval_quality"] == 0.75
