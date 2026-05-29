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
