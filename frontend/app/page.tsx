"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { ModelSelector } from "@/components/model-selector";
import { PromptPanel } from "@/components/prompt-panel";
import { RedBleeBanner } from "@/components/red-blee-banner";
import { batchCompare, comparePrompt, getModelCatalog } from "@/lib/api";
import { ModelCatalogResponse, ModelKey } from "@/lib/types";

export default function HomePage() {
  const router = useRouter();

  const [prompt, setPrompt] = useState("");
  const [batchPrompts, setBatchPrompts] = useState("");
  const [models, setModels] = useState<ModelKey[]>([]);
  const [catalog, setCatalog] = useState<ModelCatalogResponse["models"] | null>(null);
  const [batchMode, setBatchMode] = useState(false);
  const [useJudge, setUseJudge] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadCatalog = async () => {
      try {
        const data = await getModelCatalog();
        setCatalog(data.models);

        const defaults = [
          data.models.openai[0]?.key,
          data.models.claude[0]?.key,
          data.models.gemini[0]?.key,
        ].filter(Boolean) as string[];
        setModels(defaults.slice(0, 3));
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load model catalog.");
      }
    };
    loadCatalog();
  }, []);

  const onRun = async () => {
    setError("");
    if (models.length !== 3) {
      setError("Select exactly 3 models.");
      return;
    }

    try {
      setLoading(true);
      if (!batchMode) {
        if (!prompt.trim()) {
          setError("Prompt is required.");
          return;
        }
        const data = await comparePrompt({ prompt: prompt.trim(), models, use_judge: useJudge });
        localStorage.setItem("latestComparison", JSON.stringify(data));
        localStorage.removeItem("latestBatch");
      } else {
        const prompts = batchPrompts
          .split("\n")
          .map((p) => p.trim())
          .filter(Boolean);

        if (prompts.length === 0) {
          setError("Enter at least one prompt in batch mode.");
          return;
        }

        const data = await batchCompare({ prompts, models, use_judge: useJudge });
        localStorage.setItem("latestBatch", JSON.stringify(data));
        localStorage.removeItem("latestComparison");
      }

      router.push("/results");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto min-h-screen w-full max-w-6xl px-4 py-10">
      <RedBleeBanner />

      <div className="space-y-5">
        <PromptPanel
          prompt={prompt}
          setPrompt={setPrompt}
          batchPrompts={batchPrompts}
          setBatchPrompts={setBatchPrompts}
          batchMode={batchMode}
          setBatchMode={setBatchMode}
          useJudge={useJudge}
          setUseJudge={setUseJudge}
        />

        <section className="rounded-2xl border border-border bg-panel/80 p-5">
          <h2 className="mb-4 font-display text-2xl">Model Selection</h2>
          {catalog ? (
            <ModelSelector selected={models} optionsByProvider={catalog} onChange={setModels} />
          ) : (
            <p className="text-sm text-gray-400">Loading models...</p>
          )}
        </section>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onRun}
            disabled={loading}
            className="rounded-xl bg-red-500 px-6 py-3 font-semibold text-black transition hover:bg-red-400 disabled:opacity-60"
          >
            {loading ? "Running benchmark..." : "Run Comparison"}
          </button>
          {error && <p className="text-sm text-red-400">{error}</p>}
        </div>
      </div>
    </main>
  );
}
