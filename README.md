# Multi-Model AI Benchmarking Tool

Full-stack LLM comparison platform built with:
- Frontend: Next.js (App Router) + Tailwind + Recharts
- Backend: FastAPI + async HTTP clients
- Data export: pandas + openpyxl

## Folder Structure

```text
muti_model_ai/
├── backend/
│   ├── app/
│   │   ├── core/              # config + pricing
│   │   ├── routes/            # FastAPI endpoints
│   │   ├── services/          # providers, comparison, scoring, export, storage
│   │   ├── utils/             # text + keyword helpers
│   │   ├── main.py
│   │   └── schemas.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/                   # home + results dashboard
│   ├── components/            # selector, cards, charts, export button
│   ├── lib/                   # API client + shared types
│   ├── package.json
│   └── .env.example
└── README.md
```

## Backend Setup

```bash
cd /Users/kavitha/Desktop/muti_model_ai/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set API keys in `backend/.env`:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`

Run backend:

```bash
uvicorn app.main:app --reload --port 8000
```

## Frontend Setup

```bash
cd /Users/kavitha/Desktop/muti_model_ai/frontend
npm install
cp .env.example .env.local
npm run dev
```

Frontend runs on [http://localhost:3000](http://localhost:3000).

## API Endpoints

- `GET /models` (returns full GPT/Claude/Gemini model catalog for UI selection)
- `POST /compare`
- `POST /batch-compare`
- `GET /export-excel?run_id=<optional>`
- `GET /health`

### Example: /compare

```json
{
  "prompt": "Explain transformers in simple terms.",
  "models": ["gpt-4o-mini", "claude-3-5-haiku-latest", "gemini-1.5-flash-latest"],
  "use_judge": true
}
```

### Example: /batch-compare

```json
{
  "prompts": ["Prompt 1", "Prompt 2"],
  "models": ["gpt-4o-mini", "claude-3-5-haiku-latest", "gemini-1.5-flash-latest"],
  "use_judge": false
}
```

## Implemented Features

- Single prompt comparison
- Multi-model async execution
- Provider model catalog endpoint and UI model picker
- Exactly 3-model selection flow
- Side-by-side result cards (response, time, tokens, cost, score)
- Scoring pipeline:
  - Response length score
  - Keyword match score
  - Optional LLM-as-judge score (OpenAI judge)
- Best/Fastest/Cheapest model badges
- Batch prompt mode with summary metrics
- Latency + cost bar charts
- Excel export with required columns via pandas/openpyxl
- Error handling for missing keys/API failures

## Notes

- Pricing is estimated from static per-1M token table in `backend/app/core/pricing.py`.
- Update provider model names and prices in `.env` and pricing map as needed.
