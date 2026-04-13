import asyncio
import json
import time
from dataclasses import dataclass
from typing import Optional

import httpx

from app.core.config import settings
from app.core.model_catalog import MODEL_CATALOG


@dataclass
class ProviderResult:
    model_key: str
    provider: str
    provider_model: str
    response: str
    latency: float
    input_tokens: int
    output_tokens: int
    error: Optional[str] = None

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


class ProviderService:
    @staticmethod
    async def query_openai(prompt: str, model_key: str) -> ProviderResult:
        if not settings.openai_api_key:
            return ProviderResult(model_key, "openai", model_key, "", 0.0, 0, 0, "Missing OPENAI_API_KEY")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {settings.openai_api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model_key,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }

        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                res.raise_for_status()
                data = res.json()

            text = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            input_tokens = int(usage.get("prompt_tokens", 0))
            output_tokens = int(usage.get("completion_tokens", 0))
            latency = round(time.perf_counter() - start, 4)
            return ProviderResult(model_key, "openai", model_key, text, latency, input_tokens, output_tokens)
        except Exception as exc:
            latency = round(time.perf_counter() - start, 4)
            return ProviderResult(model_key, "openai", model_key, "", latency, 0, 0, str(exc))

    @staticmethod
    async def query_claude(prompt: str, model_key: str) -> ProviderResult:
        if not settings.anthropic_api_key:
            return ProviderResult(model_key, "claude", model_key, "", 0.0, 0, 0, "Missing ANTHROPIC_API_KEY")

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": settings.anthropic_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": model_key,
            "max_tokens": 1024,
            "temperature": 0.2,
            "messages": [{"role": "user", "content": prompt}],
        }

        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                res.raise_for_status()
                data = res.json()

            chunks = data.get("content", [])
            text_parts = [c.get("text", "") for c in chunks if c.get("type") == "text"]
            text = "\n".join([p for p in text_parts if p])
            usage = data.get("usage", {})
            input_tokens = int(usage.get("input_tokens", 0))
            output_tokens = int(usage.get("output_tokens", 0))
            latency = round(time.perf_counter() - start, 4)
            return ProviderResult(model_key, "claude", model_key, text, latency, input_tokens, output_tokens)
        except Exception as exc:
            latency = round(time.perf_counter() - start, 4)
            return ProviderResult(model_key, "claude", model_key, "", latency, 0, 0, str(exc))

    @staticmethod
    async def query_gemini(prompt: str, model_key: str) -> ProviderResult:
        if not settings.gemini_api_key:
            return ProviderResult(model_key, "gemini", model_key, "", 0.0, 0, 0, "Missing GEMINI_API_KEY")

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model_key}:generateContent?key={settings.gemini_api_key}"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2},
        }

        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(url, json=payload)
                res.raise_for_status()
                data = res.json()

            candidates = data.get("candidates", [])
            text = ""
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                text = "\n".join(p.get("text", "") for p in parts if p.get("text"))

            usage = data.get("usageMetadata", {})
            input_tokens = int(usage.get("promptTokenCount", 0))
            output_tokens = int(usage.get("candidatesTokenCount", 0))
            latency = round(time.perf_counter() - start, 4)
            return ProviderResult(model_key, "gemini", model_key, text, latency, input_tokens, output_tokens)
        except Exception as exc:
            latency = round(time.perf_counter() - start, 4)
            return ProviderResult(model_key, "gemini", model_key, "", latency, 0, 0, str(exc))

    @staticmethod
    async def run_selected(models: list[str], prompt: str) -> list[ProviderResult]:
        tasks = []
        immediate_results = []
        for m in models:
            meta = MODEL_CATALOG.get(m)
            if not meta:
                immediate_results.append(ProviderResult(m, "unknown", m, "", 0.0, 0, 0, "Unsupported model"))
                continue

            provider = meta["provider"]
            if provider == "openai":
                tasks.append(ProviderService.query_openai(prompt, m))
            elif provider == "claude":
                tasks.append(ProviderService.query_claude(prompt, m))
            elif provider == "gemini":
                tasks.append(ProviderService.query_gemini(prompt, m))

        if not tasks:
            return immediate_results

        gathered = await asyncio.gather(*tasks)
        return [*immediate_results, *gathered]


async def judge_with_openai(prompt: str, responses: list[tuple[str, str]]) -> dict[str, float]:
    if not settings.openai_api_key:
        return {}

    rubric = (
        "You are an impartial evaluator. Score each model response from 0 to 100 based on "
        "correctness, relevance, clarity, and completeness. Return only JSON mapping model->score."
    )

    content_lines = [f"Prompt:\n{prompt}\n", "Responses:"]
    for model, text in responses:
        content_lines.append(f"MODEL={model}\n{text}\n")

    payload = {
        "model": settings.judge_model,
        "messages": [
            {"role": "system", "content": rubric},
            {"role": "user", "content": "\n".join(content_lines)},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0,
    }

    headers = {"Authorization": f"Bearer {settings.openai_api_key}", "Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            res = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            res.raise_for_status()
            data = res.json()

        raw = data["choices"][0]["message"]["content"]
        parsed = json.loads(raw)
        out: dict[str, float] = {}
        for k, v in parsed.items():
            try:
                out[str(k)] = float(v)
            except (TypeError, ValueError):
                continue
        return out
    except Exception:
        return {}
