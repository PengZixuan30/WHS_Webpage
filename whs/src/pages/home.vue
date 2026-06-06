<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

import defaultBg from '../assets/background.png'

import top_navbar from '../components/top_navbar.vue'
import bottom_navbar from '../components/bottom_navbar.vue';

import { useLanguage } from '../composables/useLanguage'
const { t, tm, locale, switchLanguage } = useLanguage()

import { animate } from 'animejs';

import { fetchBackend } from '../main'

const bgImage = ref(defaultBg)
const firstStatus = ref(null)
const secondStatus = ref(null)
const heroRef = ref(null)
const newsList = ref([])

const historyRef = ref(null)
const historyIndex = ref(0)
const orbitAngle = ref(0)
const stageHeight = ref(window.innerHeight - 90)
const SCROLL_PER_EVENT = 400

const historyEvents = computed(() => tm('pages.home.whs_feature.whs_history.events'))
const totalEvents = computed(() => historyEvents.value.length)
const spacerHeight = computed(() => SCROLL_PER_EVENT * totalEvents.value)

const orbitRadius = computed(() => stageHeight.value / 2 + 100)
const arcCenterX = computed(() => stageHeight.value / 2 * 0.2)
const arcCenterY = computed(() => stageHeight.value / 2)

const cardStyles = computed(() => {
  const n = totalEvents.value
  if (n === 0) return []
  const spacing = 360 / n
  return Array.from({ length: n }, (_, i) => {
    const angle = i * spacing - orbitAngle.value
    const rad = angle * Math.PI / 180
    const x = arcCenterX.value + orbitRadius.value * Math.cos(rad)
    const y = arcCenterY.value + orbitRadius.value * Math.sin(rad)
    return {
      left: x + 'px',
      top: y + 'px',
      transform: 'translate(-50%, -50%)'
    }
  })
})

let scrollHandler = null
let resizeHandler = null

function onHistoryScroll() {
  if (!historyRef.value) return
  const rect = historyRef.value.getBoundingClientRect()
  const scrolled = -rect.top
  const maxScroll = spacerHeight.value
  const progress = Math.max(0, Math.min(1, scrolled / maxScroll))

  historyIndex.value = Math.min(Math.floor(progress * totalEvents.value), totalEvents.value - 1)
  const maxAngle = 360 - (360 / totalEvents.value)
  orbitAngle.value = progress * maxAngle
}

onMounted(async () => {
  const modules = import.meta.glob('../assets/wanghai_web/*.png', { eager: true })
  const wanghaiImages = Object.values(modules).map(m => m.default)
  const allImages = [defaultBg, ...wanghaiImages]
  bgImage.value = allImages[Math.floor(Math.random() * allImages.length)]

  firstStatus.value = await fetchStatus('/api/whs/status/first')
  secondStatus.value = await fetchStatus('/api/whs/status/second')

  animate(heroRef.value, { opacity: [0, 1], translateY: [20, 0] }, { duration: 1000, easing: 'easeOutQuad' })

  scrollHandler = () => requestAnimationFrame(onHistoryScroll)
  resizeHandler = () => { stageHeight.value = window.innerHeight - 90 }
  window.addEventListener('scroll', scrollHandler, { passive: true })
  window.addEventListener('resize', resizeHandler)

  newsList.value = await fetchBackend('/api/whs/news')
})

onUnmounted(() => {
  if (scrollHandler) {
    window.removeEventListener('scroll', scrollHandler)
  }
  if (resizeHandler) {
    window.removeEventListener('resize', resizeHandler)
  }
})

async function fetchStatus(url) {
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 5000)
    
    const res = await fetch(url, { signal: controller.signal })
    clearTimeout(timeout)
    return await res.json()
  } catch (e) {
    return { error: true }
  }
}

function navigateTo(url) {
    router.push(url)
}
</script>

