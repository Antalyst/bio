/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {
      fontFamily: {
        'primary': ['Inter', 'sans-serif'], 
        'secondary': ['Roboto', 'ui-sans-serif', 'system-ui'],
      },
      fontSize: {
        'primary-title': ['1.875rem', { lineHeight: '2.25rem', fontWeight: '700' }],  
        'secondary-title': ['1.5rem', { lineHeight: '2rem', fontWeight: '600' }],
        'form-label': ['0.875rem', { lineHeight: '1.25rem', fontWeight: '500' }],  
        'body-text': ['1rem', { lineHeight: '1.5rem', fontWeight: '400' }],        
        'helper-text': ['0.75rem', { lineHeight: '1rem', fontWeight: '400' }],
        'helper-text': ['0.75rem', { lineHeight: '1rem' }],
        'primary-title': ['1.875rem', { lineHeight: '2.25rem', fontWeight: '700' }],     
      },
      colors: {
       
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          800: '#1e293b',
          900: '#0f172a',
        },
        primary: {
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      },
    },
  },
  plugins: [],
}