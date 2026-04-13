"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

import { ChartsPanel } from "@/components/charts-panel";
import { ExportButton } from "@/components/export-button";
import { RedBleeBanner } from "@/components/red-blee-banner";
import { ResultsCards } from "@/components/results-cards";
import { BatchResponse, CompareResponse } from "@/lib/types";

function parseJson<T>(value: string | null): T | null {
  if (!value) return null;
  try {
    return JSON.parse(value) as T;
  } catch {
    return null;
  }
}

export default function ResultsPage() {
  const [single, setSingle] = useState<CompareResponse | null>(null);
  const [batch, setBatch] = useState<BatchResponse | null>(null);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setSingle(parseJson<CompareResponse>(localStorage.getItem("latestComparison")));
    setBatch(parseJson<BatchResponse>(localStorage.getItem("latestBatch")));
    setHydrated(true);
  }, []);

  const latestSingle = useMemo(() => {
    if (single) return single;
    if (batch?.comparisons?.length) return batch.comparisons[batch.comparisons.length - 1];
    return null;
  }, [single, batch]);

  if (!hydrated) {
    return <main className="mx-auto min-h-screen w-full max-w-4xl px-4 py-10">Loading dashboard...</main>;
  }

  if (!latestSingle) {
    return (
      <main className="mx-auto min-h-screen w-full max-w-4xl px-4 py-10">
        <h1 className="font-display text-3xl">No results available</h1>
        <p className="mt-3 text-gray-300">Run a comparison first to populate the dashboard.</p>
        <Link href="/" className="mt-6 inline-block rounded-lg border border-border px-4 py-2">
          Back to Home
        </Link>
      </main>
    );
  }

  return (
    <main className="mx-auto min-h-screen w-full max-w-7xl px-4 py-10">
      <RedBleeBanner subtitle="Results Protocol Active" />
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-red-400">Results Dashboard</p>
          <h1 className="font-display text-4xl">Benchmark Report</h1>
        </div>
        <div className="flex items-center gap-2">
          <ExportButton runId={batch?.run_id || single?.run_id} />
          <Link href="/" className="rounded-lg border border-border px-4 py-2 text-sm">
            New Run
          </Link>
        </div>
      </div>

      <section className="mb-6 rounded-2xl border border-border bg-panel/80 p-4">
        <p className="text-sm text-gray-300">Prompt</p>
        <p className="mt-2 text-gray-100">{latestSingle.prompt}</p>
        <div className="mt-4 flex flex-wrap gap-2 text-xs">
          <span className="rounded bg-green-500/15 px-2 py-1 text-green-300">Best: {latestSingle.best_model ?? "N/A"}</span>
          <span className="rounded bg-sky-500/15 px-2 py-1 text-sky-300">Fastest: {latestSingle.fastest_model ?? "N/A"}</span>
          <span className="rounded bg-amber-500/15 px-2 py-1 text-amber-300">Cheapest: {latestSingle.cheapest_model ?? "N/A"}</span>
        </div>
      </section>

      <ResultsCards
        results={latestSingle.results}
        bestModel={latestSingle.best_model}
        fastestModel={latestSingle.fastest_model}
        cheapestModel={latestSingle.cheapest_model}
      />

      <div className="mt-6">
        <ChartsPanel results={latestSingle.results} />
      </div>

      {batch && (
        <section className="mt-6 rounded-2xl border border-border bg-panel/80 p-5">
          <h2 className="font-display text-2xl">Batch Summary</h2>
          <div className="mt-3 grid grid-cols-1 gap-3 text-sm sm:grid-cols-3">
            <div className="rounded border border-border p-3">
              Avg Cost: <strong>${batch.summary.average_cost.toFixed(6)}</strong>
            </div>
            <div className="rounded border border-border p-3">
              Avg Latency: <strong>{batch.summary.average_latency.toFixed(3)}s</strong>
            </div>
            <div className="rounded border border-border p-3">
              Overall Best: <strong>{batch.summary.overall_best_model ?? "N/A"}</strong>
            </div>
          </div>
          <p className="mt-3 text-xs text-gray-400">Processed prompts: {batch.comparisons.length}</p>
        </section>
      )}
    </main>
  );
}
