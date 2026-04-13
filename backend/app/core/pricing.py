# USD price per 1M tokens (input, output). Update this table as vendors revise pricing.
PRICING_PER_MILLION: dict[str, tuple[float, float]] = {
    "openai": (0.15, 0.60),
    "claude": (0.25, 1.25),
    "gemini": (0.075, 0.30),
}


def estimate_cost(model_provider: str, input_tokens: int, output_tokens: int) -> float:
    input_price, output_price = PRICING_PER_MILLION.get(model_provider, (0.0, 0.0))
    input_cost = (input_tokens / 1_000_000) * input_price
    output_cost = (output_tokens / 1_000_000) * output_price
    return round(input_cost + output_cost, 8)
