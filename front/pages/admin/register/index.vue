<template>
    <div>
        <div v-if="step === 'capture'">
            <p>Place the same finger on the scanner 3 times…</p>
            <button :disabled="loading" @click="startCapture">{{ loading ? 'Waiting for device…' : 'Start Capture' }}</button>
            <p v-if="message">{{ message }}</p>
            <ul v-if="captureLog.length">
                <li v-for="(line, idx) in captureLog" :key="idx">{{ line }}</li>
            </ul>
        </div>

        <form v-else @submit.prevent="submit">
            <div>
                <label>Student Name</label>
                <input v-model="form.student_name" required />
            </div>
            <div>
                <label>Age</label>
                <input type="number" v-model.number="form.age" required />
            </div>
            <div>
                <label>Address</label>
                <input v-model="form.address" required />
            </div>
            <div>
                <label>Examinee No</label>
                <input v-model="form.examinee_no" required />
            </div>
            <div>
                <label>Course Taken</label>
                <input v-model="form.course_taken" required />
            </div>
            <div>
                <label>Date Registered</label>
                <input type="date" v-model="form.date_registered" required />
            </div>
            <div>
                <label>Birthdate</label>
                <input type="date" v-model="form.birthdate" required />
            </div>
            <button type="submit" :disabled="submitting">{{ submitting ? 'Saving…' : 'Save' }}</button>
        </form>
    </div>
    
</template>

<script setup>
import { ref } from 'vue'

const step = ref('capture')
const loading = ref(false)
const submitting = ref(false)
const message = ref('')
const captureLog = ref([])
const capturedTemplateB64 = ref('')

const form = ref({
    student_name: '',
    age: null,
    address: '',
    examinee_no: '',
    course_taken: '',
    date_registered: '',
    birthdate: '',
})

const apiBase = 'http://127.0.0.1:8000'

async function startCapture() {
    loading.value = true
    message.value = 'Waiting for 3 taps…'
    try {
        const res = await fetch(`${apiBase}/register-start`, { method: 'POST' })
        if (!res.ok) throw new Error('Capture failed')
        const data = await res.json()
        if (data.status === 'already_registered') {
            step.value = 'capture'
            message.value = 'This user is already registered.'
            captureLog.value = []
            return
        }
        capturedTemplateB64.value = data.fingerprint_template_b64
        captureLog.value = data.capture_log || []
        step.value = 'form'
        message.value = 'Fingerprint captured. Please fill the form.'
    } catch (e) {
        message.value = 'Failed to capture fingerprint.'
    } finally {
        loading.value = false
    }
}

async function submit() {
    submitting.value = true
    try {
        const payload = { ...form.value, fingerprint_template_b64: capturedTemplateB64.value }
        const res = await $fetch(`${apiBase}/register-save`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        })
        if (!res.ok) throw new Error('Save failed')
        message.value = 'Saved successfully.'
    } catch (e) {
        message.value = 'Failed to save.'
    } finally {
        submitting.value = false
    }
}
</script>

<style lang="scss" scoped>

</style>