# Databricks notebook source

from databricks.sdk import WorkspaceClient
from databricks_langchain import (
    DatabricksMCPServer,
    DatabricksMultiServerMCPClient,
)

from config import AI_SEARCH_MCP_PATH


QUERY = (
    "What are the conditions for evaluating a payment arrangement "
    "after a broken payment promise?"
)


async def main():
    workspace = WorkspaceClient()
    host = workspace.config.host

    client = DatabricksMultiServerMCPClient(
        [
            DatabricksMCPServer(
                name="ai-search",
                url=f"{host}{AI_SEARCH_MCP_PATH}",
                workspace_client=workspace,
            )
        ]
    )

    tools = await client.get_tools()

    search_tool = next(
        tool
        for tool in tools
        if tool.name == "bank_acme__ai__policy_chunks_index"
    )

    print(f"Calling AI Search tool: {search_tool.name}")
    print("=" * 80)

    result = await search_tool.ainvoke(
        {
            "query": QUERY,
        }
    )

    print(result)


await main()