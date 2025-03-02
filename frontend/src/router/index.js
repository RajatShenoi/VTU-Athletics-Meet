import { createRouter, createWebHistory } from 'vue-router'
import AdminHome from '@/views/AdminHome.vue'
import NotFound from '@/views/NotFound.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import AdminSetup from '@/views/AdminSetup.vue'
import AdminSetupCollege from '@/components/admin/AdminSetupCollege.vue'
import AdminSetupLocation from '@/components/admin/AdminSetupLocation.vue'
import AdminSetupRoom from '@/components/admin/AdminSetupRoom.vue'
import AdminCheckin from '@/views/AdminCheckin.vue'
import AdminCheckout from '@/views/AdminCheckout.vue'
import AdminCheckinCollege from '@/components/admin/AdminCheckinCollege.vue'
import AdminCheckoutCollege from '@/components/admin/AdminCheckoutCollege.vue'
import AdminReports from '@/views/AdminReports.vue'
import AdminReportsCollege from '@/components/admin/AdminReportsCollege.vue'
import AdminReportsLocation from '@/components/admin/AdminReportsLocation.vue'

async function fetchColleges() {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/college/list')
    const data = await response.json()
    return data.colleges.map(college => college.code)
  } catch (error) {
    console.error(error)
    return []
  }
}

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
        },
        {
          path: 'checkin',
          name: 'admin-checkin',
          component: AdminCheckin,
          children: [
            {
              path: ':collegeCode',
              name: 'admin-checkin-college',
              component: AdminCheckinCollege,
              beforeEnter: async (to, from, next) => {
                const validCollegeCodes = await fetchColleges()
                if (validCollegeCodes.includes(to.params.collegeCode)) {
                  next()
                } else {
                  next({ name: 'not-found' })
                }
              }
            }
          ]
        },
        {
          path: 'checkout',
          name: 'admin-checkout',
          component: AdminCheckout,
          children: [
            {
              path: ':collegeCode',
              name: 'admin-checkout-college',
              component: AdminCheckoutCollege,
              beforeEnter: async (to, from, next) => {
                const validCollegeCodes = await fetchColleges()
                if (validCollegeCodes.includes(to.params.collegeCode)) {
                  next()
                } else {
                  next({ name: 'not-found' })
                }
              }
            }
          ]
        },
        {
          path: 'reports',
          name: 'admin-reports',
          component: AdminReports,
          redirect: { name: 'admin-reports-college' },
          children: [
            {
              path: 'college',
              name: 'admin-reports-college',
              component: AdminReportsCollege,
            },
            {
              path: 'location',
              name: 'admin-reports-location',
              component: AdminReportsLocation,
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
