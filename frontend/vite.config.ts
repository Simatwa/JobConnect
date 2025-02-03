import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    hmr: {
      overlay: false,
      timeout: 30000 // Increase timeout to 30 seconds
    },
    watch: {
      usePolling: true,
      interval: 1000
    }
  },
  build: {
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: undefined
      }
    }
  },
  optimizeDeps: {
    force: true // Force dependency pre-bundling
  }
})