from pathlib import Path
from typing import Any

import pandas as pd

def analyze_csv(file_path: str) -> dict[str, Any]:
    """ Lee un CSV y devuelve un resumen básico."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"El archivo {file_path} no existe.")
    
    if path.suffix.lower() != '.csv':
        raise ValueError(f"El archivo {file_path} no es un CSV válido.")
    
    df = pd.read_csv(path)

    analysis = {
        "filename": path.name,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),
    }

    return analysis