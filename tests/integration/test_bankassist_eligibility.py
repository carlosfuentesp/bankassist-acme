import asyncio

from agents.bankassist.orchestrator import get_bankassist_evidence
from agents.bankassist.synthesizer import synthesize_bankassist_answer

USER_QUESTION = """
¿Qué clientes con créditos de consumo entre 31 y 60 días de mora
incumplieron una promesa de pago y cumplen las condiciones de Banco ACME
para ser evaluados para un acuerdo de pago?
""".strip()


STRUCTURED_QUERY = """
Find customers who satisfy all of these structured-data conditions:

- product type is CONSUMER_LOAN
- days past due are between 31 and 60
- latest payment promise status is BROKEN

For each matching customer, return:

- customer_id
- customer_name
- product_type
- days_past_due
- outstanding_balance
- latest_promise_status
- latest_arrangement_date
- snapshot_date

Use only structured data.

Do not apply Banco ACME policy eligibility rules.
Do not approve or recommend a payment arrangement.
""".strip()


POLICY_QUERY = """
What does the current Banco ACME collections policy say about evaluating
a customer with a BROKEN payment promise for a payment arrangement?

Return all eligibility conditions, including:

- product type
- days past due
- outstanding balance
- previous payment arrangements
- the applicable lookback period
- who has final approval responsibility
""".strip()


async def main():
    print("Collecting BankAssist evidence...")
    print("=" * 80)

    evidence = await get_bankassist_evidence(
        structured_query=STRUCTURED_QUERY,
        policy_query=POLICY_QUERY,
    )

    print("Structured and policy evidence collected.")
    print()
    print("Calling foundation model...")
    print("=" * 80)

    answer, usage = synthesize_bankassist_answer(
        user_question=USER_QUESTION,
        evidence=evidence,
    )

    print()
    print("BANKASSIST ELIGIBILITY ANSWER")
    print("=" * 80)
    print(answer)
    print(f"Model usage: {usage}")


if __name__ == "__main__":
    asyncio.run(main())
