from pyspark import pipelines as dp
from pyspark.sql import functions as F


def read_csv(file_name: str):
    source_dir = spark.conf.get("structured_source_path")

    return (
        spark.read
        .option("header", True)
        .option("inferSchema", False)
        .csv(f"{source_dir}/{file_name}")
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.col("_metadata.file_path"))
    )


@dp.materialized_view(
    name="customers",
    comment="Raw synthetic customers from Banco ACME fixtures",
)
def customers():
    return read_csv("customers.csv")


@dp.materialized_view(
    name="loans",
    comment="Raw synthetic loans from Banco ACME fixtures",
)
def loans():
    return read_csv("loans.csv")


@dp.materialized_view(
    name="installments",
    comment="Raw synthetic installments from Banco ACME fixtures",
)
def installments():
    return read_csv("installments.csv")


@dp.materialized_view(
    name="payments",
    comment="Raw synthetic payments from Banco ACME fixtures",
)
def payments():
    return read_csv("payments.csv")


@dp.materialized_view(
    name="payment_promises",
    comment="Raw synthetic payment promises from Banco ACME fixtures",
)
def payment_promises():
    return read_csv("payment_promises.csv")


@dp.materialized_view(
    name="payment_arrangements",
    comment="Raw synthetic payment arrangements from Banco ACME fixtures",
)
def payment_arrangements():
    return read_csv("payment_arrangements.csv")


@dp.materialized_view(
    name="customer_interactions",
    comment="Raw synthetic customer interactions from Banco ACME fixtures",
)
def customer_interactions():
    return read_csv("customer_interactions.csv")