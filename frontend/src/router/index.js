import { createRouter, createWebHistory } from 'vue-router'
import AdminHome from '@/views/AdminHome.vue'
import NotFound from '@/views/NotFound.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import AdminSetup from '@/views/AdminSetup.vue'
import AdminSetupCollege from '@/components/admin/AdminSetupCollege.vue'
import AdminSetupLocation from '@/components/admin/AdminSetupLocation.vue'
import AdminSetupRoom from '@/components/admin/AdminSetupRoom.vue'

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
          redirect: { name: 'admin-setup-college' },
          component: AdminSetup,
          children: [
            {
              path: 'college',
              name: 'admin-setup-college',
              component: AdminSetupCollege
            },
            {
              path: 'location',
              name: 'admin-setup-location',
              component: AdminSetupLocation
            },
            {
              path: 'room',
              name: 'admin-setup-room',
              component: AdminSetupRoom
            }
          ]
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
