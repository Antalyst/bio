<template>
  <div class="w-full min-h-full bg-slate-50 p-6 font-sans">
    <div class="max-w-4xl mx-auto space-y-6">
      <div
        class="bg-white p-8 rounded-3xl shadow-sm border border-slate-200 flex flex-col md:flex-row md:items-center justify-between gap-4"
      >
        <div>
          <h2 class="text-2xl font-bold text-slate-900 tracking-tight">
            Student Enrollment
          </h2>
          <p class="text-slate-500">Secure Biometric Registration Portal</p>
        </div>
        <div class="flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-xl">
          <div class="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
          <span class="text-xs font-bold text-blue-700 uppercase tracking-widest"
            >Scanner Active</span
          >
        </div>
      </div>

      <transition name="fade-slide" mode="out-in">
        <div
          v-if="step === 'capture'"
          key="capture"
          class="bg-white rounded-3xl border border-slate-200 shadow-sm p-12 flex flex-col items-center justify-center min-h-[500px] text-center"
        >
          <div class="relative w-48 h-48 mb-8 flex items-center justify-center">
            <Icon name="lucide:fingerprint" class="absolute w-40 h-40 text-slate-100" />

            <Icon
              name="lucide:fingerprint"
              class="absolute w-40 h-40 text-blue-600 transition-all duration-1000 ease-in-out"
              :style="{ clipPath: progressClipPath }"
            />

            <transition name="scale-check">
              <div
                v-if="pressCount >= 3 && !isDuplicate"
                class="absolute inset-0 flex items-center justify-center bg-white rounded-full"
              >
                <Icon name="lucide:check-circle-2" class="w-32 h-32 text-green-500" />
              </div>
            </transition>

            <transition name="scale-check">
              <div
                v-if="isDuplicate"
                class="absolute inset-0 flex items-center justify-center bg-white rounded-full"
              >
                <Icon name="lucide:alert-circle" class="w-32 h-32 text-red-500" />
              </div>
            </transition>
          </div>

          <div class="space-y-4 max-w-sm">
            <h3 class="text-xl font-bold text-slate-900">
              <span v-if="isDuplicate" class="text-red-600">User Already Registered</span>
              <span v-else>{{
                pressCount < 3 ? "Fingerprint Requirement" : "Capture Complete"
              }}</span>
            </h3>
            <p class="text-slate-500">
              <span v-if="isDuplicate"
                >This fingerprint is already linked to <b>{{ registeredName }}</b> in our
                database.</span
              >
              <span v-else>
                {{
                  pressCount < 3
                    ? "Please tap your finger on the scanner 3 times to create a high-resolution template."
                    : "Processing biometric data..."
                }}
              </span>
            </p>

            <div v-if="!isDuplicate" class="flex justify-center gap-2 py-4">
              <div
                v-for="i in 3"
                :key="i"
                class="w-12 h-2 rounded-full transition-colors duration-500"
                :class="pressCount >= i ? 'bg-blue-600' : 'bg-slate-100'"
              ></div>
            </div>

            <button
              @click="isDuplicate ? window.location.reload() : startCapture()"
              :disabled="loading && !isDuplicate"
              class="w-full py-4 rounded-2xl font-bold transition-all active:scale-95 disabled:opacity-50"
              :class="
                isDuplicate
                  ? 'bg-red-600 hover:bg-red-700 text-white'
                  : 'bg-slate-900 hover:bg-black text-white'
              "
            >
              {{
                isDuplicate
                  ? "Try Different Finger"
                  : loading
                  ? "Waiting for Taps..."
                  : "Start Capture"
              }}
            </button>
            <button class="text-blue-400 font-semibold text-xl" v-if="isDuplicate" @click="restart()">
                Restart
            </button>
          </div>

          <div
            v-if="captureLog.length"
            class="mt-8 w-full max-w-md bg-slate-50 rounded-2xl p-4 text-left border border-slate-100"
          >
            <p
              class="text-[10px] uppercase font-bold text-slate-400 mb-2 tracking-widest"
            >
              System Logs
            </p>
            <div class="h-20 overflow-y-auto font-mono text-xs text-slate-500 space-y-1">
              <p v-for="(line, idx) in captureLog" :key="idx">> {{ line }}</p>
              <p v-if="isDuplicate" class="text-red-500 font-bold">
                > ERROR: DUPLICATE RECORD DETECTED
              </p>
            </div>
          </div>
        </div>

        <div
          v-else
          key="form"
          class="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden"
        >
          <div class="bg-slate-900 p-6 text-white flex items-center justify-between">
            <div class="flex items-center gap-3">
              <Icon name="lucide:user-plus" class="w-6 h-6" />
              <span class="font-bold">Personal Information</span>
            </div>
            <span
              class="text-xs bg-white/20 px-3 py-1 rounded-full border border-white/10 uppercase font-bold"
              >Step 2 of 2</span
            >
          </div>

          <form @submit.prevent="submit" class="p-8">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label class="text-xs font-bold text-slate-500 uppercase tracking-widest"
                  >Student Name</label
                >
                <input
                  v-model="form.student_name"
                  required
                  placeholder="Ex. Juan Dela Cruz"
                  class="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none transition"
                />
              </div>

              <div class="space-y-2">
                <label class="text-xs font-bold text-slate-500 uppercase tracking-widest"
                  >Examinee Number</label
                >
                <input
                  v-model="form.examinee_no"
                  required
                  placeholder="2025-0001"
                  class="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none transition"
                />
              </div>

              <div class="space-y-2">
                <label class="text-xs font-bold text-slate-500 uppercase tracking-widest"
                  >Birthdate</label
                >
                <input
                  type="date"
                  v-model="form.birthdate"
                  required
                  class="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none transition"
                />
              </div>

              <div class="space-y-2">
                <label class="text-xs font-bold text-slate-500 uppercase tracking-widest"
                  >Age</label
                >
                <input
                  type="number"
                  v-model.number="form.age"
                  readonly
                  class="w-full p-4 bg-slate-100 border border-slate-200 rounded-2xl text-slate-400 font-bold"
                />
              </div>

              <div class="md:col-span-2 space-y-2">
                <label class="text-xs font-bold text-slate-500 uppercase tracking-widest"
                  >Course Taken</label
                >
                <!-- <input
                  v-model="form.course_taken"
                  required
                  placeholder="Ex. BS Information Technology"
                  class="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none transition"
                /> -->
                <select 
                  v-model="form.course_taken" 
                  class="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none transition"
                >
                  <option value="" disabled>Please Select Course</option>

                  <option value="BS Information System">BS Information System</option>
                  <option value="BS Office Administration">BS Office Administration</option>
                  <option value="BS Criminology">BS Criminology</option>
                  <option value="BSED Major In Filipino">BSED Major In Filipino</option>
                  <option value="BSED Major In Mathematics">BSED Major In Mathematics</option>
                  <option value="BSED Major In Socail Studies">BSED Major In Socail Studies</option>
                  <option value="BS Elementary Education">BSED</option>
                  <option value="BS Physical Education">BSED Physical Education</option>
                  <option value="BS Arts in English">BA English</option>
                  <option value="BS Arts in History">BA History</option>
                </select>
              </div>

               <div class="md:col-span-2 space-y-2">
                <label class="text-xs font-bold text-slate-500 uppercase tracking-widest"
                  >Senior High School Strand</label
                >
                <!-- <input
                  v-model="form.course_taken"
                  required
                  placeholder="Ex. BS Information Technology"
                  class="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none transition"
                /> -->
                <select 
                  v-model="form.strand" 
                  class="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none transition"
                >
                  <option value="" disabled>Select SHS Strand</option>

                  <optgroup label="Academic Track">
                    <option value="STEM">STEM (Science, Technology, Engineering, and Mathematics)</option>
                    <option value="ABM">ABM (Accountancy, Business, and Management)</option>
                    <option value="HUMSS">HUMSS (Humanities and Social Sciences)</option>
                    <option value="GAS">GAS (General Academic Strand)</option>
                  </optgroup>

                  <optgroup label="TVL - ICT Specializations">
                    <option value="ICT-PROGRAMMING">ICT: Computer Programming</option>
                    <option value="ICT-ANIMATION">ICT: Animation</option>
                    <option value="ICT-CSS">ICT: Computer Systems Servicing (CSS)</option>
                    <option value="ICT-ILLUSTRATION">ICT: Illustration / Graphic Design</option>
                  </optgroup>

                  <optgroup label="Other TVL Tracks">
                    <option value="TVL-HE">TVL: Home Economics</option>
                    <option value="TVL-IA">TVL: Industrial Arts</option>
                    <option value="TVL-AFA">TVL: Agri-Fishery Arts</option>
                  </optgroup>

                  <optgroup label="Specialized Tracks">
                    <option value="Sports">Sports Track</option>
                    <option value="ArtsDesign">Arts and Design Track</option>
                  </optgroup>
                </select>
              </div>


              <div class="md:col-span-2 space-y-2">
                <label class="text-xs font-bold text-slate-500 uppercase tracking-widest"
                  >Home Address</label
                >
                <input
                  v-model="form.address"
                  required
                  placeholder="Street, Barangay, City"
                  class="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none transition"
                />
              </div>
            </div>

            <div
              class="mt-8 pt-8 border-t border-slate-100 flex flex-col md:flex-row gap-4 items-center justify-between"
            >
              <p v-if="message" class="text-sm font-bold text-blue-600">{{ message }}</p>
              <div v-else></div>
              <button
                type="submit"
                :disabled="submitting"
                class="w-full md:w-auto px-12 py-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-2xl shadow-xl shadow-blue-100 transition-all active:scale-95 disabled:grayscale"
              >
                {{ submitting ? "Processing..." : "Complete Registration" }}
              </button>
            </div>
          </form>
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.5s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
.scale-check-enter-active {
  animation: bounce-in 0.6s;
}
.scale-check-leave-active {
  animation: bounce-in 0.4s reverse;
}

