"""Public BankAssist entry point shared by CLI, jobs and the web app."""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from typing import Any

from agents.bankassist.eligibility import evaluate_candidates
from agents.bankassist.evidence import extract_structured_rows
from agents.bankassist.orchestrator import get_bankassist_evidence
from agents.bankassist.prompts import POLICY_QUERY, STRUCTURED_QUERY
from agents.bankassist.synthesizer import synthesize_bankassist_answer


@dataclass
class BankAssistResult:
    answer: str
    assessments: list[dict[str, Any]]
    evidence: dict[str, Any]
    latency_seconds: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


async def ask_bankassist(
    question: str,
    structured_query: str = STRUCTURED_QUERY,
    policy_query: str = POLICY_QUERY,
) -> BankAssistResult:
    started = time.perf_counter()
    evidence = await get_bankassist_evidence(structured_query, policy_query)
    rows = extract_structured_rows(evidence["structured_evidence"])
    assessments = evaluate_candidates(rows)
    answer = synthesize_bankassist_answer(question, evidence, assessments)

    return BankAssistResult(
        answer=answer,
        assessments=assessments,
        evidence=evidence,
        latency_seconds=round(time.perf_counter() - started, 3),
    )
