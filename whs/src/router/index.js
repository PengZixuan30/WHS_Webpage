import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { titleKey: 'pageTitle.home'}
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../pages/about.vue'),
    meta: { titleKey: 'pageTitle.about'}
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
