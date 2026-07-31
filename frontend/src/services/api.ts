import type {
  AnalysisHistoryItem,
  AnalysisResult,
} from '../types/analysis'

const API_URL = 'http://127.0.0.1:8000'

export async function analyzeCsv(
  file: File,
): Promise<AnalysisResult> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_URL}/analyze`, {
    method: 'POST',
    body: formData,
  })

  const responseData = await response.json()

  if (!response.ok) {
    throw new Error(
      responseData.detail ?? 'No se pudo analizar el archivo'
    )
  }

  return responseData as AnalysisResult
}

export async function getAnalysisHistory(): Promise<
  AnalysisHistoryItem[]
> {
  const response = await fetch(`${API_URL}/analyses`)

  const responseData = await response.json()

  if (!response.ok) {
    throw new Error(
      responseData.detail ?? 'No se pudo cargar el historial'
    )
  }

  return responseData as AnalysisHistoryItem[]
}