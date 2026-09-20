from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.materialized_view(
    name="policy_chunks",
    comment="Section-based chunks of Banco ACME policy documents for retrieval",
)
def policy_chunks():
    policies = spark.read.table("bank_acme.silver.policy_documents")

    sections = (
        policies
        .withColumn(
            "sections",
            F.split(
                F.regexp_replace("content", r"\r\n", "\n"),
                r"(?m)(?=^##\s+)",
            ),
        )
        .select(
            "policy_id",
            "version",
            "effective_date",
            "classification",
            "status",
            "file_name",
            "source_path",
            F.posexplode("sections").alias("chunk_index", "chunk_text"),
        )
        .filter(F.length(F.trim("chunk_text")) >= 40)
    )

    return (
        sections
        .withColumn("chunk_text", F.trim("chunk_text"))
        .withColumn(
            "chunk_id",
            F.concat_ws(
                "::",
                F.col("policy_id"),
                F.format_string("%03d", F.col("chunk_index")),
            ),
        )
        .select(
            "chunk_id",
            "policy_id",
            "version",
            "effective_date",
            "classification",
            "status",
            "file_name",
            "source_path",
            "chunk_index",
            "chunk_text",
        )
    )