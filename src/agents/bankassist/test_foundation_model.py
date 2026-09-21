# Databricks notebook source

from databricks_openai import DatabricksOpenAI

from config import FOUNDATION_MODEL


def main():
    client = DatabricksOpenAI()

    response = client.chat.completions.create(
        model=FOUNDATION_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a concise assistant. "
                    "Respond in Spanish."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Responde exactamente con una frase indicando "
                    "que el modelo de BankAssist está operativo."
                ),
            },
        ],
        temperature=0.0,
        max_tokens=100,
    )

    print("FOUNDATION MODEL TEST")
    print("=" * 80)
    print(f"model: {FOUNDATION_MODEL}")
    print()
    print(response.choices[0].message.content)

    if response.usage:
        print()
        print("TOKEN USAGE")
        print("=" * 80)
        print(f"prompt_tokens:     {response.usage.prompt_tokens}")
        print(f"completion_tokens: {response.usage.completion_tokens}")
        print(f"total_tokens:      {response.usage.total_tokens}")


main()