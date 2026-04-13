"use client";

interface Props {
  prompt: string;
  setPrompt: (value: string) => void;
  batchPrompts: string;
  setBatchPrompts: (value: string) => void;
  batchMode: boolean;
  setBatchMode: (v: boolean) => void;
  useJudge: boolean;
  setUseJudge: (v: boolean) => void;
}

export function PromptPanel({
  prompt,
  setPrompt,
  batchPrompts,
  setBatchPrompts,
  batchMode,
  setBatchMode,
  useJudge,
  setUseJudge,
}: Props) {
  return (
    <section className="rounded-2xl border border-border bg-panel/80 p-5">
      <div className="mb-4 flex flex-wrap items-center gap-3">
        <button
          type="button"
          className={`rounded-full px-4 py-2 text-sm ${batchMode ? "bg-transparent border border-border" : "bg-red-500 text-black font-semibold"}`}
          onClick={() => setBatchMode(false)}
        >
          Single Prompt
        </button>
        <button
          type="button"
          className={`rounded-full px-4 py-2 text-sm ${batchMode ? "bg-red-500 text-black font-semibold" : "bg-transparent border border-border"}`}
          onClick={() => setBatchMode(true)}
        >
          Multi-Test Mode
        </button>
        <label className="ml-auto flex items-center gap-2 text-sm text-gray-300">
          <input
            type="checkbox"
            checked={useJudge}
            onChange={(e) => setUseJudge(e.target.checked)}
            className="h-4 w-4 accent-red-500"
          />
          Enable LLM-as-judge
        </label>
      </div>

      {!batchMode ? (
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows={5}
          placeholder="Ask a prompt to benchmark across models..."
          className="w-full rounded-xl border border-border bg-black/40 p-4 text-sm outline-none transition focus:border-red-500"
        />
      ) : (
        <textarea
          value={batchPrompts}
          onChange={(e) => setBatchPrompts(e.target.value)}
          rows={8}
          placeholder="Enter one prompt per line for batch testing..."
          className="w-full rounded-xl border border-border bg-black/40 p-4 text-sm outline-none transition focus:border-red-500"
        />
      )}
    </section>
  );
}
