export interface AnalysisResult {
  filename: string
  rows: number
  columns: number
  column_names: string[]
  missing_values: Record<string, number>
  duplicates: number
}

export interface AnalysisHistoryItem {
  id: number
  filename: string
  rows: number
  columns: string[]
  created_at: string
}