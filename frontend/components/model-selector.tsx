"use client";

import { ModelOption } from "@/lib/types";

interface Props {
  selected: string[];
  optionsByProvider: {
    openai: ModelOption[];
    claude: ModelOption[];
    gemini: ModelOption[];
  };
  onChange: (models: string[]) => void;
}

const providerTitles = {
  openai: "OpenAI GPT Family",
  claude: "Anthropic Claude Family",
  gemini: "Google Gemini Family",
};

export function ModelSelector({ selected, optionsByProvider, onChange }: Props) {
  const toggle = (key: string) => {
    if (selected.includes(key)) {
      onChange(selected.filter((m) => m !== key));
      return;
    }

    if (selected.length >= 3) {
      return;
    }

    onChange([...selected, key]);
  };

  return (
    <div className="space-y-5">
      <p className="text-sm text-gray-300">Select exactly 3 models for comparison ({selected.length}/3 selected).</p>

      {(["openai", "claude", "gemini"] as const).map((provider) => (
        <div key={provider}>
          <h3 className="mb-3 text-sm font-semibold uppercase tracking-[0.18em] text-gray-400">
            {providerTitles[provider]}
          </h3>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {optionsByProvider[provider].map((opt) => {
              const active = selected.includes(opt.key);
              const disabled = !active && selected.length >= 3;

              return (
                <button
                  key={opt.key}
                  type="button"
                  disabled={disabled}
                  onClick={() => toggle(opt.key)}
                  className={`rounded-xl border p-4 text-left transition ${
                    active
                      ? "border-red-500 bg-red-500/10 shadow-glow"
                      : "border-border bg-panel/70 hover:border-red-500/60"
                  } ${disabled ? "cursor-not-allowed opacity-50" : ""}`}
                >
                  <p className="font-display text-lg">{opt.label}</p>
                  <p className="mt-1 text-xs uppercase tracking-[0.2em] text-gray-400">{opt.key}</p>
                </button>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
