import asyncio
import json

from databricks.sdk import WorkspaceClient
from databricks_langchain import (
    DatabricksMCPServer,
    DatabricksMultiServerMCPClient,
)
from databricks_mcp.oauth_provider import DatabricksOAuthClientProvider
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
from mcp.types import CallToolRequest, CallToolResult

from config import GENIE_MCP_PATH, AI_SEARCH_MCP_PATH


TERMINAL_GENIE_STATUSES = {
    "COMPLETED",
    "FAILED",
    "CANCELLED",
}


def _parse_langchain_tool_result(result):
    text = result[0]["text"]
    return json.loads(text)


async def _search_active_collections_policy(
    workspace: WorkspaceClient,
    query: str,
):
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
                    "name": "bank_acme__ai__policy_chunks_index",
                    "arguments": {
                        "query": query,
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

            return await session.send_request(
                request,
                CallToolResult,
            )


async def get_bankassist_evidence(
    structured_query: str,
    policy_query: str,
) -> dict:
    workspace = WorkspaceClient()
    host = workspace.config.host

    client = DatabricksMultiServerMCPClient(
        [
            DatabricksMCPServer(
                name="genie",
                url=f"{host}{GENIE_MCP_PATH}",
                workspace_client=workspace,
            ),
        ]
    )

    tools = await client.get_tools()

    genie_query_tool = next(
        tool
        for tool in tools
        if tool.name.startswith("query_space_")
    )

    genie_poll_tool = next(
        tool
        for tool in tools
        if tool.name.startswith("poll_response_")
    )

    genie_result = await genie_query_tool.ainvoke(
        {
            "query": structured_query,
        }
    )

    genie_response = _parse_langchain_tool_result(genie_result)

    while genie_response["status"] not in TERMINAL_GENIE_STATUSES:
        await asyncio.sleep(2)

        poll_result = await genie_poll_tool.ainvoke(
            {
                "conversation_id": genie_response["conversationId"],
                "message_id": genie_response["messageId"],
            }
        )

        genie_response = _parse_langchain_tool_result(poll_result)

    if genie_response["status"] != "COMPLETED":
        raise RuntimeError(
            f"Genie request failed with status: "
            f"{genie_response['status']}"
        )

    policy_response = await _search_active_collections_policy(
        workspace=workspace,
        query=policy_query,
    )

    return {
        "structured_evidence": genie_response,
        "policy_evidence": policy_response,
    }