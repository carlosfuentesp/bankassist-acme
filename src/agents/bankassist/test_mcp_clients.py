# Databricks notebook source

import asyncio

from databricks.sdk import WorkspaceClient
from databricks_langchain import (
    DatabricksMCPServer,
    DatabricksMultiServerMCPClient,
)

from config import GENIE_MCP_PATH, AI_SEARCH_MCP_PATH


async def main():
    workspace = WorkspaceClient()
    host = workspace.config.host

    client = DatabricksMultiServerMCPClient(
        [
            DatabricksMCPServer(
                name="genie",
                url=f"{host}{GENIE_MCP_PATH}",
                workspace_client=workspace,
            ),
            DatabricksMCPServer(
                name="ai-search",
                url=f"{host}{AI_SEARCH_MCP_PATH}",
                workspace_client=workspace,
            ),
        ]
    )

    tools = await client.get_tools()

    print("AVAILABLE MCP TOOLS")
    print("=" * 80)

    for tool in tools:
        print(f"name: {tool.name}")
        print(f"description: {tool.description}")
        print(f"args_schema: {tool.args_schema}")
        print("-" * 80)


await main()