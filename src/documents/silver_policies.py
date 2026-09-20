from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.materialized_view(
    name="policy_documents",
    comment="Parsed Banco ACME policy documents with retrieval metadata",
)
def policy_documents():
    source = spark.read.table("bank_acme.bronze.policy_documents")

    return (
        source
        .select(
            F.trim(
                F.regexp_extract(
                    "content",
                    r"(?m)^Policy ID:\s*([^\r\n]+)",
                    1,
                )
            ).alias("policy_id"),

            F.trim(
                F.regexp_extract(
                    "content",
                    r"(?m)^Version:\s*([^\r\n]+)",
                    1,
                )
            ).alias("version"),

            F.to_date(
                F.regexp_extract(
                    "content",
                    r"(?m)^Effective from:\s*(\d{4}-\d{2}-\d{2})",
                    1,
                )
            ).alias("effective_date"),

            F.trim(
                F.regexp_extract(
                    "content",
                    r"(?m)^Classification:\s*([^\r\n]+)",
                    1,
                )
            ).alias("classification"),

            F.trim(
                F.regexp_extract(
                    "content",
                    r"(?m)^Status:\s*([^\r\n]+)",
                    1,
                )
            ).alias("status"),

            F.col("file_name"),
            F.col("source_path"),
            F.col("content"),
            F.col("_ingested_at"),
        )
    )