<template>
    <div class="home">
        <top_navbar />

        <div class="hero" :style="{ backgroundImage: `url(${bgImage})` }">
            <div class="hero-overlay" ref="heroRef">
                <h1>{{ t('pages.home.title') }}</h1>
                <p>{{ t('pages.home.description') }}</p>
            </div>
        </div>

        <div class="whs-feature">
            <div class="whs-feature-head">
                <h1>{{ t('pages.home.title') }}</h1>
                <span>{{ t('pages.home.whs_feature.old_name') }}</span>
            </div>
            <div class="whs-tag">
                <div v-for="tag in tm('pages.home.whs_feature.whs_tag')">{{ tag }}</div>
            </div>
            <div class="whs-server-status">
                <div>
                    <span
                        class="status-ribbon"
                        :class="firstStatus && firstStatus.alive ? 'ribbon-online' : 'ribbon-offline'"
                    >{{ firstStatus && firstStatus.alive ? 'ONLINE' : 'OFFLINE' }}</span>
                    <h1>{{ t('pages.home.whs_feature.server_status.first_name') }}</h1>
                    <p v-if="firstStatus">
                        {{ t('pages.home.whs_feature.players') }} {{ firstStatus.online }} / {{ firstStatus.max }}
                    </p>
                    <p v-else>{{ t('pages.home.whs_feature.loading') }}</p>
                    <p v-if="firstStatus">
                        {{ t('pages.home.whs_feature.versions') }} {{ firstStatus.version }}
                    </p>
                    <p v-else>{{ t('pages.home.whs_feature.loading') }}</p>
                </div>
                <div>
                    <span
                        class="status-ribbon"
                        :class="secondStatus && secondStatus.alive ? 'ribbon-online' : 'ribbon-offline'"
                    >{{ secondStatus && secondStatus.alive ? 'ONLINE' : 'OFFLINE' }}</span>
                    <h1>{{ t('pages.home.whs_feature.server_status.second_name') }}</h1>
                    <p v-if="secondStatus">
                        {{ t('pages.home.whs_feature.players') }} {{ secondStatus.online }} / {{ secondStatus.max }}
                    </p>
                    <p v-else>{{ t('pages.home.whs_feature.loading') }}</p>
                    <p v-if="secondStatus">
                        {{ t('pages.home.whs_feature.versions') }} {{ secondStatus.version }}
                    </p>
                    <p v-else>{{ t('pages.home.whs_feature.loading') }}</p>
                </div>
            </div>
            <div class="whs-saved">
                <div class="whs-saved-version">
                    <span class="badge-current">{{ t('pages.home.whs_feature.whs_saved.current') }}</span>
                    <span><strong>Fabric 1.21.10</strong> · {{ t('pages.home.whs_feature.whs_saved.original') }}</span>
                </div>
                <div class="whs-saved-version">
                    <span class="badge-old">{{ t("pages.home.whs_feature.whs_saved.old") }}</span>
                    <span>Fabric 1.20.4 · {{ t("pages.home.whs_feature.whs_saved.saved") }}</span>
                </div>
            </div>
            <div class="whs-concept">
                <h1>{{ t('pages.home.whs_feature.whs_concept.core') }}</h1>
                <strong>{{ t('pages.home.whs_feature.whs_concept.core_concept') }}</strong>
                <p>{{ t('pages.home.whs_feature.whs_concept.summary_p') }}<strong>{{ t('pages.home.whs_feature.whs_concept.summary_strong') }}</strong></p>
                <div class="concept-mini-card">
                    <div>{{ t('pages.home.whs_feature.whs_concept.mini_card.no_metrics') }}</div>
                    <div>{{ t('pages.home.whs_feature.whs_concept.mini_card.no_mechanization') }}</div>
                    <div>{{ t('pages.home.whs_feature.whs_concept.mini_card.return_essence') }}</div>
                </div>
            </div>
            <div class="current-achivement">
                <div>
                    <h1>{{ t('pages.home.whs_feature.whs_achievements.current_title') }}</h1>
                    <ul>
                        <li v-for="item in tm('pages.home.whs_feature.whs_achievements.current_items')" v-html="item"></li>
                    </ul>
                </div>
                <div>
                    <h1>{{ t('pages.home.whs_feature.whs_achievements.future_title') }}</h1>
                    <ul>
                        <li v-for="item in tm('pages.home.whs_feature.whs_achievements.future_items')" v-html="item"></li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="whs-history" ref="historyRef" :style="{ height: `calc(100vh + ${spacerHeight}px)` }">
            <div class="history-sticky">
                <h1>
                    <span>{{ t('pages.home.whs_feature.whs_history.title') }}</span>
                    <button @click="navigateTo('/history')">{{ t('pages.home.whs_feature.whs_history.button') }}</button>
                </h1>
                <div class="history-stage">
                    <div class="semi-circle">
                        <div class="timeline-markers">
                            <div
                                v-for="(event, i) in historyEvents"
                                :key="i"
                                class="timeline-marker"
                                :class="{ active: historyIndex === i }"
                                :style="{ top: ((i + 0.5) / totalEvents * 100) + '%' }"
                            >
                                <span class="marker-dot"></span>
                                <span class="marker-label">
                                    <strong>{{ event.date }}</strong>
                                    <em>{{ event.title }}</em>
                                </span>
                            </div>
                        </div>
                    </div>
                    <div
                        v-for="(event, i) in historyEvents"
                        :key="i"
                        class="orbit-card"
                        :class="{ active: historyIndex === i }"
                        :style="cardStyles[i]"
                    >
                        <span class="orbit-card-badge">{{ i + 1 }} / {{ totalEvents }}</span>
                        <h3>{{ event.title }}</h3>
                        <p>{{ event.desc }}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="whs-managerment">
            <h1>{{ t('pages.home.whs_feature.whs_management.title') }}</h1>
            <div>
                <span><strong>{{ t('pages.home.whs_feature.whs_management.owner') }}</strong>: stevendjr</span>
                <button @click="navigateTo('/user/stevendjr')">GO TO</button>
            </div>
            <div>
                <span><strong>{{ t('pages.home.whs_feature.whs_management.hardware_provider') }}</strong>: yizexiaomu</span>
                <button @click="navigateTo('/user/yizexiaomu')">GO TO</button>
            </div>
            <div style="display: flex; flex-direction: column; align-items: flex-start; ">
                <strong>{{ t('pages.home.whs_feature.whs_management.admins') }}</strong>
                <ul>
                    <li><span>yello</span><button @click="navigateTo('/user/yello')">GO TO</button></li>
                    <li><span>Zele</span><button @click="navigateTo('/user/Zele')">GO TO</button></li>
                    <li><span>lyh1379</span><button @click="navigateTo('/user/lyh1379')">GO TO</button></li>
                    <li><span>Zihark</span><button @click="navigateTo('/user/Zihark')">GO TO</button></li>
                    <li><span>q__w__p</span><button @click="navigateTo('/user/q__w__p')">GO TO</button></li>
                    <li><span>PeaFlower_9331</span><button @click="navigateTo('/user/PeaFlower_9331')">GO TO</button></li>
                </ul>
            </div>
        </div>

        <div class="whs-joinus">
            <h1>{{ t('pages.home.whs_feature.whs_joinus.title') }}</h1>
            <div>
                <button @click="navigateTo('/about')">{{ t('pages.home.whs_feature.whs_joinus.understand') }}</button>
                <button @click="navigateTo('/join')">{{ t('pages.home.whs_feature.whs_joinus.join') }}</button>
            </div>
        </div>

        <div class="whs-news" v-if="newsList.length > 0">
            <h1>{{ t('pages.home.whs_feature.whs_news.title') }}</h1>
            <div
                v-for="news in newsList"
                    :key="news.id"
                    class="news-item"
                @click="navigateTo({ name: 'NewsDetail', params: { id: news.id } })"
            >
                <h3><strong>{{ news.title }}</strong><span>{{ news.date }}</span></h3>
                <p>{{ news.summary }}</p>
            </div>
        </div>
        
        <bottom_navbar />
    </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.hero{
    position: relative;
    width: 100%;
    height: 100vh;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}

