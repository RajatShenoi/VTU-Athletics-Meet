<template>
    <hr>
    <h5>You are checking out participants from <span class="text-danger">{{ collegeName }}</span>. <span class="text-success">({{ collegeNumOccupants }} currently checked in)</span></h5>
    <hr>
    <h4>Rooms occupied by {{ collegeCode }}:</h4>
    <div class="table-responsive">
        <table class="table table-striped table-sm">
            <thead>
                <tr>
                    <th scope="col">Location</th>
                    <th scope="col">Room Number</th>
                    <th scope="col">{{ collegeCode }} Count</th>
                    <th scope="col">Occupant Count</th>
                    <th scope="col">Max Occupancy</th>
                    <th scope="col">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="room in rooms['rooms']" :key="room.id">
                    <td>{{ room.location }}</td>
                    <td>{{ room.number }}</td>
                    <td>{{ room.same_college_students }}</td>
                    <td>{{ room.num_students }}</td>
                    <td>{{ room.max_occupancy }}</td>
                    <td>
                        <div class="btn-group btn-group-sm" role="group" aria-label="Basic mixed styles example">
                            <button type="button" class="btn btn-danger" @click="checkout(room.id)">Checkout</button>
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
import router from '@/router'
import { API_DOMAIN } from '@/config'

const route = useRoute()
const collegeCode = ref(route.params.collegeCode)
const collegeID = ref(0)
const collegeName = ref('')
const collegeNumOccupants = ref(0)
const rooms = ref([])

async function checkout(room_id) {
    try {
        const response = await fetch(`${API_DOMAIN}/api/student/checkout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ room_id, college_id: collegeID.value })
        });

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 401) {
                router.push('/')
            }
            throw new Error(data.error || 'Failed to individual report')
        }

        await updateInfo();
    } catch (error) {
        console.error(error)
        alert(error)
    }
}

async function updateInfo() {
    collegeCode.value = route.params.collegeCode
    try {
        const res = await fetch(`${API_DOMAIN}/api/college/fromcode?code=${collegeCode.value}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        const data = await res.json();
        if (!res.ok) {
            if (res.status === 401) {
                router.push('/')
            }
            throw new Error(data.error || 'Failed to fetch college info')
        }
        collegeName.value = data['college'].name;
        collegeID.value = data['college'].id;
        collegeNumOccupants.value = data['college'].num_occupants;
    } catch (error) {
        console.error(error);
        alert(error);
    }

    try {
        const res = await fetch(`${API_DOMAIN}/api/college/occupied_rooms?college_id=${collegeID.value}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        const data = await res.json();
        if (!res.ok) {
            if (res.status === 401) {
                router.push('/')
            }
            throw new Error(data.error || 'Failed to fetch checked in rooms')
        }
        rooms.value = data;
    } catch (error) {
        console.error(error);
        alert(error);
    }
}

onMounted(async () => {
    updateInfo();
})

watch(() => route.params.collegeCode, async (newValue) => {
    collegeCode.value = newValue;
    await updateInfo();
})

</script>
  
<style scoped>
</style>