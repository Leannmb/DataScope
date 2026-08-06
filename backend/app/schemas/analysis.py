from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ColumnTypeResponse(BaseModel):
    name: str
    type: str


class NumericStatisticsResponse(BaseModel):
    name: str
    count: int
    unique: int
    mean: float | None
    median: float | None
    std: float | None
    min: float | None
    q1: float | None
    q3: float | None
    max: float | None


class NumericHistogramResponse(BaseModel):
    name: str
    labels: list[str]
    counts: list[int]


class AnalysisResponse(BaseModel):
    filename: str
    rows: int
    columns: int
    column_names: list[str]
    column_types: list[ColumnTypeResponse]
    numeric_statistics: list[NumericStatisticsResponse]
    numeric_histograms: list[NumericHistogramResponse]
    missing_values: dict[str, int]
    missing_percentage: float
    duplicates: int
    size_bytes: int


class AnalysisHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    rows: int
    columns: list[str]
    created_at: datetime