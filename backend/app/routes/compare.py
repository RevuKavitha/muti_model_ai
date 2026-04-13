from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Optional

from app.schemas import (
    BatchCompareRequest,
    BatchCompareResponse,
    BatchSummary,
    CompareRequest,
    CompareResponse,
    ModelCatalogResponse,
    SUPPORTED_MODELS,
)
from app.core.model_catalog import grouped_catalog
from app.services.comparison import run_batch_compare, run_compare
from app.services.exporter import rows_to_excel
from app.services.storage import run_store

router = APIRouter(tags=["comparison"])


def _validate_models(models: list[str]) -> list[str]:
    normalized = [m.strip() for m in models]
    invalid = [m for m in normalized if m not in SUPPORTED_MODELS]
    if invalid:
        raise HTTPException(status_code=400, detail=f"Unsupported models: {', '.join(invalid)}")
    if len(set(normalized)) != len(normalized):
        raise HTTPException(status_code=400, detail="Duplicate model entries are not allowed.")
    if len(normalized) != 3:
        raise HTTPException(status_code=400, detail="Exactly 3 models must be selected.")
    return normalized


@router.get("/models", response_model=ModelCatalogResponse)
async def list_models() -> ModelCatalogResponse:
    return ModelCatalogResponse(models=grouped_catalog())


@router.post("/compare", response_model=CompareResponse)
async def compare(req: CompareRequest) -> CompareResponse:
    models = _validate_models(req.models)
    response, _ = await run_compare(req.prompt, models, use_judge=req.use_judge)
    return response


@router.post("/batch-compare", response_model=BatchCompareResponse)
async def batch_compare(req: BatchCompareRequest) -> BatchCompareResponse:
    models = _validate_models(req.models)
    cleaned_prompts = [p.strip() for p in req.prompts if p.strip()]
    if not cleaned_prompts:
        raise HTTPException(status_code=400, detail="At least one non-empty prompt is required.")

    run_id, comparisons, summary_data = await run_batch_compare(cleaned_prompts, models, use_judge=req.use_judge)

    return BatchCompareResponse(
        run_id=run_id,
        comparisons=comparisons,
        summary=BatchSummary(**summary_data),
    )


@router.get("/export-excel")
async def export_excel(run_id: Optional[str] = Query(default=None)) -> StreamingResponse:
    rows = run_store.get_rows(run_id)
    if not rows:
        raise HTTPException(status_code=404, detail="No benchmark results available for export.")

    content = rows_to_excel(rows)
    selected = run_id or rows[0].run_id
    filename = f"llm-benchmark-{selected}.xlsx"

    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
