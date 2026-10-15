import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Relative base './' ensures asset URLs resolve properly on both Vercel (domain root)
// and GitHub Pages (repo subpath https://user.github.io/repo/).
export default defineConfig({
  plugins: [react()],
  base: './',
})
