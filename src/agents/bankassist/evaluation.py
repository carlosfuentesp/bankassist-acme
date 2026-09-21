"""Golden-dataset evaluation with MLflow tracking and deterministic policy checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from agents.bankassist.eligibility import evaluate_candidate

DEFAULT_DATASET = Path(__file__).with_name("golden_dataset.jsonl")


def _score_case(case: dict[str, Any]) -> dict[str, float]:
    assessment = evaluate_candidate(case["structured_evidence"])
    expected = case["expected"]
    return {
        "correctness": float(
            assessment.eligible_for_evaluation == expected["eligible_for_evaluation"]
        ),
        "groundedness": float(bool(case.get("structured_evidence"))),
        "retrieval_quality": float(
            case.get("retrieved_policy_id") == expected["policy_id"]
        ),
        "policy_compliance": float(
            assessment.policy_id == expected["policy_id"]
            and assessment.decision != "APPROVED"
        ),
    }


def evaluate_dataset(path: Path = DEFAULT_DATASET) -> dict[str, float]:
    cases = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    scores = [_score_case(case) for case in cases]
    return {
        name: sum(score[name] for score in scores) / len(scores)
        for name in scores[0]
    } | {"cases": float(len(cases))}


def main() -> None:
    import mlflow

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--experiment", default="/Shared/bankassist-acme-evaluation")
    args = parser.parse_args()

    metrics = evaluate_dataset(args.dataset)
    mlflow.set_experiment(args.experiment)
    with mlflow.start_run(run_name="bankassist-golden-evaluation"):
        mlflow.log_params({"dataset": str(args.dataset), "policy": "POL-COL-2026-01"})
        mlflow.log_metrics(metrics)
        mlflow.log_artifact(str(args.dataset), artifact_path="golden_dataset")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
