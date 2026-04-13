from collections import defaultdict
import asyncio
from typing import Optional, Union
from uuid import uuid4

from app.core.pricing import estimate_cost
from app.schemas import CompareResponse, ModelResult
from app.services.evaluator import score_results
from app.services.providers import ProviderService
from app.services.storage import ExportRow, run_store


async def run_compare(
    prompt: str,
    models: list[str],
    use_judge: bool = False,
    run_id: Optional[str] = None,
    persist: bool = True,
) -> tuple[CompareResponse, list[ExportRow]]:
    local_run_id = run_id or str(uuid4())
    provider_results = await ProviderService.run_selected(models, prompt)
    score_map = await score_results(prompt, provider_results, use_judge=use_judge)

    normalized: list[ModelResult] = []
    export_rows: list[ExportRow] = []
    for r in provider_results:
        scores = score_map.get(r.model_key, {})
        cost = estimate_cost(r.provider, r.input_tokens, r.output_tokens)

        item = ModelResult(
            model=r.model_key,
            provider=r.provider,
            provider_model=r.provider_model,
            response=r.response,
            time=r.latency,
            tokens=r.total_tokens,
            input_tokens=r.input_tokens,
            output_tokens=r.output_tokens,
            cost=cost,
            score=float(scores.get("total", 0.0)),
            length_score=float(scores.get("length_score", 0.0)),
            keyword_score=float(scores.get("keyword_score", 0.0)),
            judge_score=scores.get("judge_score"),
            error=r.error,
        )
        normalized.append(item)

        export_rows.append(
            ExportRow(
                run_id=local_run_id,
                prompt=prompt,
                model_name=r.model_key,
                response=r.response if not r.error else f"ERROR: {r.error}",
                time_taken=r.latency,
                token_usage=r.total_tokens,
                cost=cost,
                score=item.score,
            )
        )

    valid = [r for r in normalized if r.error is None]
    best_model = max(valid, key=lambda x: x.score).model if valid else None
    fastest_model = min(valid, key=lambda x: x.time).model if valid else None
    cheapest_model = min(valid, key=lambda x: x.cost).model if valid else None

    response = CompareResponse(
        run_id=local_run_id,
        prompt=prompt,
        results=normalized,
        best_model=best_model,
        fastest_model=fastest_model,
        cheapest_model=cheapest_model,
    )

    if persist:
        run_store.save_run(local_run_id, export_rows)

    return response, export_rows


async def run_batch_compare(
    prompts: list[str],
    models: list[str],
    use_judge: bool = False,
) -> tuple[str, list[CompareResponse], dict[str, Optional[Union[float, str]]]]:
    run_id = str(uuid4())
    tasks = [run_compare(prompt, models, use_judge=use_judge, run_id=run_id, persist=False) for prompt in prompts]
    batch_results = await asyncio.gather(*tasks)

    comparisons: list[CompareResponse] = [item[0] for item in batch_results]
    all_rows: list[ExportRow] = [row for _, rows in batch_results for row in rows]

    run_store.save_run(run_id, all_rows)

    valid_rows = [r for c in comparisons for r in c.results if r.error is None]
    avg_cost = round(sum(r.cost for r in valid_rows) / len(valid_rows), 8) if valid_rows else 0.0
    avg_latency = round(sum(r.time for r in valid_rows) / len(valid_rows), 4) if valid_rows else 0.0

    model_score_sum = defaultdict(float)
    model_count = defaultdict(int)
    for row in valid_rows:
        model_score_sum[row.model] += row.score
        model_count[row.model] += 1

    overall_best = None
    if model_score_sum:
        averages = {m: model_score_sum[m] / model_count[m] for m in model_score_sum}
        overall_best = max(averages, key=averages.get)

    summary: dict[str, Optional[Union[float, str]]] = {
        "average_cost": avg_cost,
        "average_latency": avg_latency,
        "overall_best_model": overall_best,
    }

    return run_id, comparisons, summary
