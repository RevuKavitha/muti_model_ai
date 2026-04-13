"use client";

import { ResultItem } from "@/lib/types";

interface Props {
  results: ResultItem[];
  bestModel?: string | null;
  fastestModel?: string | null;
  cheapestModel?: string | null;
}

export function ResultsCards({ results, bestModel, fastestModel, cheapestModel }: Props) {
  return (
    <div className="card-grid">
      {results.map((r) => {
        const isBest = r.model === bestModel;
        const isFastest = r.model === fastestModel;
        const isCheapest = r.model === cheapestModel;

        return (
          <article
            key={r.model}
            className={`rounded-2xl border p-4 ${
              isBest ? "border-green-500 bg-green-500/10" : "border-border bg-panel/80"
            }`}
          >
            <div className="mb-3 flex items-start justify-between gap-2">
              <div>
                <h3 className="font-display text-xl capitalize">{r.model}</h3>
                <p className="text-xs uppercase tracking-[0.2em] text-gray-400">{r.provider_model}</p>
              </div>
              <div className="flex flex-col gap-1 text-xs">
                {isBest && <span className="rounded bg-green-500/20 px-2 py-1 text-green-300">Best</span>}
                {isFastest && <span className="rounded bg-sky-500/20 px-2 py-1 text-sky-300">Fastest</span>}
                {isCheapest && <span className="rounded bg-amber-500/20 px-2 py-1 text-amber-300">Cheapest</span>}
              </div>
            </div>

            <div className="mb-4 h-48 overflow-auto rounded-lg border border-border bg-black/50 p-3 text-sm leading-relaxed text-gray-200">
              {r.error ? <span className="text-red-400">Error: {r.error}</span> : r.response}
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs text-gray-300">
              <div className="rounded border border-border p-2">Latency: {r.time.toFixed(3)}s</div>
              <div className="rounded border border-border p-2">Tokens: {r.tokens}</div>
              <div className="rounded border border-border p-2">Cost: ${r.cost.toFixed(6)}</div>
              <div className="rounded border border-border p-2">Score: {r.score.toFixed(2)}</div>
            </div>
          </article>
        );
      })}
    </div>
  );
}
