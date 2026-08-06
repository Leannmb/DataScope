from pathlib import Path
from typing import Any

import pandas as pd

from app.services.analyzer_statistics import get_numeric_statistics
from app.services.analyzer_types import get_column_types
from app.services.analyzer_charts import get_numeric_histograms

def analyze_csv(file_path: str) -> dict[str, Any]:
    """Lee un CSV y devuelve un resumen del conjunto de datos."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"El archivo {file_path} no existe."
        )

    if path.suffix.lower() != ".csv":
        raise ValueError(
            f"El archivo {file_path} no es un CSV válido."
        )

    df = pd.read_csv(path)

    # Información general
    rows = len(df)
    columns = len(df.columns)
    column_types = get_column_types(df)

    # Estadísticas numéricas
    numeric_statistics = get_numeric_statistics(df)

    numeric_histograms = get_numeric_histograms(df)

    # Calidad de los datos
    missing_values = df.isnull()

    missing_by_column = (
        missing_values.sum()
        .astype(int)
        .to_dict()
    )

    total_missing = int(
        missing_values.sum().sum()
    )

    total_cells = rows * columns

    if total_cells == 0:
        missing_percentage = 0.0
    else:
        missing_percentage = round(
            (total_missing / total_cells) * 100,
            2,
        )

    duplicates = int(
        df.duplicated().sum()
    )

    # Información del archivo
    size_bytes = path.stat().st_size

    # Respuesta final
    analysis = {
        "filename": path.name,
        "rows": rows,
        "columns": columns,
        "column_names": df.columns.tolist(),
        "column_types": column_types,
        "numeric_statistics": numeric_statistics,
        "numeric_histograms": numeric_histograms,
        "missing_values": missing_by_column,
        "missing_percentage": missing_percentage,
        "duplicates": duplicates,
        "size_bytes": size_bytes,
    }

    return analysis