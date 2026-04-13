"use client";

import { exportExcelUrl } from "@/lib/api";

export function ExportButton({ runId }: { runId?: string }) {
  return (
    <a
      href={exportExcelUrl(runId)}
      className="inline-flex items-center rounded-lg border border-green-500/40 bg-green-500/10 px-4 py-2 text-sm font-semibold text-green-300 transition hover:bg-green-500/20"
    >
      Export to Excel
    </a>
  );
}
