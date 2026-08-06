from typing import Any

import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_numeric_dtype,
)


def get_numeric_statistics(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Devuelve estadísticas descriptivas de las columnas numéricas."""

    statistics: list[dict[str, Any]] = []

    for column_name in df.columns:
        column = df[column_name]

        if (
            not is_numeric_dtype(column)
            or is_bool_dtype(column)
        ):
            continue

        clean_column = column.dropna()

        if clean_column.empty:
            statistics.append(
                {
                    "name": str(column_name),
                    "count": 0,
                    "unique": 0,
                    "mean": None,
                    "median": None,
                    "std": None,
                    "min": None,
                    "q1": None,
                    "q3": None,
                    "max": None,
                }
            )

            continue

        standard_deviation = clean_column.std()

        statistics.append(
            {
                "name": str(column_name),
                "count": int(clean_column.count()),
                "unique": int(clean_column.nunique()),
                "mean": round(float(clean_column.mean()), 2),
                "median": round(float(clean_column.median()), 2),
                "std": (
                    round(float(standard_deviation), 2)
                    if pd.notna(standard_deviation)
                    else None
                ),
                "min": round(float(clean_column.min()), 2),
                "q1": round(
                    float(clean_column.quantile(0.25)),
                    2,
                ),
                "q3": round(
                    float(clean_column.quantile(0.75)),
                    2,
                ),
                "max": round(float(clean_column.max()), 2),
            }
        )

    return statistics