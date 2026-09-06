import { defineConfig } from 'vite'
import { react } from 'vite-plugin-react' 

export default defineConfig({
  plugins: ['@vitejs/plugin-react'],
  test: {
    environment: 'jsdom',
    setupFiles: './tests/setup.js'
  }
})