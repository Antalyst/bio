<template>
    <div>
        <h2>Admin Login</h2>
        <form @submit.prevent="login">
            <div>
                <label>Username</label>
                <input v-model="username" required />
            </div>
            <div>
                <label>Password</label>
                <input type="password" v-model="password" required />
            </div>
            <button type="submit" :disabled="loading">{{ loading ? 'Signing in…' : 'Sign In' }}</button>
            <p v-if="error" style="color:red">{{ error }}</p>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
// useCookie is available globally in Nuxt 3

const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const apiBase = 'http://127.0.0.1:8000'

async function login() {
    error.value = ''
    loading.value = true
    try {
        const res = await fetch(`${apiBase}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username.value, password: password.value })
        })
        if (!res.ok) throw new Error('Invalid credentials')
        const data = await res.json()
        // Store token for client-side and SSR access
        localStorage.setItem('token', data.token)
        const tokenCookie = useCookie('token', { sameSite: 'lax', path: '/' })
        tokenCookie.value = data.token
        router.push('/admin/verify')
    } catch (e) {
        error.value = 'Invalid username or password'
    } finally {
        loading.value = false
    }
}
</script>

<style lang="scss" scoped>

</style>