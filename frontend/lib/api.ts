import { BatchResponse, CompareResponse, ModelCatalogResponse, ModelKey } from "@/lib/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function parseResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body || "Request failed");
  }
  return (await res.json()) as T;
}

export async function comparePrompt(payload: {
  prompt: string;
  models: ModelKey[];
  use_judge: boolean;
}): Promise<CompareResponse> {
  const res = await fetch(`${API_BASE}/compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseResponse<CompareResponse>(res);
}

export async function batchCompare(payload: {
  prompts: string[];
  models: ModelKey[];
  use_judge: boolean;
}): Promise<BatchResponse> {
  const res = await fetch(`${API_BASE}/batch-compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseResponse<BatchResponse>(res);
}

export function exportExcelUrl(runId?: string): string {
  if (!runId) return `${API_BASE}/export-excel`;
  return `${API_BASE}/export-excel?run_id=${encodeURIComponent(runId)}`;
}

export async function getModelCatalog(): Promise<ModelCatalogResponse> {
  const res = await fetch(`${API_BASE}/models`);
  return parseResponse<ModelCatalogResponse>(res);
}
