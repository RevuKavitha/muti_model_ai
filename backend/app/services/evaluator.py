from app.services.providers import ProviderResult, judge_with_openai
from app.utils.text_utils import extract_keywords, tokenize
from typing import Optional


def length_score(text: str) -> float:
    words = len(tokenize(text))
    if words == 0:
        return 0.0
    if 60 <= words <= 220:
        return 100.0
    if words < 60:
        return round((words / 60) * 100, 2)
    # Penalize verbosity above 220 words.
    penalty = min((words - 220) * 0.25, 100)
    return round(max(0, 100 - penalty), 2)


def keyword_match_score(prompt: str, response: str) -> float:
    keywords = extract_keywords(prompt)
    if not keywords:
        return 100.0

    response_tokens = set(tokenize(response))
    matched = sum(1 for k in keywords if k in response_tokens)
    return round((matched / len(keywords)) * 100, 2)


async def score_results(
    prompt: str,
    provider_results: list[ProviderResult],
    use_judge: bool = False,
) -> dict[str, dict[str, Optional[float]]]:
    judge_scores: dict[str, float] = {}
    if use_judge:
        judge_inputs = [(r.model_key, r.response) for r in provider_results if r.response and not r.error]
        judge_scores = await judge_with_openai(prompt, judge_inputs)

    scored: dict[str, dict[str, Optional[float]]] = {}
    for r in provider_results:
        l_score = length_score(r.response)
        k_score = keyword_match_score(prompt, r.response)
        j_score = judge_scores.get(r.model_key)

        # Weighted scoring. LLM-as-judge boosts quality ranking when enabled.
        if j_score is not None:
            total = round((0.2 * l_score) + (0.3 * k_score) + (0.5 * j_score), 2)
        else:
            total = round((0.4 * l_score) + (0.6 * k_score), 2)

        scored[r.model_key] = {
            "length_score": l_score,
            "keyword_score": k_score,
            "judge_score": j_score,
            "total": total,
        }

    return scored
