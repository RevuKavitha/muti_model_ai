from typing import Dict, List

# Curated cross-provider model catalog exposed to the frontend selector.
# Keys are sent directly in compare requests as model IDs.
MODEL_CATALOG: Dict[str, Dict[str, str]] = {
    # OpenAI GPT family
    "gpt-4o": {"provider": "openai", "family": "GPT", "label": "GPT-4o"},
    "gpt-4o-mini": {"provider": "openai", "family": "GPT", "label": "GPT-4o Mini"},
    "gpt-4.1": {"provider": "openai", "family": "GPT", "label": "GPT-4.1"},
    "gpt-4.1-mini": {"provider": "openai", "family": "GPT", "label": "GPT-4.1 Mini"},
    "gpt-4.1-nano": {"provider": "openai", "family": "GPT", "label": "GPT-4.1 Nano"},

    # Anthropic Claude family
    "claude-3-5-haiku-latest": {"provider": "claude", "family": "Claude", "label": "Claude 3.5 Haiku"},
    "claude-3-5-sonnet-latest": {"provider": "claude", "family": "Claude", "label": "Claude 3.5 Sonnet"},
    "claude-3-7-sonnet-latest": {"provider": "claude", "family": "Claude", "label": "Claude 3.7 Sonnet"},
    "claude-3-opus-latest": {"provider": "claude", "family": "Claude", "label": "Claude 3 Opus"},

    # Google Gemini family
    "gemini-1.5-flash-latest": {"provider": "gemini", "family": "Gemini", "label": "Gemini 1.5 Flash"},
    "gemini-1.5-pro-latest": {"provider": "gemini", "family": "Gemini", "label": "Gemini 1.5 Pro"},
    "gemini-2.0-flash": {"provider": "gemini", "family": "Gemini", "label": "Gemini 2.0 Flash"},
    "gemini-2.0-flash-lite": {"provider": "gemini", "family": "Gemini", "label": "Gemini 2.0 Flash-Lite"},
}


def supported_model_keys() -> set:
    return set(MODEL_CATALOG.keys())


def grouped_catalog() -> Dict[str, List[Dict[str, str]]]:
    grouped: Dict[str, List[Dict[str, str]]] = {"openai": [], "claude": [], "gemini": []}
    for key, meta in MODEL_CATALOG.items():
        grouped[meta["provider"]].append(
            {
                "key": key,
                "label": meta["label"],
                "provider": meta["provider"],
                "family": meta["family"],
            }
        )

    for provider in grouped:
        grouped[provider] = sorted(grouped[provider], key=lambda x: x["label"])

    return grouped
