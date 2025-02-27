import { createRouter, createWebHistory } from 'vue-router'
import AdminHome from '@/views/AdminHome.vue'
import NotFound from '@/views/NotFound.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import AdminSetup from '@/views/AdminSetup.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/admin',
      name: 'admin',
      redirect: { name: 'admin-dashboard' },
      component: AdminHome,
      children: [
        {
          path: 'dashboard',
          name: 'admin-dashboard',
          component: AdminDashboard
        },
        {
          path: 'setup',
          name: 'admin-setup',
          component: AdminSetup
        },
        {
          path: '',
          redirect: { name: 'admin-dashboard' }
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFound,
    }
  ],
})

export default router
