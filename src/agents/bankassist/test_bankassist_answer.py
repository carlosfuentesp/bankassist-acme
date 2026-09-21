# Databricks notebook source

from orchestrator import get_bankassist_evidence
from synthesizer import synthesize_bankassist_answer


USER_QUESTION = """
Analiza al cliente CUST-001.

¿Cuál es su situación de mora, qué pagos y promesas registra
y qué opciones puede evaluar el analista según la política vigente
de Banco ACME?
""".strip()


STRUCTURED_QUERY = """
Analyze customer CUST-001.

Return the customer's:
- delinquency status
- days past due
- outstanding balance
- latest payment
- latest payment promise
- latest payment arrangement
- latest customer interaction

Use only structured data.

Do not determine policy eligibility.
Do not approve or recommend a payment arrangement.
""".strip()


POLICY_QUERY = """
What does the current Banco ACME collections policy say about:

1. A customer with an ACTIVE payment promise whose promised
   payment date has not yet passed.
2. Whether a new payment arrangement should be initiated
   while that promise remains valid.
3. Who has final responsibility for approving a payment arrangement.
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

    answer = synthesize_bankassist_answer(
        user_question=USER_QUESTION,
        evidence=evidence,
    )

    print()
    print("BANKASSIST FINAL ANSWER")
    print("=" * 80)
    print(answer)


await main()