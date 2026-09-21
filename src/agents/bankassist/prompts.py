DEFAULT_QUESTION = """
¿Qué clientes con créditos de consumo entre 31 y 60 días de mora
incumplieron una promesa de pago y cumplen las condiciones de Banco ACME
para ser evaluados para un acuerdo de pago?
""".strip()

STRUCTURED_QUERY = """
Find customers who satisfy all of these structured-data conditions:
- product type is CONSUMER_LOAN
- days past due are between 31 and 60
- latest payment promise status is BROKEN

Return customer_id, full_name, loan_id, product_type, days_past_due,
outstanding_balance, latest_promise_status, latest_arrangement_date and snapshot_date.
Use only structured data. Do not apply policy rules or approve an arrangement.
""".strip()

POLICY_QUERY = """
What does the current Banco ACME collections policy say about evaluating a customer
with a BROKEN payment promise for a payment arrangement? Return every eligibility
condition, the lookback period and who holds final approval responsibility.
""".strip()
