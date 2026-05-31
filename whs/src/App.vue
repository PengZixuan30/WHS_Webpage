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
    // keep empty suffix on fetch failure
  }
})

watch([() => route.meta.titleKey, locale, titleSuffix], () => {
  const key = route.meta.titleKey || 'pageTitle.home'
  const base = t(key)
  const suffix = titleSuffix.value[locale.value] || ''
  document.title = base + suffix
}, { immediate: true })
</script>

<template>
  <router-view />
</template>
