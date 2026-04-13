<template>
  <div class="w-full min-h-full bg-slate-50 p-6 font-sans">
    <div class="max-w-5xl mx-auto space-y-6">
      <div
        class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-8 rounded-3xl shadow-sm border border-slate-200"
      >
        <div>
          <h2 class="text-2xl font-bold text-slate-900 tracking-tight">
            Examinee Authentication
          </h2>
          <p class="text-slate-500">Post-Exam Identity Verification Portal</p>
        </div>

        <button
          @click="verify"
          :disabled="status === 'loading' || status === 'verifying'"
          class="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-2xl shadow-lg shadow-blue-100 transition-all active:scale-95 disabled:grayscale disabled:cursor-not-allowed flex items-center gap-3"
        >
          <Icon
            v-if="status === 'loading' || status === 'verifying'"
            name="lucide:loader-2"
            class="animate-spin w-5 h-5"
          />
          <Icon v-else name="lucide:fingerprint" class="w-5 h-5" />
          {{
            status === "loading" || status === "verifying"
              ? "Processing..."
              : "Start Fingerprint Scan"
          }}
        </button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div
          class="lg:col-span-5 bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden flex flex-col items-center justify-center p-12 min-h-[400px] relative"
        >
          <div
            v-if="status === 'loading' || status === 'verifying'"
            class="absolute inset-0 flex items-center justify-center pointer-events-none"
          >
            <div class="ripple bg-[#4285F4] animate-ripple"></div>
            <div class="ripple bg-[#EA4335] animate-ripple delay-500"></div>
            <div class="ripple bg-[#FBBC05] animate-ripple delay-1000"></div>
            <div class="ripple bg-[#34A853] animate-ripple delay-1500"></div>
          </div>

          <div
            class="relative z-10 w-32 h-32 rounded-full mt-10 flex items-center justify-center transition-transform duration-500"
            :class="{ 'scale-110 shadow-blue-100': status === 'loading' }"
          >
            <Icon
              name="lucide:fingerprint"
              class="w-16 h-16 transition-colors duration-500"
              :class="{
                'text-blue-500':
                  status === '' || status === 'loading' || status === 'verifying',
                'text-green-500': status === 'success',
                'text-red-500': status === 'error',
              }"
            />
          </div>

          <div class="mt-1 text-center z-10">
            <h3 class="font-bold text-slate-900 text-lg">
              <span v-if="status === 'loading'">Place finger on glass</span>
              <span v-else-if="status === 'verifying'">Comparing Patterns...</span>
              <span v-else-if="status === 'success'" class="text-green-600"
                >Identity Confirmed</span
              >
              <span v-else-if="status === 'error'" class="text-red-600">Scan Failed</span>
              <span v-else>Scanner Ready</span>
            </h3>
            <p
              class="text-[10px] text-slate-400 mt-1 uppercase tracking-[0.2em] font-bold"
            >
              Biometric Authenticatng
            </p>
          </div>
        </div>

        <div class="lg:col-span-7">
          <transition name="slide-fade">
            <div
              v-if="status === 'success' && student"
              class="bg-white rounded-3xl border border-green-200 shadow-sm h-full overflow-hidden"
            >
              <div class="bg-green-600 p-4 text-white flex items-center gap-2">
                <Icon name="lucide:shield-check" class="w-6 h-6" />
                <span class="font-bold uppercase tracking-wider text-sm"
                  >Verified Examinee Profile</span
                >
              </div>
              <div class="p-8 grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label
                    class="block text-[10px] uppercase tracking-widest text-slate-400 font-bold mb-1"
                    >Full Name</label
                  >
                  <p class="text-lg font-bold text-slate-800">
                    {{ student.student_name }}
                  </p>
                </div>
                <div>
                  <label
                    class="block text-[10px] uppercase tracking-widest text-slate-400 font-bold mb-1"
                    >Examinee ID</label
                  >
                  <p class="text-lg font-bold text-slate-800">
                    {{ student.examinee_no }}
                  </p>
                </div>
                <div>
                  <label
                    class="block text-[10px] uppercase tracking-widest text-slate-400 font-bold mb-1"
                    >Assigned Course</label
                  >
                  <p class="text-lg font-bold text-slate-800">
                    {{ student.course_taken }}
                  </p>
                </div>
                <div>
                  <label
                    class="block text-[10px] uppercase tracking-widest text-slate-400 font-bold mb-1"
                    >Current Age</label
                  >
                  <p class="text-lg font-bold text-slate-800">
                    {{ student.age }} years old
                  </p>
                </div>
                <div class="md:col-span-2">
                  <label
                    class="block text-[10px] uppercase tracking-widest text-slate-400 font-bold mb-1"
                    >SHS Strand</label
                  >
                  <p
                    class="text-lg font-bold text-slate-800 italic border-l-4 border-green-100 pl-3"
                  >
                    {{ student.strand }}
                  </p>
                </div>
                <div class="md:col-span-2">
                  <label
                    class="block text-[10px] uppercase tracking-widest text-slate-400 font-bold mb-1"
                    >Registered Address</label
                  >
                  <p
                    class="text-lg font-bold text-slate-800 italic border-l-4 border-green-100 pl-3"
                  >
                    {{ student.address }}
                  </p>
                </div>
              </div>
            </div>

            <div
              v-else-if="status === 'error' || found"
              class="bg-red-50 border-2 border-dashed border-red-200 rounded-3xl p-12 h-full flex flex-col items-center justify-center text-center"
            >
              <div class="bg-red-100 p-4 rounded-full mb-4">
                <Icon name="lucide:user-x" class="w-12 h-12 text-red-600" />
              </div>
              <h3 class="text-xl font-bold text-red-800">Authentication Failed</h3>
              <p class="text-red-600 mt-2 max-w-xs">
                The fingerprint does not match any registered examinee for this session.
              </p>
              <button
                @click="status = ''"
                class="mt-6 text-sm font-bold text-red-700 underline underline-offset-4"
              >
                Try again
              </button>
            </div>

            <div
              v-else
              class="bg-white rounded-3xl border-2 border-dashed border-slate-200 p-12 h-full flex flex-col items-center justify-center text-center opacity-60"
            >
              <Icon name="lucide:database" class="w-16 h-16 text-slate-300 mb-4" />
              <p class="text-slate-500 font-medium">
                Scan results will appear here after verification.
              </p>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ripple {
  position: absolute;
  border-radius: 9999px;
  opacity: 0;
  pointer-events: none;
  width: 20px;
  height: 20px;
}

.animate-ripple {
  animation: ripple-animation 4s infinite cubic-bezier(0, 0.2, 0.8, 1);
}

.delay-500 {
  animation-delay: 0.5s;
}
.delay-1000 {
  animation-delay: 1s;
}
.delay-1500 {
  animation-delay: 1.5s;
}

@keyframes ripple-animation {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  100% {
    transform: scale(30);
    opacity: 0;
  }
}

.slide-fade-enter-active {
  transition: all 0.4s ease-out;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
</style>

<script setup>
import { ref } from "vue";

definePageMeta({ layout: "admin" });
const found = ref(false);
const status = ref("");
const student = ref(null);
const tokenCookie = useCookie("token");

async function verify() {
  status.value = "loading";
  found.value = false;
  student.value = null;

  try {
    status.value = "verifying";
    const token = tokenCookie.value || localStorage.getItem("token");

    const res = await $fetch("http://127.0.0.1:8000/verify-only", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    student.value = res;
    status.value = "success";
  } catch (err) {
    console.error("API error:", err);
    status.value = "error";
    found.value = true;
  }
}
</script>