@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}
</style>

<script setup>
import { ref, watch, computed, onBeforeUnmount } from "vue";

definePageMeta({ layout: "admin" });
const step = ref("capture");
const loading = ref(false);
const submitting = ref(false);
const message = ref("");
const captureLog = ref([]);
const capturedTemplateB64 = ref("");
const pressCount = ref(0);
const isDuplicate = ref(false);
const registeredName = ref("");
const apiBase = "http://127.0.0.1:8000";
let progressTimer = null;

const restart = ()=>{
    window.location.reload();
}

const form = ref({
  student_name: "",
  age: null,
  address: "",
  examinee_no: "",
  course_taken: "",
  strand: "",
  date_registered: new Date().toISOString().substr(0, 10),
  birthdate: "",
});

const progressClipPath = computed(() => {
  if (pressCount.value === 0) return "inset(100% 0 0 0)";
  if (pressCount.value === 1) return "inset(75% 0 0 0)";
  if (pressCount.value === 2) return "inset(30% 0 0 0)";
  return "inset(0% 0 0 0)";
});

watch(
  () => form.value.birthdate,
  (newVal) => {
    if (!newVal) {
      form.value.age = null;
      return;
    }
    const birthDate = new Date(newVal);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    form.value.age = age;
  }
);

function startPolling() {
  if (progressTimer) return;
  progressTimer = setInterval(async () => {
    try {
      const res = await fetch(`${apiBase}/register-progress`);
      const data = await res.json();
      if (Array.isArray(data.log)) captureLog.value = data.log;
      if (typeof data.count === "number") pressCount.value = data.count;

      if (data.status === "already_registered") {
        isDuplicate.value = true;
        registeredName.value = data.student.student_name;
        clearInterval(progressTimer);
        progressTimer = null;
        loading.value = false;
      } else if (["done", "error"].includes(data.status)) {
        clearInterval(progressTimer);
        progressTimer = null;
      }
    } catch {}
  }, 500);
}