.hero-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: rgba(0, 0, 0, 0.4);
    color: #ffffff;
    text-align: center;
    padding: 0 24px;
}

.hero-overlay h1 {
    font-size: 48px;
    font-weight: bold;
    margin: 0 0 16px 0;
}

.hero-overlay p {
    font-size: 20px;
    margin: 0;
    opacity: 0.85;
}

.whs-feature {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    color: var(--text-color);
}

.whs-feature-head {
    display: flex;
    align-items: center;
    width: 50%;
    justify-content: space-between;
}
.whs-feature-head h1 {
    font-size: 30px;
}
.whs-feature-head span {
    font-size: 16px;
    background-color: var(--links-color);
    color: var(--bg-color);
    padding: 4px 8px;
    border-radius: 8px;
}

.whs-tag {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    width: 50%;
    gap: 10px;
    padding-top: 40px;
    border-top: var(--links-color) solid 2px;
}
.whs-tag div {
    display: flex;
    background-color: var(--links-color);
    color: var(--bg-color);
    padding: 6px 12px;
    border-radius: 12px;

    box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.25), 0 4px 12px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.whs-tag div:hover {
    transform: translateY(-2px);
    box-shadow: 0 32px 48px -16px rgba(0, 0, 0, 0.3);
}

.whs-server-status {
    display: flex;
    justify-content: center;
    gap: 20px;
    width: 50%;
}
.whs-server-status > div {
    position: relative;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: stretch;
    gap: 20px;

    background-color: var(--card-color);
    color: var(--text-color);
    box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.25), 0 4px 12px rgba(0, 0, 0, 0.05);

    padding: 10px 24px;
    border-radius: 12px;
    overflow: hidden;

    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.status-ribbon {
    position: absolute;
    top: 12px;
    right: -42px;
    width: 140px;
    height: 24px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0;
    color: #fff;
    transform: rotate(45deg);
    box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    text-indent: 0;
}
.ribbon-online {
    background-color: rgba(46, 204, 113, 0.8);
}
.ribbon-offline {
    background-color: rgba(231, 76, 60, 0.8);
}
.whs-server-status div h1 {
    font-size: 24px;
    text-align: center;
}
.whs-server-status div p {
    font-size: 18px;
    margin: 0;
    text-align: center;
}
.whs-server-status div:hover {
    transform: translateY(-4px);
    box-shadow: 0 32px 48px -16px rgba(0, 0, 0, 0.3);
}

