<template>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">College Status</h1>
    </div>
    <div class="table-responsive">
        <table class="table table-striped table-sm">
            <thead>
                <tr>
                    <th scope="col">Code</th>
                    <th scope="col">Name</th>
                    <th scope="col">Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="college in colleges['colleges']" :key="college.id">
                    <td>{{ college.code }}</td>
                    <td>{{ college.name }}</td>
                    <td>
                        <select v-model="college.status" @change="updateCollegeStatus(college)" :class="{'btn btn-sm': true, 'btn-danger': college.status === 'Checked out', 'btn-success': college.status === 'Checked in', 'btn-info': college.status === 'Yet to arrive'}">
                            <option value="Yet to arrive">Yet to arrive</option>
                            <option value="Checked in">Checked in</option>
                            <option value="Checked out">Checked out</option>
                        </select>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'

const colleges = ref([])

async function updateCollegeStatus(college) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/college/status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({
                college_id: college.id,
                status: college.status
            })
        })
        if (!response.ok) {
            const err = response.json()
            throw new Error(err['error'])
        }
    } catch (error) {
        console.error(error)
        alert(error)
    }
}

async function fetchColleges() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/college/list', {
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
        colleges.value = data
    } catch (error) {
        console.error(error)
        alert(error)
    }
}

onMounted(async () => {
    await fetchColleges()
})

</script>
  
<style scoped>
</style>