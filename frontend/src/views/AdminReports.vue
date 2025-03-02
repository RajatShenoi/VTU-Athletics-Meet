<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">Reports</h1>
    <div class="btn-toolbar mb-2 mb-md-0">
        <ul class="nav nav-tabs">
            <li class="nav-item">
                <RouterLink :to="{name: 'admin-reports-college'}" class="nav-link" exact-active-class="active">Colleges</RouterLink>
            </li>
            <li class="nav-item">
                <RouterLink :to="{name: 'admin-reports-location'}" class="nav-link" exact-active-class="active">Locations</RouterLink>
            </li>
        </ul>
    </div>
    </div>
    <div>
        <RouterView />
    </div>
</template>
  
<script setup>
</script>
  
<style scoped>
body {
  font-size: .875rem;
}

.feather {
  width: 16px;
  height: 16px;
  vertical-align: text-bottom;
}

.nav-link.active {
  color: #2470dc;
}
</style>