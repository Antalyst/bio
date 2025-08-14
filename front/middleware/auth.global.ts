export default defineNuxtRouteMiddleware((to) => {
  if (process.server) return
  const token = localStorage.getItem('token') || useCookie<string | null>('token').value
  if (!token && to.path.startsWith('/admin')) {
    return navigateTo('/')
  }
  if (token && (to.path === '/' || to.path === '/login')) {
    return navigateTo('/admin/verify')
  }
});

