from policy_search import search_active_collections_policies

QUERY = (
    "What are the conditions for evaluating a payment arrangement "
    "after a broken promise?"
)


response = search_active_collections_policies(QUERY)

print("Filtered AI Search results")
print("=" * 80)

manifest_columns = [
    column["name"]
    for column in response["manifest"]["columns"]
]

for row in response["result"]["data_array"]:
    result = dict(zip(manifest_columns, row, strict=True))

    print(f"policy_id:       {result['policy_id']}")
    print(f"version:         {result['version']}")
    print(f"classification:  {result['classification']}")
    print(f"status:          {result['status']}")
    print(f"score:           {result['score']}")
    print("-" * 80)
