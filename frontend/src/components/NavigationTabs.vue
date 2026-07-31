<script setup lang="ts">
defineProps<{
  activeView: 'analyze' | 'history'
}>()

const emit = defineEmits<{
  (event: 'change-view', view: 'analyze' | 'history'): void
}>()
</script>

<template>
  <nav>
    <button
      :disabled="activeView === 'analyze'"
      @click="emit('change-view', 'analyze')"
    >
      Analizar
    </button>

    <button
      :disabled="activeView === 'history'"
      @click="emit('change-view', 'history')"
    >
      Historial
    </button>
  </nav>
</template>