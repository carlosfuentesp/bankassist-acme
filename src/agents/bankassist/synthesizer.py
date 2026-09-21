import json

from databricks_openai import DatabricksOpenAI

from config import FOUNDATION_MODEL


SYSTEM_PROMPT = """
You are BankAssist, an assistant for authorized Banco ACME collections analysts.

You receive two types of evidence:

1. STRUCTURED EVIDENCE
   Customer, loan, delinquency, payment, promise, arrangement,
   and interaction facts obtained from Banco ACME structured data.

2. POLICY EVIDENCE
   Current Banco ACME collections policy retrieved from authorized
   policy documents.

Rules:

- Use only the evidence provided.
- Never invent customer facts, policy conditions, dates, balances,
  payments, promises, arrangements, or interactions.
- Treat structured evidence as the source of customer facts.
- Treat policy evidence as the source of policy rules.
- Do not use policy rules that are not present in the supplied policy evidence.
- Do not approve a payment arrangement.
- Do not claim that Banco ACME has approved an arrangement.
- Final evaluation and approval remain the responsibility of an authorized
  Banco ACME collections analyst.
- If the evidence is insufficient to answer a part of the question,
  explicitly state that the available evidence is insufficient.
- When applying policy, explain which customer facts correspond to which
  policy conditions.
- Cite the applicable policy using its policy_id, for example:
  [POL-COL-2026-01]
- Do not cite a policy that is not present in the supplied policy evidence.
- Respond in Spanish.
- Be concise but sufficiently detailed for a collections analyst.
""".strip()


def _extract_genie_evidence(structured_response: dict) -> dict:
    content = structured_response.get("content", {})

    return {
        "status": structured_response.get("status"),
        "conversation_id": structured_response.get("conversationId"),
        "message_id": structured_response.get("messageId"),
        "text_answers": content.get("textAttachments", []),
        "query_attachments": content.get("queryAttachments", []),
    }


def _extract_policy_evidence(policy_response) -> list[dict]:
    policies = []

    for item in policy_response.content or []:
        if getattr(item, "type", None) != "text":
            continue

        text = getattr(item, "text", "")

        try:
            parsed = json.loads(text)

            if isinstance(parsed, list):
                policies.extend(parsed)
            elif isinstance(parsed, dict):
                policies.append(parsed)

        except json.JSONDecodeError:
            policies.append(
                {
                    "raw_text": text,
                }
            )

    return policies


def build_context_package(evidence: dict) -> dict:
    return {
        "structured_evidence": _extract_genie_evidence(
            evidence["structured_evidence"]
        ),
        "policy_evidence": _extract_policy_evidence(
            evidence["policy_evidence"]
        ),
    }


def synthesize_bankassist_answer(
    user_question: str,
    evidence: dict,
) -> str:
    context_package = build_context_package(evidence)

    user_prompt = f"""
USER QUESTION
{user_question}

EVIDENCE PACKAGE
{json.dumps(
    context_package,
    indent=2,
    ensure_ascii=False,
    default=str,
)}

Produce the final BankAssist answer using only this evidence.
""".strip()

    client = DatabricksOpenAI()

    response = client.chat.completions.create(
        model=FOUNDATION_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.0,
        max_tokens=1000,
    )

    return response.choices[0].message.content