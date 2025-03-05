<template>
    <div class="input-group mb-3">
        <span class="input-group-text">Code</span>
        <input type="text" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" v-model="searchValue">
        <button class="btn btn-success input-group-text" @click="fetchIndividualReport(searchValue)">Search</button>
    </div>
    <div v-for="college in report['report']" :key="college.id">
        <h5><span class="text-success">{{college.college_code}}</span> - {{ college.college_name }}</h5>
        <div v-if="college['rooms'].length > 0" class="table-responsive">
            <table class="table table-striped table-sm">
                <thead>
                    <tr>
                        <th scope="col">Location</th>
                        <th scope="col">Room Number</th>
                        <th scope="col">{{ college.college_code }} Count</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="room in college['rooms']" :key="room.id">
                        <td>{{ room.location }}</td>
                        <td>{{ room.number }}</td>
                        <td>{{ room.occupied_by_college_count }}</td>
                    </tr>
                    <tr>
                        <th></th>
                        <th>Total</th>
                        <th>{{college.college_count}}</th>
                    </tr>
                </tbody>
            </table>
        </div>
        <hr v-if="college['rooms'].length == 0">
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'
import router from '@/router'
import { API_DOMAIN } from '@/config'

const report = ref([])
const searchValue = ref('')

async function fetchIndividualReport(code) {
    try {
        const response = await fetch(`${API_DOMAIN}/api/college/report?code=${code}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        })
        const data = await response.json()
        if (!response.ok) {
            if (response.status === 401) {
                router.push('/')
            }
            throw new Error(data.error || 'Failed to individual report')
        }
        report.value = data
    } catch (error) {
        console.error(error)
    }
}

async function fetchReport() {
    try {
        const response = await fetch(`${API_DOMAIN}/api/college/report`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        })
        const data = await response.json()
        if (!response.ok) {
            if (response.status === 401) {
                router.push('/')
            }
            throw new Error(data.error || 'Failed to individual report')
        }
        report.value = data
    } catch (error) {
        console.error(error)
    }
}

onMounted(async () => {
    await fetchReport()
})

</script>
  
<style scoped>
</style>