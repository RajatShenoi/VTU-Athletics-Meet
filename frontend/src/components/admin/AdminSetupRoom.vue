<template>
    <div class="row">
        <div class="col-6">
            <h4>Existing rooms ({{ roomCount }})</h4>
        </div>
        <div class="col-6 text-end">
            <div class="btn-group me-2">
                <button type="button" class="btn btn-sm btn-outline-secondary" @click="fetchRooms">Refresh</button>
                <button type="button" class="btn btn-sm btn-success" data-bs-toggle="modal" data-bs-target="#staticBackdrop">Add new room</button>
            </div>
        </div>  
    </div>
    <div class="table-responsive">
        <table class="table table-striped table-sm">
            <thead>
                <tr>
                    <th scope="col">Location</th>
                    <th scope="col">Room Number</th>
                    <th scope="col">Max Occupancy</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="room in rooms['rooms']" :key="room.id">
                    <td>{{ room.location }}</td>
                    <td>{{ room.number }}</td>
                    <td>{{ room.max_occupancy }}</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="modal fade" id="staticBackdrop" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="staticBackdropLabel">Create a new room</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="locationName" class="form-label">Location Name</label>
                        <select class="form-control" id="locationName" v-model="newRoom.location_id">
                            <option v-for="location in locations['locations']" :key="location.id" :value="location.id">{{ location.name }}</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="roomNumber" class="form-label">Room Number</label>
                        <input type="text" class="form-control" id="roomNumber" v-model="newRoom.number" placeholder="46" maxlength="100">
                    </div>
                    <div class="mb-3">
                        <label for="roomCapacity" class="form-label">Max Occupancy</label>
                        <input type="number" class="form-control" id="roomCapacity" v-model="newRoom.max_occupancy" placeholder="2" min="0">
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-success" @click="createRoom">Create</button>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'

const rooms = ref([])
const roomCount = ref(0)
const locations = ref([])
const newRoom = ref({
    location_id: '',
    number: '',
    max_occupancy: 0,
})

async function fetchRooms() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/room/list')
        rooms.value = await response.json()
        roomCount.value = rooms.value['rooms'].length
    } catch (error) {
        console.error(error)
    }
}

async function fetchLocations() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/location/list')
        locations.value = await response.json()
    } catch (error) {
        console.error(error)
    }
}

async function createRoom() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/room/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newRoom.value)
        })
        if (response.ok) {
            await fetchRooms()
            newRoom.value.number = ''
            newRoom.value.max_occupancy = null
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
    fetchRooms()
    fetchLocations()
})

</script>
  
<style scoped>
</style>