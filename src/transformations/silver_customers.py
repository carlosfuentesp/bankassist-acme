from pyspark import pipelines as dp
from pyspark.sql import functions as F

from contracts.expectations import CUSTOMERS_EXPECTATIONS


@dp.materialized_view(
    name="customers",
    comment="Validated and typed Banco ACME customers",
)
@dp.expect_all(CUSTOMERS_EXPECTATIONS)
def customers():
    return (
        spark.read.table("bank_acme.bronze.customers")
        .select(
            F.col("customer_id").cast("string").alias("customer_id"),
            F.col("full_name").cast("string").alias("full_name"),
            F.col("city").cast("string").alias("city"),
            F.col("customer_segment").cast("string").alias("customer_segment"),
            F.col("_ingested_at"),
            F.col("_source_file"),
        )
    )