<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()

import top_navbar from '../components/top_navbar.vue'
import bottom_navbar from '../components/bottom_navbar.vue'
import { fetchBackend } from '../main'

import { useLanguage } from '../composables/useLanguage'
const { t, locale } = useLanguage()

import MarkdownIt from 'markdown-it'
const md = new MarkdownIt()

const news = ref(null)
const html = ref(null)
const error = ref(false)

onMounted(async () => {
    try {
        const res = await fetchBackend(`/api/whs/news/${route.params.id}`)
        news.value = res
        html.value = md.render(res.content)
    } catch (err) {
        error.value = true
    }
})
</script>

<template>
    <top_navbar />

    <div class="news-detail" v-if="news">
        <h1>
            <span>{{ news.title }}</span>
            <a href="#"># {{ news.id }}</a>
        </h1>
        <p v-html="html"></p>
    </div>
    <div class="news-detail" v-else-if="!error">
        <p>{{ t('pages.news_detail.loading') }}</p>
    </div>
    <div class="news-detail" v-if="error">
        <h1>
            <span>{{ t('pages.news_detail.error') }}</span>
            <a>404Error</a>
        </h1>
    </div>

    <bottom_navbar />
</template>

<style scoped>
.news-detail {
    max-width: 800px;
    margin: 0 auto;
    padding-top: calc(2% + 70px + 20px);
    color: var(--text-color)
}
.news-detail h1 {
    font-size: 50px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
}
.news-detail h1 a {
    font-size: 20px;
    color: var(--links-color);
    text-decoration: none;
    align-self: center;
}
.news-detail p {
    font-size: 20px;
    line-height: 1.6;
}
.news-detail p :deep(a) {
    color: var(--links-color);
    text-decoration: none;
}
.news-detail p :deep(a:hover) {
    color: var(--text-color);
    text-decoration: underline;
}
</style>
