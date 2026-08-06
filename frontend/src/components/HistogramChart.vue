<script setup lang="ts">
import { computed } from 'vue'
import VChart from 'vue-echarts'

import { BarChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { use } from 'echarts/core'

use([
  BarChart,
  GridComponent,
  TooltipComponent,
  CanvasRenderer,
])

const props = defineProps<{
  title: string
  labels: string[]
  counts: number[]
}>()

const chartOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow',
    },
  },
  grid: {
    left: 48,
    right: 24,
    top: 24,
    bottom: 72,
  },
  xAxis: {
    type: 'category',
    data: props.labels,
    axisLabel: {
      rotate: 35,
      interval: 0,
    },
  },
  yAxis: {
    type: 'value',
    minInterval: 1,
    name: 'Frecuencia',
  },
  series: [
    {
      type: 'bar',
      data: props.counts,
      barMaxWidth: 42,
    },
  ],
}))
</script>

<template>
  <article class="histogram-card">
    <h4>{{ title }}</h4>

    <VChart
      class="histogram-chart"
      :option="chartOption"
      autoresize
    />
  </article>
</template>