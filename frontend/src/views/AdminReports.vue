<script setup>
import { RouterLink, RouterView } from 'vue-router'

const downloadPdfReport = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/college/report/pdf', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/pdf',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'college_report.pdf';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
};
</script>

<template>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">Reports</h1>
    <div class="btn-toolbar mb-2 mb-md-0">
      <button class="btn btn-warning" @click="downloadPdfReport">PDF Report</button>
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