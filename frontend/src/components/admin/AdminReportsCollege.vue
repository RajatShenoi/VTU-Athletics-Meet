<template>
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

const report = ref([])

async function fetchReport() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/college/report')
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