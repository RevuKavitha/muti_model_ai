from pydantic import BaseModel, Field
from typing import Optional

from app.core.model_catalog import supported_model_keys

SUPPORTED_MODELS = supported_model_keys()


class CompareRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    models: list[str] = Field(..., min_length=3, max_length=3)
    use_judge: bool = False


class BatchCompareRequest(BaseModel):
    prompts: list[str] = Field(..., min_length=1)
    models: list[str] = Field(..., min_length=3, max_length=3)
    use_judge: bool = False


class ModelResult(BaseModel):
    model: str
    provider: str
    provider_model: str
    response: str
    time: float
    tokens: int
    input_tokens: int
    output_tokens: int
    cost: float
    score: float
    length_score: float
    keyword_score: float
    judge_score: Optional[float] = None
    error: Optional[str] = None


class CompareResponse(BaseModel):
    run_id: str
    prompt: str
    results: list[ModelResult]
    best_model: Optional[str]
    fastest_model: Optional[str]
    cheapest_model: Optional[str]


class BatchSummary(BaseModel):
    average_cost: float
    average_latency: float
    overall_best_model: Optional[str]


class BatchCompareResponse(BaseModel):
    run_id: str
    comparisons: list[CompareResponse]
    summary: BatchSummary


class ModelOption(BaseModel):
    key: str
    label: str
    provider: str
    family: str


class ModelCatalogResponse(BaseModel):
    models: dict[str, list[ModelOption]]
