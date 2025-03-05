<template>
    <div class="row">
        <div class="col-6">
            <h4>Existing locations ({{ locationCount }})</h4>
        </div>
        <div class="col-6 text-end">
            <div class="btn-group me-2">
                <button type="button" class="btn btn-sm btn-outline-secondary" @click="fetchLocations">Refresh</button>
                <button type="button" class="btn btn-sm btn-success" data-bs-toggle="modal" data-bs-target="#staticBackdrop">Add new location</button>
            </div>
        </div>  
    </div>
    <div class="table-responsive">
        <table class="table table-striped table-sm">
            <thead>
                <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Total Rooms</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="location in locations['locations']" :key="location.id">
                    <td>{{ location.name }}</td>
                    <td>{{ location.num_rooms }}</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="modal fade" id="staticBackdrop" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="staticBackdropLabel">Create a new location</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="locationName" class="form-label">Location Name</label>
                        <input type="text" class="form-control" id="locationName" v-model="newLocation.name" placeholder="Krishna Hostel" maxlength="100">
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-success" @click="createLocation">Create</button>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'
import router from '@/router'
import { API_DOMAIN } from '@/config'

const locations = ref([])
const locationCount = ref(0)
const newLocation = ref({
    name: '',
})

async function fetchLocations() {
    try {
        const response = await fetch(`${API_DOMAIN}/api/location/list`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        })
        const data = await response.json()
        if (!response.ok) {
            if (response.status === 401) {
                router.push('/')
            }
            throw new Error(data.error || 'Failed to fetch locations')
        }
        locations.value = data
        locationCount.value = locations.value['locations'].length
    } catch (error) {
        console.error(error)
    }
}

async function createLocation() {
    try {
        const response = await fetch(`${API_DOMAIN}/api/location/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify(newLocation.value)
        })
        if (response.ok) {
            await fetchLocations()
            newLocation.value.name = ''
        } else {
            response.json().then(data => {
                alert(data['error'])
            })
        }
    } catch (error) {
        console.error(error)
    }
}

onMounted(async () => {
    await fetchLocations()
})

</script>
  
<style scoped>
</style>