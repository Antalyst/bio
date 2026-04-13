<template>
  <div class="h-dvh w-full flex bg-slate-50 font-sans text-slate-900">
    <aside class="h-full w-64 bg-white border-r border-slate-200 flex flex-col shadow-sm">
      <div class="p-6 border-b border-slate-100">
        <h1 class="text-xl font-bold text-blue-600 flex items-center gap-2">
          <Icon name="lucide:fingerprint" class="w-8 h-8" />
          <span class="tracking-tight">BioAuth</span>
        </h1>
      </div>

      <nav class="flex-1 p-4 space-y-2">
        <NuxtLink
          to="/"
          class="flex items-center gap-3 p-3 rounded-xl text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-all duration-200"
          active-class="bg-blue-50 text-blue-600 font-bold shadow-sm"
        >
          <Icon name="lucide:layout-dashboard" class="w-5 h-5" />
          <span>Dashboard</span>
        </NuxtLink>

        <NuxtLink
          to="/admin/register"
          class="flex items-center gap-3 p-3 rounded-xl text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-all duration-200"
          active-class="bg-blue-50 text-blue-600 font-bold shadow-sm"
        >
          <Icon name="lucide:user-plus" class="w-5 h-5" />
          <span>Register Student</span>
        </NuxtLink>

        <NuxtLink
          to="/admin/verify"
          class="flex items-center gap-3 p-3 rounded-xl text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-all duration-200"
          active-class="bg-blue-50 text-blue-600 font-bold shadow-sm"
        >
          <Icon name="lucide:shield-check" class="w-5 h-5" />
          <span>Verify Fingerprint</span>
        </NuxtLink>
      </nav>

      <div class="p-4 border-t border-slate-100">
        <button
          @click="logout"
          class="flex items-center gap-3 w-full p-3 text-red-600 hover:bg-red-50 rounded-xl transition-all duration-200 group"
        >
          <Icon
            name="lucide:log-out"
            class="w-5 h-5 group-hover:translate-x-1 transition-transform"
          />
          <span class="font-semibold">Logout</span>
        </button>
      </div>
    </aside>

    <main class="flex-1 overflow-y-auto bg-slate-50">
      <header
        class="h-16 bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-10 px-8 flex items-center justify-between"
      >
        <h2 class="text-lg font-bold text-slate-800 capitalize">
          {{ $route.path.split("/").pop() || "Dashboard" }}
        </h2>
        <div class="flex items-center gap-2">
          <div
            class="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-bold"
          >
            BC
          </div>
        </div>
      </header>

      <div class="p-8">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
const router = useRouter();
const tokenCookie = useCookie("token");
const student = ref(null);

function logout() {
  localStorage.removeItem("token");
  tokenCookie.value = null;
  student.value = null;
  router.push("/");
}
</script>
