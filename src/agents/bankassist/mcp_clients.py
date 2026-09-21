from databricks.sdk import WorkspaceClient
from databricks_mcp import DatabricksMCPClient

from agents.bankassist.config import AI_SEARCH_MCP_PATH, GENIE_MCP_PATH


def _workspace_client() -> WorkspaceClient:
    return WorkspaceClient()


def get_genie_mcp_client() -> DatabricksMCPClient:
    workspace = _workspace_client()

    return DatabricksMCPClient(
        server_url=f"{workspace.config.host}{GENIE_MCP_PATH}",
        workspace_client=workspace,
    )


def get_ai_search_mcp_client() -> DatabricksMCPClient:
    workspace = _workspace_client()

    return DatabricksMCPClient(
        server_url=f"{workspace.config.host}{AI_SEARCH_MCP_PATH}",
        workspace_client=workspace,
    )
