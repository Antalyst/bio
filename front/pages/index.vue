<template>
  <div
    class="w-full h-dvh flex items-center justify-center bg-[url('@/public/assets/login.png')] bg-cover bg-bottom bg-no-repeat text-white px-40"
  >
    <section class="flex gap-4">
      <div
        class="bg-white text-black space-y-2 flex flex-col items-center justify-center p-10 rounded-tl-md rounded-bl-md"
      >
        <h2 class="text-2xl font-semibold text-blue pb-10">Admin Login</h2>
        <form @submit.prevent="login">
          <div class="w-80 flex flex-col gap-4">
            <div class="w-full space-y-2">
              <label class="block text-form-label font-secondary text-secondary-700"
                >Username</label
              >
              <input
                class="w-full border-b-2 outline-none focus:border-blue-500"
                v-model="username"
                required
              />
            </div>
            <div class="w-full">
              <label class="block text-form-label font-secondary text-secondary-700">
                Password
              </label>

              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                class="w-full border-b-2 bg-transparent py-2 outline-none transition-colors focus:border-blue-500"
                required
              />

              <div class="flex items-center gap-2 mt-2">
                <input
                  id="show-password"
                  type="checkbox"
                  v-model="showPassword"
                  class="w-4 h-4 rounded border-secondary-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
                />
                <label
                  for="show-password"
                  class="text-helper-text font-secondary text-secondary-600 cursor-pointer select-none"
                >
                  Show password
                </label>
              </div>
            </div>
          </div>

          <button
            class="w-full shadow-lg mt-8 py-2 bg-blue-400 rounded-md text-white"
            type="submit"
            :disabled="loading"
          >
            {{ loading ? "Signing in…" : "Sign In" }}
          </button>
          <p
            v-if="error"
            class="text-red-500 my-4 bg-red-200/30 p-2 text-center rounded-md"
          >
            {{ error }}
          </p>
        </form>
      </div>
      <div class="">
        <div class="p-5 border-r-4 border-b-4">
          <div class="p-5 border-r-4 border-b-4 flex flex-col">
            <div>
              <h1 class="text-[5em] font-extrabold leading-[1em] max-w-[800px]">
                Your Fingerprint, Your Key.
              </h1>
              <h4 class="pt-5 pb-2">Bago City College</h4>
              <p class="max-w-96 p-2 rounded-lg bg-[#595757]/50">
                "Ensuring every student wins fairly by protecting against exam proxies,
                maintaining absolute integrity so that your hard work truly counts."
              </p>
            </div>
            <div class="flex w-full justify-end pt-20 gap-2">
              <img class="w-12" src="@/public/assets/BCC.png" alt="" />
              <img class="w-12" src="@/public/assets/BSIS.png" alt="" />
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const username = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");
const showPassword = ref(false);
const apiBase = "http://127.0.0.1:8000";

async function login() {
  error.value = "";
  loading.value = true;
  try {
    const res = await fetch(`${apiBase}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username.value, password: password.value }),
    });
    if (!res.ok) throw new Error("Invalid credentials");
    const data = await res.json();

    localStorage.setItem("token", data.token);
    const tokenCookie = useCookie("token", { sameSite: "lax", path: "/" });
    tokenCookie.value = data.token;
    router.push("/admin/verify");
  } catch (e) {
    error.value = "Invalid username or password";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped></style>
