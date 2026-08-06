<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

import { SESSION_EXPIRED_EVENT } from './services/session'
import AnalysisForm from './components/AnalysisForm.vue'
import AnalysisHistory from './components/AnalysisHistory.vue'
import AnalysisResults from './components/AnalysisResults.vue'
import LoginForm from './components/LoginForm.vue'
import NavigationTabs from './components/NavigationTabs.vue'
import RegisterForm from './components/RegisterForm.vue'


import {
  analyzeCsv,
  getAnalysisHistory,
} from './services/api'

import {
  login,
  register,
} from './services/auth'

import {
  isAuthenticated as hasStoredToken,
  removeToken,
  saveToken,
} from './services/token'

import type {
  AnalysisHistoryItem,
  AnalysisResult,
} from './types/analysis'

type ActiveView = 'analyze' | 'history'
type AppView = 'login' | 'register' | 'app'

const currentView = ref<AppView>(
  hasStoredToken() ? 'app' : 'login'
)

const activeView = ref<ActiveView>('analyze')

const authenticationError = ref('')
const isAuthenticationLoading = ref(false)

const selectedFile = ref<File | null>(null)
const analysis = ref<AnalysisResult | null>(null)
const errorMessage = ref('')
const isLoading = ref(false)

const analysisHistory = ref<AnalysisHistoryItem[]>([])
const isHistoryLoading = ref(false)
const historyErrorMessage = ref('')


function showLogin(): void {
  authenticationError.value = ''
  currentView.value = 'login'
}


function showRegister(): void {
  authenticationError.value = ''
  currentView.value = 'register'
}


async function handleLogin(
  email: string,
  password: string,
): Promise<void> {
  authenticationError.value = ''
  isAuthenticationLoading.value = true

  try {
    const response = await login(
      email,
      password,
    )

    saveToken(response.access_token)

    currentView.value = 'app'
    activeView.value = 'analyze'
  } catch (error) {
    authenticationError.value =
      error instanceof Error
        ? error.message
        : 'No se pudo iniciar sesión.'
  } finally {
    isAuthenticationLoading.value = false
  }
}


async function handleRegister(
  name: string,
  email: string,
  password: string,
): Promise<void> {
  authenticationError.value = ''
  isAuthenticationLoading.value = true

  try {
    await register(
      name,
      email,
      password,
    )

    const loginResponse = await login(
      email,
      password,
    )

    saveToken(loginResponse.access_token)

    currentView.value = 'app'
    activeView.value = 'analyze'
  } catch (error) {
    authenticationError.value =
      error instanceof Error
        ? error.message
        : 'No se pudo crear la cuenta.'
  } finally {
    isAuthenticationLoading.value = false
  }
}


function handleLogout(): void {
  removeToken()

  currentView.value = 'login'
  activeView.value = 'analyze'

  selectedFile.value = null
  analysis.value = null
  analysisHistory.value = []

  errorMessage.value = ''
  historyErrorMessage.value = ''
  authenticationError.value = ''
}

function handleSessionExpired(): void {
  console.log('Sesión expirada')

  removeToken()

  currentView.value = 'login'
  activeView.value = 'analyze'

  selectedFile.value = null
  analysis.value = null
  analysisHistory.value = []

  errorMessage.value = ''
  historyErrorMessage.value = ''

  authenticationError.value =
    'Tu sesión ha expirado. Inicia sesión de nuevo.'
}

async function changeView(
  view: ActiveView,
): Promise<void> {
  activeView.value = view

  if (view === 'history') {
    await loadAnalysisHistory()
  }
}


function handleFileChange(event: Event): void {
  const input = event.target as HTMLInputElement

  selectedFile.value = input.files?.[0] ?? null
  analysis.value = null
  errorMessage.value = ''
}


async function analyzeFile(): Promise<void> {
  if (!selectedFile.value) {
    return
  }

  isLoading.value = true
  analysis.value = null
  errorMessage.value = ''

  try {
    analysis.value = await analyzeCsv(
      selectedFile.value,
    )
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Ocurrió un error desconocido.'
  } finally {
    isLoading.value = false
  }
}


async function loadAnalysisHistory(): Promise<void> {
  isHistoryLoading.value = true
  historyErrorMessage.value = ''

  try {
    analysisHistory.value =
      await getAnalysisHistory()
  } catch (error) {
    historyErrorMessage.value =
      error instanceof Error
        ? error.message
        : 'Ocurrió un error desconocido.'
  } finally {
    isHistoryLoading.value = false
  }
}

onMounted(() => {
  window.addEventListener(
    SESSION_EXPIRED_EVENT,
    handleSessionExpired,
  )
})

onUnmounted(() => {
  window.removeEventListener(
    SESSION_EXPIRED_EVENT,
    handleSessionExpired,
  )
})
</script>

<template>
  <main>
    <h1>DataScope</h1>

    <LoginForm
      v-if="currentView === 'login'"
      :is-loading="isAuthenticationLoading"
      :error-message="authenticationError"
      @login="handleLogin"
      @show-register="showRegister"
    />

    <RegisterForm
      v-else-if="currentView === 'register'"
      :is-loading="isAuthenticationLoading"
      :error-message="authenticationError"
      @register="handleRegister"
      @show-login="showLogin"
    />

    <template v-else>
      <button
        type="button"
        @click="handleLogout"
      >
        Cerrar sesión
      </button>

      <NavigationTabs
        :active-view="activeView"
        @change-view="changeView"
      />

      <AnalysisForm
        v-if="activeView === 'analyze'"
        :selected-file="selectedFile"
        :is-loading="isLoading"
        :error-message="errorMessage"
        @file-change="handleFileChange"
        @analyze="analyzeFile"
      >
        <AnalysisResults
          v-if="analysis"
          :analysis="analysis"
        />
      </AnalysisForm>

      <AnalysisHistory
        v-else
        :items="analysisHistory"
        :is-loading="isHistoryLoading"
        :error-message="historyErrorMessage"
      />
    </template>
  </main>
</template>