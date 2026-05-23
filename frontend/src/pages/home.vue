<script setup>
import { ref } from 'vue'

import top_navbar from '../components/top_navbar.vue'
import bottom_navbar from '../components/bottom_navbar.vue';

import { useLanguage } from '../composables/useLanguage'
const { t, locale, switchLanguage } = useLanguage()
</script>

<template>
    <div class="home">
        <top_navbar />
        <div class="hero">
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
    width: 100%;
    height: 100vh;
    background-image: url('../assets/background.png');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}
</style>