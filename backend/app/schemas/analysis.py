from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AnalysisResponse(BaseModel):
    filename: str
    rows: int
    columns: int
    column_names: list[str]
    missing_values: dict[str, int]
    duplicates: int


class AnalysisHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    rows: int
    columns: list[str]
    created_at: datetime
    