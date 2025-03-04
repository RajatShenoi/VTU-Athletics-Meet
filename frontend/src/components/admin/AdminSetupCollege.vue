<template>
    <div class="row">
        <div class="col-6">
            <h4>Existing colleges ({{ collegeCount }})</h4>
        </div>
        <div class="col-6 text-end">
            <div class="btn-group me-2">
                <button type="button" class="btn btn-sm btn-outline-secondary" @click="fetchColleges">Refresh</button>
                <button type="button" class="btn btn-sm btn-success" data-bs-toggle="modal" data-bs-target="#staticBackdrop">Add new college</button>
            </div>
        </div>  
    </div>
    <div class="table-responsive">
        <table class="table table-striped table-sm">
            <thead>
                <tr>
                    <th scope="col">Code</th>
                    <th scope="col">Name</th>
                    <th scope="col">Point of Contact</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="college in colleges['colleges']" :key="college.id">
                    <td>{{ college.code }}</td>
                    <td>{{ college.name }}</td>
                    <td>{{ college.poc }}</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="modal fade" id="staticBackdrop" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="staticBackdropLabel">Create a new college</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="collegeName" class="form-label">College Name</label>
                        <input type="text" class="form-control" id="collegeName" v-model="newCollege.name" placeholder="JNN College of Engineering" maxlength="100">
                    </div>
                    <div class="mb-3">
                        <label for="collegeCode" class="form-label">College Code</label>
                        <input type="text" class="form-control" id="collegeCode" v-model="newCollege.code" placeholder="JN" maxlength="3" minlength="2">
                    </div>
                    <div class="mb-3">
                        <label for="contactNumber" class="form-label">Contact Number</label>
                        <input type="tel" class="form-control" id="contactNumber" v-model="newCollege.poc" placeholder="8182225341" maxlength="10" minlength="10">
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-success" @click="createCollege">Create</button>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'

const colleges = ref([])
const collegeCount = ref(0)
const newCollege = ref({
    name: '',
    code: '',
    poc: ''
})

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
            throw new Error(data.error || 'Failed to fetch colleges')
        }
        colleges.value = data
        collegeCount.value = colleges.value['colleges'].length
    } catch (error) {
        console.error(error)
    }
}

async function createCollege() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/college/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify(newCollege.value)
        })
        const data = await response.json()
        if (response.ok) {
            await fetchColleges()
            newCollege.value.name = ''
            newCollege.value.code = ''
            newCollege.value.poc = ''
        } else {
            throw new Error(data.error || 'Failed to create college')
        }
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