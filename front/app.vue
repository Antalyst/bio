<template>
  <div>
    <button @click="verify">Verify</button>

    <div v-if="status === 'loading'">Place your finger on the scanner...</div>
    <div v-if="status === 'verifying'">Checking fingerprint in database...</div>
    <div v-if="status === 'success'">
      <h3>Fingerprint verified!</h3>
      <p><strong>Name:</strong> {{ student.student_name }}</p>
      <p><strong>Age:</strong> {{ student.age }}</p>
      <p><strong>Address:</strong> {{ student.address }}</p>
      <p><strong>Course:</strong> {{ student.course_taken }}</p>
      <p><strong>Birthdate:</strong> {{ student.birthdate }}</p>
    </div>
    <div v-if="status === 'error'">Fingerprint not found or something went wrong!</div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const status = ref('')
const student = ref({})

watch(status, (newStatus) => {
  if (newStatus === 'success') {
    console.log('✅ Verified! Student found.')
  } else if (newStatus === 'error') {
    alert('❌ No matching fingerprint found.')
  }
})

async function verify() {
  status.value = 'loading';

  try {
    status.value = 'verifying'

    const res = await $fetch('http://127.0.0.1:8000/register-user', {
      method: 'POST'
    })
    student.value = res
    status.value = 'success'
  } catch (err) {
    console.error('API error:', err)
    status.value = 'error'
  }
}
</script>

