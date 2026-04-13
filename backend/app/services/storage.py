from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class ExportRow:
    run_id: str
    prompt: str
    model_name: str
    response: str
    time_taken: float
    token_usage: int
    cost: float
    score: float


class RunStore:
    def __init__(self) -> None:
        self._rows_by_run: dict[str, list[ExportRow]] = {}
        self._latest_run_id: Optional[str] = None
        self._created_at: dict[str, datetime] = {}

    def save_run(self, run_id: str, rows: Iterable[ExportRow]) -> None:
        self._rows_by_run[run_id] = list(rows)
        self._latest_run_id = run_id
        self._created_at[run_id] = datetime.now(timezone.utc)

    def get_rows(self, run_id: Optional[str] = None) -> list[ExportRow]:
        selected_run = run_id or self._latest_run_id
        if not selected_run:
            return []
        return self._rows_by_run.get(selected_run, [])


run_store = RunStore()
