<template>
    <hr>
    <h5>You are checking in participants from <span class="text-danger">{{ collegeName }}</span>. <span class="text-success">({{ collegeNumOccupants }} already checked in)</span></h5>
    <div class="accordion accordion-flush border">
        <div class="accordion-item">
            <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
                Currently occupied data (click here)
            </button>
            </h2>
            <div id="flush-collapseOne" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
            <div class="accordion-body">
                <div v-for="college in report['report']" :key="college.id">
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
            </div>
            </div>
        </div>
    </div>
    <hr>
    <h4>Available Rooms:</h4>
    <div class="table-responsive">
        <table class="table table-striped table-sm">
            <thead>
                <tr>
                    <th scope="col">Location</th>
                    <th scope="col">Room Number</th>
                    <th scope="col">{{collegeCode}} Count</th>
                    <th scope="col">Occupant Count</th>
                    <th scope="col">Max Occupancy</th>
                    <th scope="col">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="room in rooms['available_rooms']" :key="room.id">
                    <td>{{ room.location }}</td>
                    <td>{{ room.number }}</td>
                    <td>{{ room.same_college_students }}</td>
                    <td>{{ room.num_students }}</td>
                    <td>{{ room.max_occupancy }}</td>
                    <td>
                        <div class="btn-group btn-group-sm" role="group" aria-label="Basic mixed styles example">
                            <button type="button" :class="['btn', room.same_college_students > 0 ? 'btn-success' : 'btn-warning']" @click="checkin(room.id)">Add</button>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
  
<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const collegeCode = ref(route.params.collegeCode)
const collegeID = ref(0)
const collegeName = ref('')
const collegeNumOccupants = ref(0)
const rooms = ref([])

const report = ref([])

async function fetchIndividualReport() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/college/report?code=${collegeCode.value}`)
        report.value = await response.json()
    } catch (error) {
        console.error(error)
    }
}

async function checkin(room_id) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/student/checkin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ room_id, college_id: collegeID.value })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        await updateIndo();
    } catch (error) {
        console.error('Error checking in:', error);
        alert('Error checking in:', error);
    }
}

async function updateIndo() {
    collegeCode.value = route.params.collegeCode
    fetchIndividualReport();
    try {
        const res = await fetch(`http://127.0.0.1:5000/api/college/fromcode?code=${collegeCode.value}`);
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json();
        collegeName.value = data['college'].name;
        collegeID.value = data['college'].id;
        collegeNumOccupants.value = data['college'].num_occupants;
    } catch (error) {
        console.error('Error fetching college name:', error);
        alert('Error fetching college name:', error);
    }

    try {
        const res = await fetch(`http://127.0.0.1:5000/api/room/available?college_id=${collegeID.value}`)
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        rooms.value = await res.json();
    } catch (error) {
        console.error('Error fetching available rooms:', error);
        alert('Error fetching available rooms:', error);
    }
}

onMounted(async () => {
    updateIndo();
})

watch(() => route.params.collegeCode, async (newValue) => {
    collegeCode.value = newValue;
    await updateIndo();
})

</script>
  
<style scoped>
</style>