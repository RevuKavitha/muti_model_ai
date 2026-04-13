from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes.compare import router as compare_router

app = FastAPI(
    title="Multi-Model AI Benchmarking API",
    version="1.0.0",
    description="Compare and evaluate LLM responses across providers.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(compare_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
