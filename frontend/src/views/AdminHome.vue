<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted } from 'vue'
import feather from 'feather-icons'
import router from '@/router'

const logout = () => {
    localStorage.removeItem('access_token')
    router.push({ name: 'home' })
}

onMounted(() => {
    feather.replace()
})
</script>

<template>
  <div class="container-fluid">
    <div class="row">
        <nav id="sidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
        <div class="position-sticky pt-3">
            <ul class="nav flex-column">
            <li class="nav-item">
                <RouterLink :to="{name: 'admin-setup'}" active-class="active" class="nav-link">
                <span data-feather="tool"></span>
                Setting Up
                </RouterLink>
            </li>
            <li class="nav-item">
                <RouterLink :to="{name: 'admin-college-status'}" active-class="active" class="nav-link">
                <span data-feather="check-circle"></span>
                College Status
                </RouterLink>
            </li>
            <li class="nav-item">
                <RouterLink :to="{name: 'admin-checkin'}" active-class="active" class="nav-link">
                <span data-feather="user-plus"></span>
                Check in
                </RouterLink>
            </li>
            <li class="nav-item">
                <RouterLink :to="{name: 'admin-checkout'}" active-class="active" class="nav-link">
                <span data-feather="user-minus"></span>
                Check out
                </RouterLink>
            </li>
            <li class="nav-item">
                <RouterLink :to="{name: 'admin-reports'}" active-class="active" class="nav-link">
                <span data-feather="file-text"></span>
                Reports
                </RouterLink>
            </li>
            <li class="nav-item">
                <button @click="logout" class="nav-link">
                <span data-feather="log-out"></span>
                Sign out
                </button>
            </li>
            </ul>
        </div>
        </nav>

        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <RouterView />
        </main>
    </div>
    </div>
</template>

<style scoped>
body {
  font-size: .875rem;
}

.feather {
  width: 16px;
  height: 16px;
  vertical-align: text-bottom;
}

/*
 * Sidebar
 */

.sidebar {
  position: fixed;
  top: 0;
  /* rtl:raw:
  right: 0;
  */
  bottom: 0;
  /* rtl:remove */
  left: 0;
  z-index: 100; /* Behind the navbar */
  padding: 48px 0 0; /* Height of navbar */
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
}

@media (max-width: 767.98px) {
  .sidebar {
    top: 5rem;
  }
}

.sidebar-sticky {
  position: relative;
  top: 0;
  height: calc(100vh - 48px);
  padding-top: .5rem;
  overflow-x: hidden;
  overflow-y: auto; /* Scrollable contents if viewport is shorter than content. */
}

.sidebar .nav-link {
  font-weight: 500;
  color: #333;
}

.sidebar .nav-link .feather {
  margin-right: 4px;
  color: #727272;
}

.sidebar .nav-link.active {
  color: #2470dc;
}

.sidebar .nav-link:hover .feather,
.sidebar .nav-link.active .feather {
  color: inherit;
}

.sidebar-heading {
  font-size: .75rem;
  text-transform: uppercase;
}
</style>