import pytest

from agents.bankassist.guardrails import GuardrailViolation, validate_answer


def test_accepts_grounded_evaluation_language():
    answer = "CUST-002 cumple condiciones para evaluación [POL-COL-2026-01]."
    assert validate_answer(answer, {"POL-COL-2026-01"}) == answer


def test_rejects_unauthorized_policy_citation():
    with pytest.raises(GuardrailViolation):
        validate_answer("Regla aplicable [POL-COL-2025-01].", {"POL-COL-2026-01"})


def test_rejects_automatic_approval():
    with pytest.raises(GuardrailViolation):
        validate_answer("El acuerdo ha sido aprobado.", {"POL-COL-2026-01"})
