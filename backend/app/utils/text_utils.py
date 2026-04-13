import re
from collections import Counter

STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "of",
    "to",
    "is",
    "in",
    "for",
    "on",
    "with",
    "by",
    "at",
    "from",
    "that",
    "this",
    "it",
    "as",
    "be",
    "are",
    "was",
    "were",
    "can",
    "could",
    "should",
    "would",
    "you",
    "your",
    "i",
    "we",
    "they",
    "he",
    "she",
    "them",
    "their",
}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def extract_keywords(prompt: str, top_k: int = 8) -> list[str]:
    words = [w for w in tokenize(prompt) if w not in STOPWORDS and len(w) > 2]
    counts = Counter(words)
    return [w for w, _ in counts.most_common(top_k)]
