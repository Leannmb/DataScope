<script setup lang="ts">
import type { AnalysisResult } from '../types/analysis'

defineProps<{
  analysis: AnalysisResult
}>()

function formatFileSize(bytes: number): string {
  if (bytes < 1024) {
    return `${bytes} B`
  }

  const kilobytes = bytes / 1024

  if (kilobytes < 1024) {
    return `${kilobytes.toFixed(2)} KB`
  }

  const megabytes = kilobytes / 1024

  return `${megabytes.toFixed(2)} MB`
}

function formatStatistic(value: number | null): string {
  if (value === null) {
    return 'No disponible'
  }

  return value.toLocaleString('es-ES', {
    maximumFractionDigits: 2,
  })
}
</script>

<template>
  <section class="analysis-results">
    <header class="results-header">
      <div>
        <p class="results-eyebrow">
          Dataset analizado
        </p>

        <h2>{{ analysis.filename }}</h2>
      </div>
    </header>

    <div class="summary-grid">
      <article class="summary-card">
        <span>Filas</span>
        <strong>{{ analysis.rows }}</strong>
      </article>

      <article class="summary-card">
        <span>Columnas</span>
        <strong>{{ analysis.columns }}</strong>
      </article>

      <article class="summary-card">
        <span>Duplicados</span>
        <strong>{{ analysis.duplicates }}</strong>
      </article>

      <article class="summary-card">
        <span>Valores nulos</span>
        <strong>{{ analysis.missing_percentage }} %</strong>
      </article>

      <article class="summary-card">
        <span>Tamaño</span>
        <strong>{{ formatFileSize(analysis.size_bytes) }}</strong>
      </article>
    </div>

    <section class="analysis-section">
      <h3>Columnas</h3>

      <div class="columns-grid">
        <article
          v-for="column in analysis.column_types"
          :key="column.name"
          class="column-card"
        >
          <header class="column-card-header">
            <h4>{{ column.name }}</h4>

            <span class="type-badge">
              {{ column.type }}
            </span>
          </header>

          <p>
            <span>Valores nulos</span>

            <strong>
              {{ analysis.missing_values[column.name] ?? 0 }}
            </strong>
          </p>
        </article>
      </div>
    </section>

    <section class="analysis-section">
      <h3>Estadísticas numéricas</h3>

      <p v-if="analysis.numeric_statistics.length === 0">
        No hay columnas numéricas.
      </p>

      <div
        v-else
        class="statistics-grid"
      >
        <article
          v-for="statistics in analysis.numeric_statistics"
          :key="statistics.name"
          class="statistics-card"
        >
          <h4>{{ statistics.name }}</h4>

          <dl>
            <div>
              <dt>Valores válidos</dt>
              <dd>{{ statistics.count }}</dd>
            </div>

            <div>
              <dt>Valores únicos</dt>
              <dd>{{ statistics.unique }}</dd>
            </div>

            <div>
              <dt>Media</dt>
              <dd>{{ formatStatistic(statistics.mean) }}</dd>
            </div>

            <div>
              <dt>Mediana</dt>
              <dd>{{ formatStatistic(statistics.median) }}</dd>
            </div>

            <div>
              <dt>Desviación típica</dt>
              <dd>{{ formatStatistic(statistics.std) }}</dd>
            </div>

            <div>
              <dt>Mínimo</dt>
              <dd>{{ formatStatistic(statistics.min) }}</dd>
            </div>

            <div>
              <dt>Q1</dt>
              <dd>{{ formatStatistic(statistics.q1) }}</dd>
            </div>

            <div>
              <dt>Q3</dt>
              <dd>{{ formatStatistic(statistics.q3) }}</dd>
            </div>

            <div>
              <dt>Máximo</dt>
              <dd>{{ formatStatistic(statistics.max) }}</dd>
            </div>
          </dl>
        </article>
      </div>
    </section>
  </section>
</template>