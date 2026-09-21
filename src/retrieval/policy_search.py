from databricks.ai_search.client import AISearchClient


ENDPOINT_NAME = "bankassist-acme-ai-search-dev"
INDEX_NAME = "bank_acme.ai.policy_chunks_index"


def search_active_collections_policies(
    query: str,
    num_results: int = 3,
) -> dict:
    client = AISearchClient()

    index = client.get_index(
        endpoint_name=ENDPOINT_NAME,
        index_name=INDEX_NAME,
    )

    return index.similarity_search(
        query_text=query,
        query_type="HYBRID",
        columns=[
            "chunk_id",
            "policy_id",
            "version",
            "effective_date",
            "classification",
            "status",
            "file_name",
            "chunk_text",
        ],
        filters={
            "status": "ACTIVE",
            "classification": "COLLECTIONS",
        },
        num_results=num_results,
    )