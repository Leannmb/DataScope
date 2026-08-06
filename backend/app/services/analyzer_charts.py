from typing import Any

import numpy as np
import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_numeric_dtype,
)


def get_numeric_histograms(
    df: pd.DataFrame,
    bins: int = 10,
) -> list[dict[str, Any]]:
    """Genera histogramas para las columnas numéricas."""

    histograms: list[dict[str, Any]] = []

    for column_name in df.columns:
        column = df[column_name]

        if (
            not is_numeric_dtype(column)
            or is_bool_dtype(column)
        ):
            continue

        clean_column = column.dropna()

        if clean_column.empty:
            histograms.append(
                {
                    "name": str(column_name),
                    "labels": [],
                    "counts": [],
                }
            )

            continue

        counts, bin_edges = np.histogram(
            clean_column,
            bins=bins,
        )

        labels = [
            (
                f"{round(float(bin_edges[index]), 2)}"
                f" - "
                f"{round(float(bin_edges[index + 1]), 2)}"
            )
            for index in range(len(bin_edges) - 1)
        ]

        histograms.append(
            {
                "name": str(column_name),
                "labels": labels,
                "counts": counts.astype(int).tolist(),
            }
        )

    return histograms