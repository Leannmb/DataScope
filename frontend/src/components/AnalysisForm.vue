<script setup lang="ts">
defineProps<{
  selectedFile: File | null
  isLoading: boolean
  errorMessage: string
}>()

const emit = defineEmits<{
  (event: 'file-change', value: Event): void
  (event: 'analyze'): void
}>()
</script>

<template>
  <section>
    <h2>Analizar CSV</h2>

    <p>Selecciona un archivo CSV para analizarlo.</p>

    <input
      type="file"
      accept=".csv"
      @change="emit('file-change', $event)"
    >

    <p v-if="selectedFile">
      Archivo seleccionado: {{ selectedFile.name }}
    </p>

    <button
      :disabled="!selectedFile || isLoading"
      @click="emit('analyze')"
    >
      {{ isLoading ? 'Analizando...' : 'Analizar' }}
    </button>

    <p v-if="errorMessage">
      Error: {{ errorMessage }}
    </p>

    <slot />
  </section>
</template>