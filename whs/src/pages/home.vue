<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

import defaultBg from '../assets/background.png'

import top_navbar from '../components/top_navbar.vue'
import bottom_navbar from '../components/bottom_navbar.vue';

import { useLanguage } from '../composables/useLanguage'
const { t, tm, locale, switchLanguage } = useLanguage()

const bgImage = ref(defaultBg)
const firstStatus = ref(null)
const secondStatus = ref(null)

onMounted(async () => {
  const modules = import.meta.glob('../assets/wanghai_web/*.png', { eager: true })
  const wanghaiImages = Object.values(modules).map(m => m.default)
  const allImages = [defaultBg, ...wanghaiImages]
  bgImage.value = allImages[Math.floor(Math.random() * allImages.length)]

  firstStatus.value = await fetchStatus('/api/status/first')
  secondStatus.value = await fetchStatus('/api/status/second')
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
            <div class="hero-overlay">
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

        <div class="whs-history">
            <h1>
                <span>{{ t('pages.home.whs_feature.whs_history.title') }}</span>
                <button @click="navigateTo('/history')">{{ t('pages.home.whs_feature.whs_history.button') }}</button>
            </h1>
            <div class="timeline">
                <div
                    class="timeline-event"
                    v-for="event in tm('pages.home.whs_feature.whs_history.events')"
                    :key="event.date"
                >
                    <div class="timeline-dot"></div>
                    <div class="timeline-date">{{ event.date }}</div>
                    <div class="timeline-card">
                        <h3>{{ event.title }}</h3>
                        <p>{{ event.desc }}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="whs-managerment"></div>
        
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
    width: 100%;
    max-width: 600px;
    box-sizing: border-box;
    padding: 0 16px;
    align-self: center;
}
.whs-history h1 {
    text-align: center;
    font-size: 30px;
    margin-bottom: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.whs-history h1 button {
    padding: 10px 24px;
    font-size: 16px;
    border: 2px solid var(--text-color);
    border-radius: 8px;
    background: transparent;
    color: var(--text-color);
    cursor: pointer;
    transition: all 0.3s ease;
}

.timeline {
    position: relative;
    padding-left: 32px;
}
.timeline::before {
    content: '';
    position: absolute;
    left: 15px;
    top: 0;
    bottom: 0;
    width: 3px;
    background: var(--links-color);
    border-radius: 2px;
}
.timeline-event {
    position: relative;
    margin-bottom: 28px;
}
.timeline-dot {
    position: absolute;
    left: -25px;
    top: 8px;
    width: 14px;
    height: 14px;
    background: var(--links-color);
    border: 3px solid var(--bg-color);
    border-radius: 50%;
    z-index: 1;
}
.timeline-date {
    font-size: 13px;
    font-weight: 700;
    color: var(--links-color);
    margin-bottom: 4px;
    letter-spacing: 1px;
}
.timeline-card {
    background-color: var(--card-color);
    color: var(--text-color);
    padding: 14px 20px;
    border-radius: 12px;
    box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.25), 0 4px 12px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.timeline-card h3 {
    margin: 0 0 6px 0;
    font-size: 18px;
}
.timeline-card p {
    margin: 0;
    font-size: 14px;
    opacity: 0.85;
    line-height: 1.6;
}
.timeline-card:hover {
    transform: translateY(-2px);
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
    .whs-concept,
    .whs-saved {
        width: 80%;
    }
}
</style>