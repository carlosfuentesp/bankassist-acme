from agents.bankassist.eligibility import evaluate_candidate


def candidate(**overrides):
    row = {
        "customer_id": "CUST-002",
        "product_type": "CONSUMER_LOAN",
        "days_past_due": 48,
        "outstanding_balance": "1800.00",
        "latest_promise_status": "BROKEN",
        "latest_arrangement_date": None,
        "snapshot_date": "2026-09-19",
    }
    row.update(overrides)
    return row


def test_cust_002_is_eligible_for_human_evaluation():
    result = evaluate_candidate(candidate())
    assert result.eligible_for_evaluation is True
    assert result.decision == "ELIGIBLE_FOR_EVALUATION"


def test_cust_001_active_promise_is_not_eligible():
    result = evaluate_candidate(
        candidate(customer_id="CUST-001", latest_promise_status="ACTIVE", days_past_due=42)
    )
    assert result.eligible_for_evaluation is False
    assert result.checks["broken_payment_promise"] is False


def test_cust_003_recent_arrangement_is_not_eligible():
    result = evaluate_candidate(
        candidate(
            customer_id="CUST-003",
            days_past_due=37,
            outstanding_balance="2100.00",
            latest_arrangement_date="2026-08-10",
        )
    )
    assert result.eligible_for_evaluation is False
    assert result.checks["no_arrangement_in_previous_90_days"] is False


def test_ninety_day_boundary_is_not_eligible():
    result = evaluate_candidate(candidate(latest_arrangement_date="2026-06-21"))
    assert result.eligible_for_evaluation is False


def test_day_91_is_eligible():
    result = evaluate_candidate(candidate(latest_arrangement_date="2026-06-20"))
    assert result.eligible_for_evaluation is True


def test_missing_snapshot_fails_closed():
    result = evaluate_candidate(candidate(snapshot_date=None))
    assert result.eligible_for_evaluation is False
