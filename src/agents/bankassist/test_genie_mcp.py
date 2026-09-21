# Databricks notebook source

import asyncio
import json

from databricks.sdk import WorkspaceClient
from databricks_langchain import (
    DatabricksMCPServer,
    DatabricksMultiServerMCPClient,
)

from config import GENIE_MCP_PATH


QUERY = """
Analyze customer CUST-001.

What is the customer's delinquency status, outstanding balance,
latest payment, latest payment promise, and latest customer interaction?

Use only structured data.
Do not evaluate payment-arrangement eligibility or apply collection policy.
""".strip()


def parse_tool_result(result):
    text = result[0]["text"]
    return json.loads(text)


async def main():
    workspace = WorkspaceClient()
    host = workspace.config.host

    client = DatabricksMultiServerMCPClient(
        [
            DatabricksMCPServer(
                name="genie",
                url=f"{host}{GENIE_MCP_PATH}",
                workspace_client=workspace,
            )
        ]
    )

    tools = await client.get_tools()

    query_tool = next(
        tool for tool in tools
        if tool.name.startswith("query_space_")
    )

    poll_tool = next(
        tool for tool in tools
        if tool.name.startswith("poll_response_")
    )

    print(f"Calling Genie tool: {query_tool.name}")
    print("=" * 80)

    result = await query_tool.ainvoke({"query": QUERY})
    response = parse_tool_result(result)

    print(f"Initial status: {response['status']}")

    conversation_id = response["conversationId"]
    message_id = response["messageId"]

    while response["status"] not in {
        "COMPLETED",
        "FAILED",
        "CANCELLED",
    }:
        await asyncio.sleep(2)

        result = await poll_tool.ainvoke(
            {
                "conversation_id": conversation_id,
                "message_id": message_id,
            }
        )

        response = parse_tool_result(result)
        print(f"Polling status: {response['status']}")

    print("=" * 80)
    print(json.dumps(response, indent=2, ensure_ascii=False))


await main()