async function startCapture() {
  isDuplicate.value = false;
  loading.value = true;
  message.value = "Waiting for 3 taps…";
  try {
    pressCount.value = 0;
    captureLog.value = [];
    startPolling();
    const res = await fetch(`${apiBase}/register-start`, { method: "POST" });
    const data = await res.json();

    if (data.status === "already_registered") {
      isDuplicate.value = true;
      registeredName.value = data.student.student_name;
      loading.value = false;
      return;
    }

    capturedTemplateB64.value = data.fingerprint_template_b64;

    setTimeout(() => {
      if (!isDuplicate.value) {
        step.value = "form";
        message.value = "Fingerprint captured. Please fill the form.";
      }
    }, 500);
  } catch (e) {
    message.value = "Failed to capture fingerprint.";
  } finally {
    loading.value = false;
  }
}

async function submit() {
  submitting.value = true;
  try {
    const payload = {
      ...form.value,
      fingerprint_template_b64: capturedTemplateB64.value,
    };

    const response = await fetch(`${apiBase}/register-save`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error("Network response was not ok");

    message.value = "Successfully Registered!";

    setTimeout(() => {
      window.location.reload();
    }, 2000);
  } catch (e) {
    message.value = "Error saving to database.";
    console.error(e);
  } finally {
    submitting.value = false;
  }
}

onBeforeUnmount(() => {
  if (progressTimer) clearInterval(progressTimer);
});
</script>
