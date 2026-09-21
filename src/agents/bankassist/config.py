import os

GENIE_SPACE_ID = os.getenv(
    "BANKASSIST_GENIE_SPACE_ID",
    "01f1b55197c11b7995b4599d90badc02",
)

GENIE_MCP_PATH = (
    f"/api/2.0/mcp/genie/{GENIE_SPACE_ID}"
)

AI_SEARCH_INDEX = os.getenv(
    "BANKASSIST_AI_SEARCH_INDEX",
    "bank_acme.ai.policy_chunks_index",
)

AI_SEARCH_MCP_PATH = "/api/2.0/mcp/ai-search/" + AI_SEARCH_INDEX.replace(".", "/")

FOUNDATION_MODEL = os.getenv(
    "BANKASSIST_FOUNDATION_MODEL",
    "databricks-qwen3-next-80b-a3b-instruct",
)

MAX_GENIE_POLLS = int(os.getenv("BANKASSIST_MAX_GENIE_POLLS", "60"))
GENIE_POLL_SECONDS = float(os.getenv("BANKASSIST_GENIE_POLL_SECONDS", "2"))

# Rates are deliberately configurable: workspace pricing and model rates vary.
MODEL_INPUT_USD_PER_MILLION = float(
    os.getenv("BANKASSIST_MODEL_INPUT_USD_PER_MILLION", "0")
)
MODEL_OUTPUT_USD_PER_MILLION = float(
    os.getenv("BANKASSIST_MODEL_OUTPUT_USD_PER_MILLION", "0")
)
GENIE_USD_PER_QUERY = float(os.getenv("BANKASSIST_GENIE_USD_PER_QUERY", "0"))
AI_SEARCH_USD_PER_QUERY = float(os.getenv("BANKASSIST_AI_SEARCH_USD_PER_QUERY", "0"))
