CUSTOMERS_EXPECTATIONS = {
    "customer_id_not_null": "customer_id IS NOT NULL",
    "valid_customer_segment": "customer_segment IN ('MASS', 'AFFLUENT')",
}

LOANS_EXPECTATIONS = {
    "loan_id_not_null": "loan_id IS NOT NULL",
    "customer_id_not_null": "customer_id IS NOT NULL",
    "valid_product_type": "product_type = 'CONSUMER_LOAN'",
    "positive_original_amount": "original_amount > 0",
    "non_negative_outstanding_balance": "outstanding_balance >= 0",
    "non_negative_days_past_due": "days_past_due >= 0",
    "valid_loan_status": "status IN ('CURRENT', 'PAST_DUE')",
}

INSTALLMENTS_EXPECTATIONS = {
    "installment_id_not_null": "installment_id IS NOT NULL",
    "loan_id_not_null": "loan_id IS NOT NULL",
    "positive_amount_due": "amount_due > 0",
    "non_negative_amount_paid": "amount_paid >= 0",
    "valid_installment_status": "status IN ('PAID', 'PARTIAL', 'OVERDUE', 'PENDING')",
}

PAYMENTS_EXPECTATIONS = {
    "payment_id_not_null": "payment_id IS NOT NULL",
    "loan_id_not_null": "loan_id IS NOT NULL",
    "positive_payment_amount": "amount > 0",
    "valid_payment_channel": (
        "channel IN ('MOBILE_BANKING', 'TRANSFER', 'BRANCH', 'AUTO_DEBIT')"
    ),
}

PAYMENT_PROMISES_EXPECTATIONS = {
    "promise_id_not_null": "promise_id IS NOT NULL",
    "customer_id_not_null": "customer_id IS NOT NULL",
    "positive_promised_amount": "promised_amount > 0",
    "valid_promise_status": "status IN ('ACTIVE', 'KEPT', 'BROKEN')",
}

PAYMENT_ARRANGEMENTS_EXPECTATIONS = {
    "arrangement_id_not_null": "arrangement_id IS NOT NULL",
    "customer_id_not_null": "customer_id IS NOT NULL",
    "valid_arrangement_status": "status IN ('ACTIVE', 'COMPLETED', 'BROKEN')",
}

CUSTOMER_INTERACTIONS_EXPECTATIONS = {
    "interaction_id_not_null": "interaction_id IS NOT NULL",
    "customer_id_not_null": "customer_id IS NOT NULL",
    "valid_interaction_channel": "channel IN ('PHONE', 'WHATSAPP', 'EMAIL')",
}