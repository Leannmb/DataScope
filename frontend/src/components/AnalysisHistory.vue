<script setup lang="ts">
interface AnalysisHistoryItem {
  id: number
  filename: string
  rows: number
  columns: string[]
  created_at: string
}

defineProps<{
  items: AnalysisHistoryItem[]
  isLoading: boolean
  errorMessage: string
}>()
</script>

<template>
  <section>
    <h2>Historial de análisis</h2>

    <p v-if="isLoading">
      Cargando historial...
    </p>

    <p v-else-if="errorMessage">
      Error: {{ errorMessage }}
    </p>

    <p v-else-if="items.length === 0">
      No hay análisis guardados.
    </p>

    <table v-else>
      <thead>
        <tr>
          <th>Archivo</th>
          <th>Filas</th>
          <th>Columnas</th>
          <th>Fecha</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="historyItem in items"
          :key="historyItem.id"
        >
          <td>{{ historyItem.filename }}</td>
          <td>{{ historyItem.rows }}</td>
          <td>{{ historyItem.columns.join(', ') }}</td>
          <td>
            {{
              new Date(historyItem.created_at).toLocaleString('es-ES', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
              })
            }}
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>