<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()
const route = useRoute()

const titleSuffix = ref({ zh: '', en: '' })

onMounted(async () => {
  try {
    const res = await fetch('/api/whs')
    const data = await res.json()
    if (data.title_suffix) {
      titleSuffix.value = data.title_suffix
    }
  } catch {
    console.error('Failed to fetch title suffix')
  }
})

watch([() => route.meta.titleKey, locale, titleSuffix], () => {
  const key = route.meta.titleKey || 'pageTitle.home'
  const base = t(key)
  const suffix = titleSuffix.value[locale.value] || ''
  if (key === 'pageTitle.home' && suffix) {
    document.title = base + suffix
  } else {
    document.title = base
  }
}, { immediate: true })
</script>

<template>
  <router-view />
</template>
