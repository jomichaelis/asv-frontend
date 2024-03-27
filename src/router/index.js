// Composables
import { createRouter, createWebHistory } from 'vue-router'
import { auth, getCurrentUser } from '@/plugins/firebase'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/Default.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta: { requiresAuth: true },
      },
    ],
  },
  {
    path: '/login',
    component: () => import('@/layouts/Blank.vue'),
    children: [
      {
        path: '',
        name: 'Anmelden',
        component: () => import('@/views/Auth/Login.vue'),
      },
    ],
  },
  {
    path: '/matchday',
    component: () => import('@/layouts/Default.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Matchday',
        component: () => import('@/views/Matchday.vue'),
      },
    ],
  },
  {
    path: '/verwaltung',
    component: () => import('@/layouts/Default.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Verwaltung',
        component: () => import('@/views/Verwaltung.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

router.beforeResolve(async (to) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)
  if (requiresAuth && !await getCurrentUser()) {
    return {
      path: '/login',
      query: { redirect: to.fullPath },
    }
  }
})

export default router
