from pyspark.sql import functions as F


source = spark.read.table("bank_acme.ai.policy_chunks")

(
    source
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
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("bank_acme.ai.policy_chunks_source")
)