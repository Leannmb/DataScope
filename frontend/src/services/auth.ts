const API_URL = 'http://127.0.0.1:8000'

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface RegisterResponse {
  id: number
  name: string
  email: string
  created_at: string
}

async function parseResponse(response: Response): Promise<unknown> {
  const contentType = response.headers.get('content-type')

  if (contentType?.includes('application/json')) {
    return response.json()
  }

  return null
}

export async function login(
  email: string,
  password: string,
): Promise<LoginResponse> {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email,
      password,
    }),
  })

  const responseData = await parseResponse(response)

  if (!response.ok) {
    const detail =
      typeof responseData === 'object' &&
      responseData !== null &&
      'detail' in responseData
        ? String(responseData.detail)
        : 'No se pudo iniciar sesión.'

    throw new Error(detail)
  }

  return responseData as LoginResponse
}

export async function register(
  name: string,
  email: string,
  password: string,
): Promise<RegisterResponse> {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name,
      email,
      password,
    }),
  })

  const responseData = await parseResponse(response)

  if (!response.ok) {
    const detail =
      typeof responseData === 'object' &&
      responseData !== null &&
      'detail' in responseData
        ? String(responseData.detail)
        : 'No se pudo crear la cuenta.'

    throw new Error(detail)
  }

  return responseData as RegisterResponse
}