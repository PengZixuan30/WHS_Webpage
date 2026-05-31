import { createApp, watch } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n'

const app = createApp(App)
app.use(router).use(i18n)
app.mount('#app')

const locale = i18n.global.locale
document.documentElement.lang = locale.value
watch(locale, (val) => {
  document.documentElement.lang = val
})

export async function fetchBackend(url, { timeout = 5000 } = {}) {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeout)

  try {
    const response = await fetch(url, { signal: controller.signal })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    if (error.name === 'AbortError') {
      console.error('Request timed out')
    } else {
      console.error('Fetch error, URL: ' + url + ', Error:', error)
    }
    return null
  }
  finally {
    clearTimeout(timer)
  }
}
