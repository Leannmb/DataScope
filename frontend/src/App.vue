<script setup lang="ts">
import { h, ref } from 'vue';


interface AnalysisResult{
  filename: string
  rows: number
  columns: number
  column_names: string[]
  missing_values: Record<string, number>
  duplicates: number
}

const selectedFile = ref<File | null>(null);
const analysis = ref<AnalysisResult | null>(null)
const errorMessage = ref('')
const isLoading = ref(false)


function handleFileChange(event: Event) : void {
  const input = event.target as HTMLInputElement

  selectedFile.value = input.files?.[0] ?? null
  analysis.value = null
  errorMessage.value = ''
}

async function analyzeFile(): Promise<void> {
  if (!selectedFile.value){
    return
  }

  isLoading.value = true
  analysis.value = null
  errorMessage.value = ''

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try { 
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: formData
    })

    const responseData = await response.json() 

    if(!response.ok){
      throw new Error(responseData.detail ?? 'No se pudo analizar el archivo')
    }

    analysis.value = responseData as AnalysisResult
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Ocurrió un error desconocido'
  } finally {
    isLoading.value = false
  }
}

</script>

<template>
  <main>
    <h1>DataScope</h1>

    <p>Selecciona un archivo CSV para analizarlo.</p>

    <input
      type="file"
      accept=".csv"
      @change="handleFileChange"
    >

    <p v-if="selectedFile">  
      Archivo seleccionado: {{ selectedFile.name }}
    </p>

    <button :disabled="!selectedFile || isLoading" 
    @click="analyzeFile"
    >
      {{ isLoading ? 'Analizando...' : 'Analizar' }}
    
    </button>

    <p v-if="errorMessage">
      Error: {{ errorMessage }}
    </p>>

    <section v-if="analysis"> 
      <h2>Resultados del análisis</h2>

      <p><strong>Archivo:</strong> {{ analysis.filename }}</p>
      <p><strong>Filas:</strong> {{ analysis.rows }}</p>
      <p><strong>Columnas:</strong> {{ analysis.columns }}</p>
      <p><strong>Duplicados:</strong> {{ analysis.duplicates }}</p>
      
     <h3>Nombres de las columnas</h3>

     <ul>
        <li
          v-for="column in analysis.column_names"
          :key="column"
        >
          {{ column }}
        </li>
      </ul>

      <h3>Valores nulos</h3>

      <ul>
        <li
          v-for="(missingCount, column) in analysis.missing_values"
          :key="column"
        >
          {{ column }}: {{ missingCount }}
        </li>
      </ul>
    </section>
  </main>
</template>