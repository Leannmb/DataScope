<script setup lang="ts">
interface AnalysisResult {
  filename: string
  rows: number
  columns: number
  column_names: string[]
  missing_values: Record<string, number>
  duplicates: number
}

defineProps<{
  analysis: AnalysisResult
}>()
</script>

<template>
  <section>
    <h2>Resultados del análisis</h2>

    <p>
      <strong>Archivo:</strong>
      {{ analysis.filename }}
    </p>

    <p>
      <strong>Filas:</strong>
      {{ analysis.rows }}
    </p>

    <p>
      <strong>Columnas:</strong>
      {{ analysis.columns }}
    </p>

    <p>
      <strong>Duplicados:</strong>
      {{ analysis.duplicates }}
    </p>

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
</template>