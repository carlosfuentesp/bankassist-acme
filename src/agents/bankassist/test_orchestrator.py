# Databricks notebook source

import json

from orchestrator import get_bankassist_evidence


STRUCTURED_QUERY = """
Analyze customer CUST-001.

What is the customer's delinquency status, outstanding balance,
latest payment, latest payment promise, and latest customer interaction?

Use only structured data.
Do not evaluate payment-arrangement eligibility or apply collection policy.
""".strip()


POLICY_QUERY = """
What does the current Banco ACME collections policy say about a customer
with an active payment promise that has not yet reached its promised payment date?

Also state whether a new payment arrangement should be initiated.
""".strip()


def extract_policy_text(policy_response):
    if not policy_response.content:
        return []

    results = []

    for content_item in policy_response.content:
        if content_item.type != "text":
            continue

        try:
            parsed = json.loads(content_item.text)
            results.extend(parsed)
        except json.JSONDecodeError:
            results.append(
                {
                    "raw_text": content_item.text,
                }
            )

    return results


async def main():
    evidence = await get_bankassist_evidence(
        structured_query=STRUCTURED_QUERY,
        policy_query=POLICY_QUERY,
    )

    structured = evidence["structured_evidence"]
    policies = extract_policy_text(
        evidence["policy_evidence"]
    )

    print("\nSTRUCTURED EVIDENCE — GENIE")
    print("=" * 80)
    print(f"status: {structured['status']}")
    print(f"conversation_id: {structured['conversationId']}")
    print(f"message_id: {structured['messageId']}")

    print("\nGenie answer:")
    for attachment in structured["content"].get(
        "textAttachments",
        [],
    ):
        print(attachment)

    print("\nPOLICY EVIDENCE — AI SEARCH")
    print("=" * 80)

    for policy in policies:
        print(f"policy_id:       {policy.get('policy_id')}")
        print(f"version:         {policy.get('version')}")
        print(f"effective_date:  {policy.get('effective_date')}")
        print(f"classification:  {policy.get('classification')}")
        print(f"status:          {policy.get('status')}")
        print(f"score:           {policy.get('score')}")
        print()

        print(policy.get("chunk_text"))
        print("-" * 80)


await main()