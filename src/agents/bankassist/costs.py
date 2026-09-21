"""Transparent per-question cost estimates using configurable rates."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from agents.bankassist.config import (
    AI_SEARCH_USD_PER_QUERY,
    GENIE_USD_PER_QUERY,
    MODEL_INPUT_USD_PER_MILLION,
    MODEL_OUTPUT_USD_PER_MILLION,
)


@dataclass(frozen=True)
class CostEstimate:
    input_tokens: int
    output_tokens: int
    genie_queries: int
    ai_search_queries: int
    estimated_usd: float
    configured: bool

    def to_dict(self) -> dict:
        return asdict(self)


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    genie_queries: int = 1,
    ai_search_queries: int = 1,
) -> CostEstimate:
    rates = (
        MODEL_INPUT_USD_PER_MILLION,
        MODEL_OUTPUT_USD_PER_MILLION,
        GENIE_USD_PER_QUERY,
        AI_SEARCH_USD_PER_QUERY,
    )
    total = (
        input_tokens * MODEL_INPUT_USD_PER_MILLION / 1_000_000
        + output_tokens * MODEL_OUTPUT_USD_PER_MILLION / 1_000_000
        + genie_queries * GENIE_USD_PER_QUERY
        + ai_search_queries * AI_SEARCH_USD_PER_QUERY
    )
    return CostEstimate(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        genie_queries=genie_queries,
        ai_search_queries=ai_search_queries,
        estimated_usd=round(total, 6),
        configured=any(rate > 0 for rate in rates),
    )
