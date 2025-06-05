import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      // '/api': 'http://localhost:8000',
      '/api': 'http://52.231.105.218:8000',
    },
  },
})
