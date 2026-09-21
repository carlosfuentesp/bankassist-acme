from pyspark import pipelines as dp
from pyspark.sql import functions as F

from contracts.expectations import (
    CUSTOMER_INTERACTIONS_EXPECTATIONS,
    CUSTOMERS_EXPECTATIONS,
    INSTALLMENTS_EXPECTATIONS,
    LOANS_EXPECTATIONS,
    PAYMENT_ARRANGEMENTS_EXPECTATIONS,
    PAYMENT_PROMISES_EXPECTATIONS,
    PAYMENTS_EXPECTATIONS,
)


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


@dp.materialized_view(
    name="loans",
    comment="Validated and typed Banco ACME loans",
)
@dp.expect_all(LOANS_EXPECTATIONS)
def loans():
    return (
        spark.read.table("bank_acme.bronze.loans")
        .select(
            F.col("loan_id").cast("string").alias("loan_id"),
            F.col("customer_id").cast("string").alias("customer_id"),
            F.col("product_type").cast("string").alias("product_type"),
            F.col("original_amount").cast("decimal(12,2)").alias("original_amount"),
            F.col("outstanding_balance").cast("decimal(12,2)").alias("outstanding_balance"),
            F.col("days_past_due").cast("int").alias("days_past_due"),
            F.col("status").cast("string").alias("status"),
            F.to_date("snapshot_date").alias("snapshot_date"),
            F.col("_ingested_at"),
            F.col("_source_file"),
        )
    )


@dp.materialized_view(
    name="installments",
    comment="Validated and typed Banco ACME installments",
)
@dp.expect_all(INSTALLMENTS_EXPECTATIONS)
def installments():
    return (
        spark.read.table("bank_acme.bronze.installments")
        .select(
            F.col("installment_id").cast("string").alias("installment_id"),
            F.col("loan_id").cast("string").alias("loan_id"),
            F.to_date("due_date").alias("due_date"),
            F.col("amount_due").cast("decimal(12,2)").alias("amount_due"),
            F.col("amount_paid").cast("decimal(12,2)").alias("amount_paid"),
            F.col("status").cast("string").alias("status"),
            F.col("_ingested_at"),
            F.col("_source_file"),
        )
    )


@dp.materialized_view(
    name="payments",
    comment="Validated and typed Banco ACME payments",
)
@dp.expect_all(PAYMENTS_EXPECTATIONS)
def payments():
    return (
        spark.read.table("bank_acme.bronze.payments")
        .select(
            F.col("payment_id").cast("string").alias("payment_id"),
            F.col("loan_id").cast("string").alias("loan_id"),
            F.to_timestamp("payment_date").alias("payment_date"),
            F.col("amount").cast("decimal(12,2)").alias("amount"),
            F.col("channel").cast("string").alias("channel"),
            F.col("_ingested_at"),
            F.col("_source_file"),
        )
    )


@dp.materialized_view(
    name="payment_promises",
    comment="Validated and typed Banco ACME payment promises",
)
@dp.expect_all(PAYMENT_PROMISES_EXPECTATIONS)
def payment_promises():
    return (
        spark.read.table("bank_acme.bronze.payment_promises")
        .select(
            F.col("promise_id").cast("string").alias("promise_id"),
            F.col("customer_id").cast("string").alias("customer_id"),
            F.to_date("promise_date").alias("promise_date"),
            F.to_date("promised_payment_date").alias("promised_payment_date"),
            F.col("promised_amount").cast("decimal(12,2)").alias("promised_amount"),
            F.col("status").cast("string").alias("status"),
            F.col("_ingested_at"),
            F.col("_source_file"),
        )
    )


@dp.materialized_view(
    name="payment_arrangements",
    comment="Validated and typed Banco ACME payment arrangements",
)
@dp.expect_all(PAYMENT_ARRANGEMENTS_EXPECTATIONS)
def payment_arrangements():
    return (
        spark.read.table("bank_acme.bronze.payment_arrangements")
        .select(
            F.col("arrangement_id").cast("string").alias("arrangement_id"),
            F.col("customer_id").cast("string").alias("customer_id"),
            F.to_date("arrangement_date").alias("arrangement_date"),
            F.col("status").cast("string").alias("status"),
            F.col("_ingested_at"),
            F.col("_source_file"),
        )
    )


@dp.materialized_view(
    name="customer_interactions",
    comment="Validated and typed Banco ACME customer interactions",
)
@dp.expect_all(CUSTOMER_INTERACTIONS_EXPECTATIONS)
def customer_interactions():
    return (
        spark.read.table("bank_acme.bronze.customer_interactions")
        .select(
            F.col("interaction_id").cast("string").alias("interaction_id"),
            F.col("customer_id").cast("string").alias("customer_id"),
            F.to_timestamp("interaction_ts").alias("interaction_ts"),
            F.col("channel").cast("string").alias("channel"),
            F.col("notes").cast("string").alias("notes"),
            F.col("_ingested_at"),
            F.col("_source_file"),
        )
    )