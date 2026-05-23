import { useI18n } from 'vue-i18n'
import { onMounted } from 'vue'

/*
import { useLanguage } from '../composables/useLanguage'
const { t, locale , switchLanguage } = useLanguage()
*/
export function useLanguage() {
  const { t, locale } = useI18n()

  onMounted(() => {
    const saved = localStorage.getItem('lang')
    if (saved && (saved === 'zh' || saved === 'en')) {
      locale.value = saved
    }
  })

  const switchLanguage = (lang) => {
    locale.value = lang
    localStorage.setItem('lang', lang)
  }

  return { t, locale, switchLanguage }
}
