import type {
  AnalysisHistoryItem,
  AnalysisResult,
} from '../types/analysis'

import { getToken } from './token'

const API_URL = 'http://127.0.0.1:8000'


async function apiFetch(
  endpoint: string,
  options: RequestInit = {},
): Promise<Response> {
  const token = getToken()
  const headers = new Headers(options.headers)

  if (token !== null) {
    headers.set(
      'Authorization',
      `Bearer ${token}`,
    )
  }

  return fetch(
    `${API_URL}${endpoint}`,
    {
      ...options,
      headers,
    },
  )
}


export async function analyzeCsv(
  file: File,
): Promise<AnalysisResult> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiFetch(
    '/analyze',
    {
      method: 'POST',
      body: formData,
    },
  )

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
  const response = await apiFetch('/analyses')
  const responseData = await response.json()

  if (!response.ok) {
    throw new Error(
      responseData.detail ?? 'No se pudo cargar el historial'
    )
  }

  return responseData as AnalysisHistoryItem[]
}