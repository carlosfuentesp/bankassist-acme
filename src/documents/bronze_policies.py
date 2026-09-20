from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.materialized_view(
    name="policy_documents",
    comment="Raw Banco ACME policy documents with source metadata",
)
def policy_documents():
    source_path = spark.conf.get("documents_source_path")

    return (
        spark.read
        .format("text")
        .option("wholetext", True)
        .load(f"{source_path}/*.md")
        .select(
            F.col("value").alias("content"),
            F.col("_metadata.file_path").alias("source_path"),
            F.col("_metadata.file_name").alias("file_name"),
            F.current_timestamp().alias("_ingested_at"),
        )
    )