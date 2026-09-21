# Databricks notebook source

import json

from databricks.sdk import WorkspaceClient
from databricks_mcp.oauth_provider import DatabricksOAuthClientProvider
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
from mcp.types import CallToolRequest, CallToolResult

from config import AI_SEARCH_MCP_PATH


QUERY = (
    "What are the conditions for evaluating a payment arrangement "
    "after a broken payment promise?"
)

TOOL_NAME = "bank_acme__ai__policy_chunks_index"


async def main():
    workspace = WorkspaceClient()
    server_url = f"{workspace.config.host}{AI_SEARCH_MCP_PATH}"

    async with streamablehttp_client(
        url=server_url,
        auth=DatabricksOAuthClientProvider(workspace),
    ) as (read_stream, write_stream, _):

        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            request = CallToolRequest(
                method="tools/call",
                params={
                    "name": TOOL_NAME,
                    "arguments": {
                        "query": QUERY,
                    },
                    "_meta": {
                        "num_results": "3",
                        "filters": json.dumps(
                            {
                                "status": "ACTIVE",
                                "classification": "COLLECTIONS",
                            }
                        ),
                        "query_type": "HYBRID",
                        "columns": (
                            "chunk_id,policy_id,version,effective_date,"
                            "classification,status,file_name,chunk_text"
                        ),
                        "include_score": "true",
                    },
                },
            )

            response = await session.send_request(
                request,
                CallToolResult,
            )

            print(response)


await main()