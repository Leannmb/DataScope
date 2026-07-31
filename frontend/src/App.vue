<script setup lang="ts">
import { ref } from 'vue'

import AnalysisForm from './components/AnalysisForm.vue'
import AnalysisHistory from './components/AnalysisHistory.vue'
import AnalysisResults from './components/AnalysisResults.vue'
import NavigationTabs from './components/NavigationTabs.vue'

import {
  analyzeCsv,
  getAnalysisHistory,
} from './services/api'

import type {
  AnalysisHistoryItem,
  AnalysisResult,
} from './types/analysis'

type ActiveView = 'analyze' | 'history'

const selectedFile = ref<File | null>(null)
const analysis = ref<AnalysisResult | null>(null)
const errorMessage = ref('')
const isLoading = ref(false)

const analysisHistory = ref<AnalysisHistoryItem[]>([])
const isHistoryLoading = ref(false)
const historyErrorMessage = ref('')

const activeView = ref<ActiveView>('analyze')

async function changeView(view: ActiveView): Promise<void> {
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
    analysis.value = await analyzeCsv(selectedFile.value)
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Ocurrió un error desconocido'
  } finally {
    isLoading.value = false
  }
}

async function loadAnalysisHistory(): Promise<void> {
  isHistoryLoading.value = true
  historyErrorMessage.value = ''

  try {
    analysisHistory.value = await getAnalysisHistory()
  } catch (error) {
    historyErrorMessage.value =
      error instanceof Error
        ? error.message
        : 'Ocurrió un error desconocido'
  } finally {
    isHistoryLoading.value = false
  }
}
</script>

<template>
  <main>
    <h1>DataScope</h1>

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
  </main>
</template>