import { defineNuxtPlugin } from '#app'
import * as echarts from 'echarts'

export default defineNuxtPlugin(() => {
  return {
    provide: { echarts }
  }
})