from typing import Any

import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_float_dtype,
    is_integer_dtype,
    is_string_dtype,
)


def get_column_types(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Devuelve un tipo simplificado para cada columna."""

    column_types: list[dict[str, Any]] = []

    for column_name in df.columns:
        column = df[column_name]

        if is_bool_dtype(column):
            column_type = "boolean"

        elif is_integer_dtype(column):
            column_type = "integer"

        elif is_float_dtype(column):
            column_type = "float"

        elif is_datetime64_any_dtype(column):
            column_type = "datetime"

        elif is_string_dtype(column):
            column_type = "string"

        else:
            column_type = "unknown"

        column_types.append(
            {
                "name": str(column_name),
                "type": column_type,
            }
        )

    return column_types