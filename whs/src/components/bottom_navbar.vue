<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Sun, Moon, MoonIcon, SunIcon } from 'lucide-vue-next'

import { useLanguage } from '../composables/useLanguage'
const { t, locale , switchLanguage } = useLanguage()

const menuOpen = ref(false)
const navbarRef = ref(null)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
  menuOpen.value = false
}

function handleClickOutside(event) {
  if (navbarRef.value && !navbarRef.value.contains(event.target)) {
    closeMenu()
  }
}

const isDark = ref(false)

onMounted(() => {
  const saved = localStorage.getItem('theme')
  if (saved === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  } else if (saved === 'light') {
    isDark.value = false
    document.documentElement.classList.add('light')
  }
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

function toggleTheme() {
  isDark.value = !isDark.value
  const html = document.documentElement
  if (isDark.value) {
    html.classList.add('dark')
    html.classList.remove('light')
    localStorage.setItem('theme', 'dark')
  } else {
    html.classList.remove('dark')
    html.classList.add('light')
    localStorage.setItem('theme', 'light')
  }
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
    <footer class="navbar" ref="navbarRef">
        <div class="left">
            <a
                href="https://github.com/PengZixuan30/WHS_Webpage"
                target="_blank"
                rel="noopener noreferrer"
            >
                <span>MIT License, Copyright &copy; {{ new Date().getFullYear() }} yello</span>
            </a>
        </div>

        <div class="right">
            <div class="switch">
                <button @click="toggleTheme">
                    <span v-if="isDark"><Moon :size="20" /></span>
                    <span v-else><Sun :size="20" /></span>
                </button>
            </div>

            <div class="switch lang-switch">
                <button
                    :class="{ open: menuOpen }"
                    @click="toggleMenu"
                    @mouseenter="menuOpen = true"
                    aria-label="菜单"
                    >
                    <span>{{ locale === 'zh' ? '中文' : 'English' }}</span>
                </button>

                <Transition name="slide">
                    <div
                        v-if="menuOpen"
                        class="lang-menu"
                        @mouseleave="closeMenu"
                    >
                        <button
                            :class="{ active: locale === 'zh' }"
                            @click="switchLanguage('zh'); closeMenu()"
                        >
                            中文
                        </button>
                        <button
                            :class="{ active: locale === 'en' }"
                            @click="switchLanguage('en'); closeMenu()"
                        >
                            English
                        </button>
                    </div>
                </Transition>
            </div>

            <button @click="scrollToTop">
                <span>{{ t('bottom_navbar.backtop') }}</span>
            </button>
        </div>
    </footer>
</template>

<style scoped>
.navbar {
  position: relative;
  left: 0;
  right: 0;
  margin: 0 auto;

  border-top: 2px solid var(--text-color);

  width: 100%;
  height: 70px;
  box-sizing: border-box;

  display: flex;
  justify-content: space-between;
  align-items: center;

  padding: 0 60px;

  background: var(--navbar-bg);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease, color 0.3s ease;
}

.left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.left a{
    text-decoration: none;
    color: var(--links-color);
    transition: color 0.2s;

    font-size: 14px;
    font-weight: 500;
}

.left a:hover{
    color: var(--text-color);
}

.right {
    display: flex;
    align-items: stretch;
    gap: 20px;
}

.right button {
    padding: 10px 24px;
    font-size: 16px;
    border: 2px solid var(--text-color);
    border-radius: 8px;
    background: transparent;
    color: var(--text-color);
    cursor: pointer;
    transition: all 0.3s ease;
}
.right button:hover {
    background: var(--btn-hover);
}

.switch {
    display: flex;
    align-items: stretch;
}

.lang-switch {
    position: relative;
}

.switch button {
    padding: 10px 24px;
    font-size: 16px;
    border: 2px solid var(--text-color);
    border-radius: 8px;
    background: transparent;
    color: var(--text-color);
    cursor: pointer;
    transition: all 0.3s ease;
}

.switch button:hover {
    background: var(--text-color);
    color: var(--bg-color);
}

.lang-switch button:hover {
    background: var(--btn-hover);
    color: var(--text-color);
}

.lang-menu {
    display: flex;
    flex-direction: column;
    gap: 4px;

    position: absolute;
    bottom: 100%;
    margin-bottom: 16px;

    min-width: 140px;
    padding: 8px 0;

    background: rgba(var(--bg-color-rgb), 0.95);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 12px;

    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    z-index: 1001;
}

.slide-enter-active {
  transition: all 0.3s ease-out;
}
.slide-leave-active {
  transition: all 0.25s ease-in;
}
.slide-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.slide-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

.lang-menu button {
    display: block;
    width: 100%;
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: var(--links-color);
    font-size: 14px;
    text-align: left;
    cursor: pointer;
    transition: all 0.15s;
}

.lang-menu button:hover {
    background: rgba(var(--text-color-rgb), 0.08);
    color: var(--text-color);
}

.lang-menu button.active {
    color: var(--text-color);
    font-weight: 600;
}

@media (max-width: 768px) {
    .navbar {
        width: 100%;
        left: 0;
        right: 0;
        padding: 20px 24px;
        text-align: center;
        gap: 12px;

        flex-direction: column;
    }

    .lang-menu {
        margin-bottom: 8px;
    }
}
</style>