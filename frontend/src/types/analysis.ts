export interface ColumnType {
  name: string
  type: string
}

export interface NumericStatistics {
  name: string
  count: number
  unique: number
  mean: number | null
  median: number | null
  std: number | null
  min: number | null
  q1: number | null
  q3: number | null
  max: number | null
}

export interface AnalysisResult {
  filename: string
  rows: number
  columns: number
  column_names: string[]
  column_types: ColumnType[]
  numeric_statistics: NumericStatistics[]
  numeric_histograms: NumericHistogram[]
  missing_values: Record<string, number>
  missing_percentage: number
  duplicates: number
  size_bytes: number
}

export interface AnalysisHistoryItem {
  id: number
  filename: string
  rows: number
  columns: string[]
  created_at: string
}

export interface NumericHistogram {
  name: string
  labels: string[]
  counts: number[]
}