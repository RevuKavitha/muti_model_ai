"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { ResultItem } from "@/lib/types";

interface Props {
  results: ResultItem[];
}

export function ChartsPanel({ results }: Props) {
  const latencyData = results.map((r) => ({ model: r.model, latency: Number(r.time.toFixed(3)) }));
  const costData = results.map((r) => ({ model: r.model, cost: Number(r.cost.toFixed(6)) }));

  return (
    <section className="grid grid-cols-1 gap-4 lg:grid-cols-2">
      <div className="rounded-2xl border border-border bg-panel/80 p-4">
        <h3 className="mb-3 font-display text-lg">Latency Comparison</h3>
        <div className="h-60 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={latencyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2a3d" />
              <XAxis dataKey="model" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip />
              <Bar dataKey="latency" fill="#38bdf8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="rounded-2xl border border-border bg-panel/80 p-4">
        <h3 className="mb-3 font-display text-lg">Cost Comparison</h3>
        <div className="h-60 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={costData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2a3d" />
              <XAxis dataKey="model" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip />
              <Bar dataKey="cost" fill="#f59e0b" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </section>
  );
}
