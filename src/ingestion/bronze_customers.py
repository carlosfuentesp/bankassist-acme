from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.materialized_view(
    name="customers",
    comment="Raw synthetic customers from Banco ACME fixtures"
)
def customers():
    return (
        spark.read
        .option("header", True)
        .option("inferSchema", False)
        .csv(spark.conf.get("customers_source_path"))
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.col("_metadata.file_path"))
    )