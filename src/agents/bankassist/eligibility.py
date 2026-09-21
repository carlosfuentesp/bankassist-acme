"""Deterministic, fail-closed policy checks for payment-arrangement evaluation."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any


@dataclass(frozen=True)
class CollectionsPolicy:
    policy_id: str = "POL-COL-2026-01"
    product_type: str = "CONSUMER_LOAN"
    min_days_past_due: int = 31
    max_days_past_due: int = 60
    max_outstanding_balance: Decimal = Decimal("2500.00")
    arrangement_lookback_days: int = 90


@dataclass(frozen=True)
class EligibilityAssessment:
    customer_id: str
    eligible_for_evaluation: bool
    decision: str
    checks: dict[str, bool]
    reasons: list[str]
    policy_id: str
    snapshot_date: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _as_date(value: Any) -> date | None:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _as_decimal(value: Any) -> Decimal | None:
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def evaluate_candidate(
    row: dict[str, Any],
    policy: CollectionsPolicy | None = None,
) -> EligibilityAssessment:
    """Apply the active policy without guessing missing values.

    The result is eligibility *for analyst evaluation*, never approval.
    Missing or malformed evidence fails closed and is reported explicitly.
    """

    policy = policy or CollectionsPolicy()
    customer_id = str(row.get("customer_id") or "UNKNOWN")
    snapshot = _as_date(row.get("snapshot_date"))
    arrangement = _as_date(row.get("latest_arrangement_date"))
    balance = _as_decimal(row.get("outstanding_balance"))

    try:
        dpd = int(row["days_past_due"])
    except (KeyError, TypeError, ValueError):
        dpd = None

    checks = {
        "consumer_loan": row.get("product_type") == policy.product_type,
        "days_past_due_31_to_60": dpd is not None
        and policy.min_days_past_due <= dpd <= policy.max_days_past_due,
        "broken_payment_promise": row.get("latest_promise_status") == "BROKEN",
        "balance_at_or_below_2500": balance is not None
        and balance <= policy.max_outstanding_balance,
        "no_arrangement_in_previous_90_days": False,
    }

    if snapshot is not None:
        if arrangement is None:
            checks["no_arrangement_in_previous_90_days"] = True
        else:
            age_days = (snapshot - arrangement).days
            checks["no_arrangement_in_previous_90_days"] = (
                age_days > policy.arrangement_lookback_days
            )

    labels = {
        "consumer_loan": "el producto no es un crédito de consumo",
        "days_past_due_31_to_60": "la mora no está entre 31 y 60 días",
        "broken_payment_promise": "la última promesa no consta como incumplida",
        "balance_at_or_below_2500": "el saldo falta o supera USD 2.500",
        "no_arrangement_in_previous_90_days": (
            "falta snapshot_date o existe un acuerdo dentro de los 90 días anteriores"
        ),
    }
    reasons = [labels[name] for name, passed in checks.items() if not passed]
    eligible = all(checks.values())

    return EligibilityAssessment(
        customer_id=customer_id,
        eligible_for_evaluation=eligible,
        decision="ELIGIBLE_FOR_EVALUATION" if eligible else "NOT_ELIGIBLE_FOR_EVALUATION",
        checks=checks,
        reasons=reasons,
        policy_id=policy.policy_id,
        snapshot_date=snapshot.isoformat() if snapshot else None,
    )


def evaluate_candidates(
    rows: Iterable[dict[str, Any]],
    policy: CollectionsPolicy | None = None,
) -> list[dict[str, Any]]:
    return [evaluate_candidate(row, policy).to_dict() for row in rows]
