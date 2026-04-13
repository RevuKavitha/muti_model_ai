from io import BytesIO

import pandas as pd

from app.services.storage import ExportRow


def rows_to_excel(rows: list[ExportRow]) -> bytes:
    df = pd.DataFrame(
        [
            {
                "Prompt": r.prompt,
                "Model Name": r.model_name,
                "Response": r.response,
                "Time Taken": r.time_taken,
                "Token Usage": r.token_usage,
                "Cost": r.cost,
                "Score": r.score,
            }
            for r in rows
        ]
    )

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Benchmark Results")
    output.seek(0)
    return output.read()
