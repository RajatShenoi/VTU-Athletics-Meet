<template>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 class="h2">Check out</h1>
    </div>
    <div class="mb-2">
        Use the below input field to search for the college you'd like to checkout using its name or code and click "find" to search for occupied rooms.
    </div>
    <div class="input-group mb-2">
        <input v-model="collegeInput" type="text" list="colleges" class="form-control" placeholder="College Code / Name" aria-label="College code / name" aria-describedby="submit-button">
        <RouterLink :to="`/admin/checkout/${collegeCode}`" :class="{ disabled: buttonDisabled }" class="btn btn-danger" type="button" id="submit-button" :disabled="buttonDisabled">Check out</RouterLink>
        <datalist id="colleges">
            <option v-for="college in colleges['colleges']" :key="college.code" :value="`${college.code} - ${college.name}`"></option>
        </datalist>
    </div>
    <RouterView />
</template>
  
<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

const colleges = ref([])
const collegeInput = ref('')
const buttonDisabled = ref(true)

const collegeCode = computed(() => {
    return collegeInput.value.split(' - ')[0]
})

watch(collegeInput, (newValue) => {
    const collegeName = newValue.split(' - ')[1]?.trim()
    buttonDisabled.value = !colleges.value['colleges'].some(college => college.name === collegeName)
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
            throw new Error(data.error || 'Failed to individual report')
        }
        colleges.value = data
    } catch (error) {
        console.error(error)
        alert(error)
    }
}

onMounted(() => {
    fetchColleges()
})

</script>
  
<style scoped>
.disabled {
    pointer-events: none;
    opacity: 0.5;
}
</style>