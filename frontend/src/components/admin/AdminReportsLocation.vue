<template>
    <div class="input-group mb-3">
        <span class="input-group-text">Name</span>
        <input type="text" list="locations" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" v-model="searchValue">
        <button class="btn btn-success input-group-text" @click="fetchIndividualReport(searchValue)">Search</button>
        <datalist id="locations">
            <option v-for="location in report['report']" :key="location.id" :value="location.location_name"></option>
        </datalist>
    </div>
    <div v-for="location in report['report']" :key="location.id">
        <h5>{{ location.location_name }}</h5>
        <div v-if="location['rooms'].length > 0" class="table-responsive">
            <table class="table table-striped table-sm">
                <thead>
                    <tr>
                        <th scope="col">Room Number</th>
                        <th scope="col">Occupant Count</th>
                        <th scope="col">College Breakup</th>
                        <th scope="col">Max Occupancy</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="room in location['rooms']" :key="location.id">
                        <td>{{ room.number }}</td>
                        <td>{{ room.num_students }}</td>
                        <td>
                            <span v-for="(count, collegeName) in room.college_counts" :key="collegeName">
                                <span class="text-success">{{ collegeName }}</span>: <span class="text-danger">{{ count }}</span>;
                            </span> 
                        </td>
                        <td>{{ room.max_occupancy }}</td>
                    </tr>
                    <tr>
                        <th>Total</th>
                        <th>{{location.total_students}}</th>
                    </tr>
                </tbody>
            </table>
        </div>
        <hr v-if="location['rooms'].length == 0">
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'

const report = ref([])

async function fetchIndividualReport(locationName) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/location/report?location_name=${locationName}`)
        report.value = await response.json()
    } catch (error) {
        console.error(error)
    }
}

async function fetchReport() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/location/report')
        report.value = await response.json()
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