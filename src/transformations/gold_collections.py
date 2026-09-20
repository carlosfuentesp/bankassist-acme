from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.materialized_view(
    name="customer_collections_snapshot",
    comment="Business-ready collections snapshot for Banco ACME consumer loans",
)
def customer_collections_snapshot():
    customers = spark.read.table("bank_acme.silver.customers")
    loans = spark.read.table("bank_acme.silver.loans")
    payments = spark.read.table("bank_acme.silver.payments")
    promises = spark.read.table("bank_acme.silver.payment_promises")
    arrangements = spark.read.table("bank_acme.silver.payment_arrangements")
    interactions = spark.read.table("bank_acme.silver.customer_interactions")

    latest_payment = (
        payments
        .groupBy("loan_id")
        .agg(
            F.max_by(
                F.struct(
                    "payment_date",
                    "amount",
                    "channel",
                ),
                "payment_date",
            ).alias("latest_payment")
        )
    )

    latest_promise = (
        promises
        .groupBy("customer_id")
        .agg(
            F.max_by(
                F.struct(
                    "promise_date",
                    "promised_payment_date",
                    "promised_amount",
                    "status",
                ),
                "promise_date",
            ).alias("latest_promise")
        )
    )

    latest_arrangement = (
        arrangements
        .groupBy("customer_id")
        .agg(
            F.max("arrangement_date").alias("latest_arrangement_date")
        )
    )

    latest_interaction = (
        interactions
        .groupBy("customer_id")
        .agg(
            F.max_by(
                F.struct(
                    "interaction_ts",
                    "channel",
                    "notes",
                ),
                "interaction_ts",
            ).alias("latest_interaction")
        )
    )

    return (
        loans
        .join(customers, on="customer_id", how="inner")
        .join(latest_payment, on="loan_id", how="left")
        .join(latest_promise, on="customer_id", how="left")
        .join(latest_arrangement, on="customer_id", how="left")
        .join(latest_interaction, on="customer_id", how="left")
        .select(
            "customer_id",
            "full_name",
            "city",
            "customer_segment",
            "loan_id",
            "product_type",
            "original_amount",
            "outstanding_balance",
            "days_past_due",
            F.col("loans.status").alias("loan_status"),
            "snapshot_date",

            F.col("latest_payment.payment_date")
                .alias("latest_payment_date"),
            F.col("latest_payment.amount")
                .alias("latest_payment_amount"),
            F.col("latest_payment.channel")
                .alias("latest_payment_channel"),

            F.col("latest_promise.promise_date")
                .alias("latest_promise_date"),
            F.col("latest_promise.promised_payment_date")
                .alias("latest_promised_payment_date"),
            F.col("latest_promise.promised_amount")
                .alias("latest_promised_amount"),
            F.col("latest_promise.status")
                .alias("latest_promise_status"),

            "latest_arrangement_date",

            F.col("latest_interaction.interaction_ts")
                .alias("latest_interaction_ts"),
            F.col("latest_interaction.channel")
                .alias("latest_interaction_channel"),
            F.col("latest_interaction.notes")
                .alias("latest_interaction_notes"),
        )
    )