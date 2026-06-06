<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'

import { useLanguage } from '../composables/useLanguage'
const { t, locale , switchLanguage } = useLanguage()

const menuOpen = ref(false)
const navbarRef = ref(null)
const noticeEl = ref(null)
const hasNotice = ref(false)
const noticeData = ref(null)

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

async function fetchNotice() {
  try {
    const response = await fetch('/api/whs/notice')
    if (!response.ok) {
      throw new Error('Network response was not ok')
    }
    noticeData.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch notice:', error)
    noticeData.value = null
  }
}

function updateNoticeDisplay() {
  if (!noticeEl.value) return
  const data = noticeData.value
  if (!data) {
    hasNotice.value = false
    noticeEl.value.style.display = 'none'
    return
  }
  const text = data[locale.value] || data.zh || data.en || null
  if (text) {
    hasNotice.value = true
    noticeEl.value.innerHTML = text
    noticeEl.value.style.display = 'block'
  } else {
    hasNotice.value = false
    noticeEl.value.style.display = 'none'
  }
}

onMounted(async () => {
  await fetchNotice()
  updateNoticeDisplay()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

watch(locale, () => {
  updateNoticeDisplay()
})
</script>

<template>
  <nav class="navbar" :class="{ 'notice-navbar': hasNotice }" ref="navbarRef">

    <div style="display: flex; align-items: center; justify-content: space-between; width: 100%; height: 100%;">

      <div class="logo">
        <a href="/">
          <img src="/icons.png" />
          <span>{{ t('nav.title') }}</span>
        </a>
      </div>

      <div class="links desktop-links">
        <a href="/news">{{ t('nav.news') }}</a>
        <a href="/join">{{ t('nav.join') }}</a>
        <a href="/about">{{ t('nav.about') }}</a>
      </div>

      <button
        class="menu-toggle"
        :class="{ open: menuOpen }"
        @click="toggleMenu"
        @mouseenter="menuOpen = true"
        aria-label="菜单"
      >
        <span v-if="!menuOpen" class="icon-hamburger">☰</span>
        <span v-else class="icon-arrow">▼</span>
      </button>

      <Transition name="slide">
        <div
          v-if="menuOpen"
          class="mobile-menu"
          @mouseleave="closeMenu"
        >
          <a href="/news" @click="closeMenu">{{ t('nav.news') }}</a>
          <a href="/join" @click="closeMenu">{{ t('nav.join') }}</a>
          <a href="/about" @click="closeMenu">{{ t('nav.about') }}</a>
        </div>
      </Transition>

    </div>

    <div class="notice" ref="noticeEl"></div>

  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 2%;
  left: 0;
  right: 0;
  margin: 0 auto;
  z-index: 1000;

  width: 80%;
  height: 70px;
  box-sizing: border-box;

  border: none;
  border-radius: 16px;

  display: flex;
  flex-direction: column;
  align-items: center;

  padding: 0 60px;

  background: var(--navbar-bg);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease, color 0.3s ease;
}
.notice-navbar {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}
.logo a {
  font-size: 28px;
  font-weight: bold;
  color: var(--text-color);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
}
.logo a img {
  width: 36px;
  height: 36px;
  object-fit: contain;
}
@media (max-width: 768px) {
  .logo a span {
    display: none;
  }
}

.links {
  display: flex;
  align-items: center;
  gap: 32px;
}

.links a {
  color: var(--links-color);
  text-decoration: none;
  font-size: 18px;
  transition: color 0.2s;
}

.links a:hover {
  color: var(--text-color);
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: var(--links-color);
  font-size: 22px;
  transition: all 0.3s;
}

.menu-toggle:hover,
.menu-toggle.open {
  color: var(--text-color);
}

.icon-hamburger {
  display: inline-block;
  transition: transform 0.3s;
}

.icon-arrow {
  display: inline-block;
  animation: flipIn 0.3s ease;
}

@keyframes flipIn {
  from {
    transform: rotateX(90deg);
    opacity: 0;
  }
  to {
    transform: rotateX(0deg);
    opacity: 1;
  }
}

.mobile-menu {
  display: none;
}

.slide-enter-active {
  transition: all 0.3s ease-out;
}
.slide-leave-active {
  transition: all 0.25s ease-in;
}
.slide-enter-from {
  opacity: 0;
  transform: translateY(-12px);
}
.slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

.notice {
  position: absolute;
  top: calc(100%);
  left: 0;
  right: 0;

  display: none;
  padding: 10px 20px;
  border-bottom-left-radius: 16px;
  border-bottom-right-radius: 16px;

  background: var(--notice-color);
  backdrop-filter: blur(10px);
  color: var(--text-color);
  font-size: 14px;
  line-height: 1.5;
  text-align: center;
  font-weight: 600;

  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.15);
  word-break: break-word;
  transition: all 0.3s ease, color 0.3s ease;
}
.notice :deep(a) {
  color: var(--links-color);
  text-decoration: none;
}
.notice :deep(a:hover) {
  color: var(--text-color);
  text-decoration: underline;
}

@media (max-width: 768px) {

  .navbar {
    width: 80%;
    left: 0;
    right: 0;
    padding: 0 24px;
    justify-content: space-between;
  }

  .desktop-links {
    display: none;
  }

  .menu-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .mobile-menu {
    display: flex;
    flex-direction: column;
    gap: 4px;

    position: absolute;
    top: 70px;
    right: 12px;
    z-index: 999;

    min-width: 160px;
    padding: 8px 0;

    background: rgba(var(--bg-color-rgb), 0.95);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 12px;

    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  }

  .mobile-menu a {
    display: block;
    padding: 10px 20px;

    color: var(--links-color);
    text-decoration: none;
    font-size: 16px;

    border-radius: 6px;
    transition: all 0.15s;
  }

  .mobile-menu a:hover {
    background: rgba(var(--text-color-rgb), 0.08);
    color: var(--text-color);
  }

  .mobile-menu button{
    padding: 10px 24px;
    font-size: 16px;
    border: 2px solid var(--bg-color);
    border-radius: 8px;
    background: transparent;
    color: var(--text-color);
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .mobile-menu button:hover {
    background: var(--text-color);
    color: var(--bg-color);
  }

  .notice {
    font-size: 13px;
    padding: 8px 16px;
  }

}
</style>