export type ModelKey = string;

export interface ModelOption {
  key: string;
  label: string;
  provider: "openai" | "claude" | "gemini";
  family: "GPT" | "Claude" | "Gemini" | string;
}

export interface ModelCatalogResponse {
  models: {
    openai: ModelOption[];
    claude: ModelOption[];
    gemini: ModelOption[];
  };
}

export interface ResultItem {
  model: ModelKey;
  provider: string;
  provider_model: string;
  response: string;
  time: number;
  tokens: number;
  input_tokens: number;
  output_tokens: number;
  cost: number;
  score: number;
  length_score: number;
  keyword_score: number;
  judge_score?: number | null;
  error?: string | null;
}

export interface CompareResponse {
  run_id: string;
  prompt: string;
  results: ResultItem[];
  best_model: ModelKey | null;
  fastest_model: ModelKey | null;
  cheapest_model: ModelKey | null;
}

export interface BatchResponse {
  run_id: string;
  comparisons: CompareResponse[];
  summary: {
    average_cost: number;
    average_latency: number;
    overall_best_model: ModelKey | null;
  };
}
