<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()
const route = useRoute()

watch([() => route.meta.titleKey, locale], () => {
  const key = route.meta.titleKey || 'pageTitle.home'
  document.title = t(key)
}, { immediate: true })
</script>

<template>
  <router-view />
</template>
