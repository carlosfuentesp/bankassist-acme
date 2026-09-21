"""Output guardrails independent from model prompting."""

from __future__ import annotations

import re

APPROVAL_PATTERNS = (
    r"\bacuerdo (?:ha sido|fue|queda) aprobad[oa]\b",
    r"\bapruebo (?:el|un) acuerdo\b",
    r"\baprobar automáticamente\b",
)


class GuardrailViolation(RuntimeError):
    pass


def validate_answer(answer: str, allowed_policy_ids: set[str]) -> str:
    normalized = answer.lower()
    for pattern in APPROVAL_PATTERNS:
        if re.search(pattern, normalized, flags=re.IGNORECASE):
            raise GuardrailViolation("La respuesta afirma una aprobación no autorizada.")

    cited = set(re.findall(r"\[(POL-[A-Z]+-\d{4}-\d+)\]", answer))
    unauthorized = cited - allowed_policy_ids
    if unauthorized:
        raise GuardrailViolation(
            "La respuesta cita políticas no recuperadas: " + ", ".join(sorted(unauthorized))
        )
    return answer
