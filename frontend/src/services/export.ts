import type { AnalysisResult } from '../types/analysis'

import { getToken } from './token'

const API_URL = 'http://127.0.0.1:8000'

export function downloadJson(
  filename: string,
  data: unknown,
): void {
  const json = JSON.stringify(
    data,
    null,
    2,
  )

  const blob = new Blob(
    [json],
    {
      type: 'application/json',
    },
  )

  const url = URL.createObjectURL(blob)

  const link = document.createElement('a')

  link.href = url
  link.download = filename

  document.body.appendChild(link)
  link.click()
  link.remove()

  URL.revokeObjectURL(url)
}

export async function downloadPdf(
  analysis: AnalysisResult,
): Promise<void> {
  const token = getToken()

  const response = await fetch(
    `${API_URL}/export/pdf`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(analysis),
    },
  )

  if (!response.ok) {
    throw new Error(
      'No se pudo generar el PDF.'
    )
  }

  const blob = await response.blob()

  const url = URL.createObjectURL(blob)

  const link = document.createElement('a')

  link.href = url

  link.download = analysis.filename.replace(
    /\.csv$/i,
    '_report.pdf',
  )

  document.body.appendChild(link)

  link.click()

  link.remove()

  URL.revokeObjectURL(url)
}