.whs-saved {
    display: flex;
    flex-direction: column;
    gap: 10px;

    width: 50%;

    padding: 10px 24px;
    border-radius: 12px;

    background-color: var(--card-color);
    color: var(--text-color);
    box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.25), 0 4px 12px rgba(0, 0, 0, 0.05);

    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.whs-saved-version {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
}
.badge-current {
    background-color: #2c5e3f;
    color: #f5f5f5;
    padding: 6px 12px;
    border-radius: 12px;
    font-weight: 600;
}
.badge-old {
    background-color: #cfdfd4;
    color: #1e3a2f;
    padding: 6px 12px;
    border-radius: 12px;
    font-weight: 600;
}
.whs-saved:hover {
    transform: translateY(-4px);
    box-shadow: 0 32px 48px -16px rgba(0, 0, 0, 0.3);
}

.whs-concept {
    display: flex;
    flex-direction: column;
    gap: 10px;

    width: 50%;

    padding: 10px 24px;
    border-radius: 12px;

    background-color: var(--card-color);
    color: var(--text-color);
    box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.25), 0 4px 12px rgba(0, 0, 0, 0.05);

    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.whs-concept h1{
    font-size: 30px;
}
.whs-concept strong {
    font-weight: 600;
}
.concept-mini-card {
    display: flex;
    gap: 10px;
}
.concept-mini-card div {
    background-color: var(--text-color);
    color: var(--bg-color);

    padding: 6px 12px;
    border-radius: 12px;
}
.whs-concept:hover {
    transform: translateY(-4px);
    box-shadow: 0 32px 48px -16px rgba(0, 0, 0, 0.3);
}

