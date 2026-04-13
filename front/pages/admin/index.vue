<template>
  <div class="p-6 bg-slate-50 min-h-screen font-sans">
    <div class="max-w-7xl mx-auto space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-blue-100 text-blue-600 rounded-2xl">
              <Icon name="lucide:users" class="w-6 h-6" />
            </div>
            <div>
              <p class="text-slate-500 text-sm font-bold uppercase tracking-wider">
                Total Examinees
              </p>
              <h4 class="text-2xl font-black text-slate-900">{{ students.length }}</h4>
            </div>
          </div>
        </div>

        <div
          class="md:col-span-2 bg-slate-900 p-6 rounded-3xl shadow-xl flex flex-col md:flex-row items-center justify-between gap-4"
        >
          <div class="text-white">
            <h3 class="font-bold text-lg">Export Batch Record</h3>
            <p class="text-slate-400 text-xs">Download list by registration month</p>
          </div>
          <div class="flex gap-2 bg-white/10 p-2 rounded-2xl">
            <select
              v-model="exportParams.month"
              class="bg-transparent text-white text-sm outline-none p-2 cursor-pointer"
            >
              <option class="text-slate-900" value="01">January</option>
              <option class="text-slate-900" value="02">February</option>
              <option class="text-slate-900" value="03">March</option>
              <option class="text-slate-900" value="04">April</option>
              <option class="text-slate-900" value="05">May</option>
              <option class="text-slate-900" value="06">June</option>
              <option class="text-slate-900" value="07">July</option>
              <option class="text-slate-900" value="08">August</option>
              <option class="text-slate-900" value="09">September</option>
              <option class="text-slate-900" value="10">October</option>
              <option class="text-slate-900" value="11">November</option>
              <option class="text-slate-900" value="12">December</option>
            </select>
            <select
              v-model="exportParams.year"
              class="bg-transparent text-white text-sm outline-none p-2 cursor-pointer"
            >
              <option
                v-for="y in [2024, 2025, 2026]"
                :key="y"
                :value="y"
                class="text-slate-900"
              >
                {{ y }}
              </option>
            </select>
            <button
              @click="downloadBatch"
              class="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded-xl font-bold flex items-center gap-2 transition"
            >
              <Icon name="lucide:download" class="w-4 h-4" /> Export Excel
            </button>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
          <h3 class="font-bold text-slate-800 mb-4 flex items-center gap-2">
            <Icon name="lucide:pie-chart" class="text-blue-500" /> Course Distribution
          </h3>
          <div id="courseChart" class="h-64"></div>
        </div>

        <div
          class="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm flex flex-col justify-center items-center text-center"
        >
          <Icon name="lucide:award" class="w-12 h-12 text-yellow-500 mb-2" />
          <h4 class="text-slate-500 font-bold uppercase text-xs tracking-widest">
            Most Enrolled Course
          </h4>
          <p class="text-2xl font-black text-slate-900">{{ topCourse }}</p>
        </div>
      </div>

      <div class="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center">
          <h3 class="font-bold text-slate-800 flex items-center gap-2">
            <Icon name="lucide:database" class="w-5 h-5 text-blue-500" /> Examinee
            Database
          </h3>
          <div class="relative">
            <input
              v-model="search"
              placeholder="Search student..."
              class="pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm outline-none focus:ring-2 focus:ring-blue-500"
            />
            <Icon
              name="lucide:search"
              class="absolute left-3 top-2.5 w-4 h-4 text-slate-400"
            />
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead
              class="bg-slate-50 text-slate-400 text-[10px] uppercase font-bold tracking-widest"
            >
              <tr>
                <th class="p-4">Examinee No</th>
                <th class="p-4">Name</th>
                <th class="p-4">Course</th>
                <th class="p-4">Reg. Date</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50 text-sm">
              <tr
                v-for="s in filteredStudents"
                :key="s.id"
                class="hover:bg-blue-50/50 transition-colors"
              >
                <td class="p-4 font-mono font-bold text-blue-600">{{ s.examinee_no }}</td>
                <td class="p-4 font-bold text-slate-800">{{ s.student_name }}</td>
                <td class="p-4 text-slate-600">{{ s.course_taken }}</td>
                <td class="p-4 text-slate-400">{{ s.date_registered }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import Highcharts from "highcharts";

definePageMeta({ layout: "admin" });

const students = ref([]);
const search = ref("");
const exportParams = ref({
  month: new Date().toISOString().slice(5, 7),
  year: 2025,
});
const courseStats = computed(() => {
  const counts = {};
  students.value.forEach((s) => {
    counts[s.course_taken] = (counts[s.course_taken] || 0) + 1;
  });
  return Object.entries(counts).map(([name, y]) => ({ name, y }));
});

const topCourse = computed(() => {
  if (courseStats.value.length === 0) return "N/A";
  return [...courseStats.value].sort((a, b) => b.y - a.y)[0].name;
});

const initChart = () => {
  Highcharts.chart("courseChart", {
    chart: { type: "pie", backgroundColor: "transparent" },
    title: { text: "" },
    plotOptions: {
      pie: {
        innerSize: "60%",
        dataLabels: { enabled: true, format: "{point.name}: {point.y}" },
      },
    },
    series: [
      {
        name: "Students",
        data: courseStats.value,
      },
    ],
    credits: { enabled: false },
  });
};

const fetchStudents = async () => {
  try {
    const data = await $fetch("http://127.0.0.1:8000/students");
    students.value = data;
    initChart();
  } catch (err) {
    console.error("Failed to fetch students", err);
  }
};

watch(students, () => {
  initChart();
});

const filteredStudents = computed(() => {
  if (!search.value) return students.value;
  return students.value.filter(
    (s) =>
      s.student_name.toLowerCase().includes(search.value.toLowerCase()) ||
      s.examinee_no.includes(search.value)
  );
});

const downloadBatch = () => {
  const url = `http://127.0.0.1:8000/export-batch?month=${exportParams.value.month}&year=${exportParams.value.year}`;
  window.open(url, "_blank");
};

onMounted(() => {
  fetchStudents();
});
</script>
