import { createI18n } from 'vue-i18n'
import en from '../locales/en.json'
import zh from '../locales/zh.json'

const supportedLocales = ['zh', 'en']

function detectLanguage() {
  const browserLang = navigator.language || navigator.userLanguage || ''
  const shortLang = browserLang.split('-')[0]
  return supportedLocales.includes(shortLang) ? shortLang : 'en'
}

const i18n = createI18n({
  legacy: false,
  locale: detectLanguage(),
  fallbackLocale: 'en',
  messages: {
    en,
    zh
  }
})

export default i18n