.current-achivement {
    display: flex;
    gap: 20px;

    width: 70%;

    justify-content: center;
    align-items: stretch;
}
.current-achivement div {
    display: flex;
    flex-direction: column;

    background-color: var(--card-color);
    color: var(--text-color);

    border-radius: 12px;
    padding: 12px 24px;

    box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.25), 0 4px 12px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.current-achivement div h1 {
    font-size: 18px;
    font-weight: 500;
    border-left: var(--text-color) solid 4px;
    padding-left: 10px;
}
.current-achivement div ul li :deep(strong) {
    font-weight: 700;
}
.current-achivement div ul li :deep(span) {
    background-color: var(--links-color);
    color: var(--bg-color);

    padding: 2px 4px;
    border-radius: 5px;
}
.current-achivement div ul {
    padding-left: 2em;
}
.current-achivement div:hover {
    transform: translateY(-4px);
    box-shadow: 0 32px 48px -16px rgba(0, 0, 0, 0.3);
}

.whs-history {
    position: relative;
    width: 100%;
    box-sizing: border-box;
    align-self: center;
}
.history-sticky {
    position: sticky;
    top: 0;
    height: 100vh;
    overflow: hidden;
    padding: 0 16px;
    box-sizing: border-box;
}
.history-sticky h1 {
    text-align: center;
    font-size: 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.history-sticky h1 button {
    padding: 10px 24px;
    font-size: 16px;
    border: 2px solid var(--text-color);
    border-radius: 8px;
    background: transparent;
    color: var(--text-color);
    cursor: pointer;
    transition: all 0.3s ease;
}
.history-sticky h1 button:hover {
    background: var(--btn-hover);
}

.history-stage {
    position: relative;
    height: calc(100vh - 90px);
    overflow: hidden;
}

.semi-circle {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    aspect-ratio: 1 / 2;
    border-radius: 0 100% 100% 0 / 0 50% 50% 0;
    background-color: var(--card-color);
    color: var(--text-color);
}

.timeline-markers {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
}
.timeline-marker {
    position: absolute;
    left: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    transform: translateY(-50%);
    transition: opacity 0.4s ease;
    opacity: 0.35;
}
.timeline-marker.active {
    opacity: 1;
}
.marker-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--links-color);
    flex-shrink: 0;
}
.marker-label {
    font-size: 12px;
    line-height: 1.3;
    color: var(--text-color);
    max-width: 180px;
}
.marker-label strong {
    display: block;
    font-size: 11px;
    color: var(--links-color);
}
.marker-label em {
    display: block;
    font-style: normal;
    opacity: 0.8;
}

.orbit-card {
    position: absolute;
    width: 200px;
    background-color: var(--card-color);
    color: var(--text-color);
    padding: 16px 20px;
    border-radius: 14px;
    box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.35), 0 4px 12px rgba(0, 0, 0, 0.1);
    z-index: 10;
    pointer-events: none;
    opacity: 0.3;
    transition: opacity 0.4s ease, transform 0.4s ease;
}
.orbit-card.active {
    opacity: 1;
    z-index: 20;
}
.orbit-card-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 700;
    background: var(--links-color);
    color: var(--bg-color);
    padding: 2px 10px;
    border-radius: 20px;
    margin-bottom: 10px;
}
.orbit-card h3 {
    margin: 0 0 10px 0;
    font-size: 20px;
}
.orbit-card p {
    margin: 0;
    font-size: 14px;
    opacity: 0.85;
    line-height: 1.6;
}

.whs-managerment {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    align-self: center;
    gap: 20px;
    align-items: stretch;
    padding: 20px 16px;
    width: 80%;
    transition: all 0.2s ease;
}
.whs-managerment h1 {
    font-size: 30px;
    align-self: center;
}
.whs-managerment div {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 16px;
    background-color: var(--card-color);
    color: var(--text-color);
    padding: 12px 24px;
    border-radius: 12px;
    box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.25), 0 4px 12px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
}
.whs-managerment div button {
    padding: 10px 24px;
    font-size: 16px;
    border: 2px solid var(--text-color);
    border-radius: 8px;
    background: transparent;
    color: var(--text-color);
    cursor: pointer;
    transition: all 0.3s ease;
}
.whs-managerment div button:hover {
    background-color: var(--btn-hover);
}
.whs-managerment div span strong {
    font-weight: 600;
}
.whs-managerment div ul {
    margin: 0;
    padding-left: 24px;
    align-self: stretch;
}
.whs-managerment div ul li {
    margin: 8px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.whs-managerment div:hover {
    transform: translateY(-4px);
    box-shadow: 0 32px 48px -16px rgba(0, 0, 0, 0.3);
}

.whs-joinus {
    margin: 40px 0;
    padding: 16px 0;
    width: 80%;
    background-color: var(--card-color);
    color: var(--text-color);
    align-self: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 20px;
    border-radius: 12px;
    box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.25), 0 4px 12px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
}
.whs-joinus h1 {
    font-size: 30px;
    font-weight: 600;
}
.whs-joinus div {
    display: flex;
    gap: 20px;
}
.whs-joinus div button {
    padding: 10px 24px;
    font-size: 16px;
    border: 2px solid var(--text-color);
    border-radius: 8px;
    background: transparent;
    color: var(--text-color);
    cursor: pointer;
    transition: all 0.3s ease;
}
.whs-joinus div button:hover {
    background-color: var(--btn-hover);
}
.whs-joinus:hover {
    transform: translateY(-4px);
    box-shadow: 0 32px 48px -16px rgba(0, 0, 0, 0.3);
}

.whs-news {
    width: 80%;
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    align-self: center;
    justify-content: center;
    align-items: stretch;
}
.whs-news h1 {
    flex: 1 1 100%;
    text-align: center;
    font-size: 30px;
}
.news-item {
    flex: 1 1 300px;
    min-width: 0;
    background-color: var(--card-color);
    color: var(--text-color);
    padding: 16px 20px;
    border-radius: 14px;
    box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.35), 0 4px 12px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
    overflow-wrap: break-word;
}
.news-item h3 {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    font-size: 24px;
}
.news-item h3 strong {
    font-weight: 600;
}
.news-item h3 span {
    font-size: 12px;
    color: var(--links-color);
}
.news-item p {
    font-size: 16px;
    opacity: 0.85;
}
.news-item:hover {
    transform: translateY(-4px);
    box-shadow: 0 32px 48px -16px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
    .whs-feature-head {
        width: 100%;
        justify-content: center;
        gap: 20px;
        padding: 0 16px;
        box-sizing: border-box;
    }
    .current-achivement,
    .whs-server-status {
        flex-direction: column;
        width: 100%;
        padding: 0 16px;
        box-sizing: border-box;
    }
    .whs-managerment,
    .whs-concept,
    .whs-saved {
        width: 80%;
    }

    .orbit-card {
        width: 160px;
        padding: 12px 14px;
    }
    .orbit-card h3 {
        font-size: 16px;
    }
    .marker-label {
        max-width: 120px;
        font-size: 11px;
    }
}
</style>