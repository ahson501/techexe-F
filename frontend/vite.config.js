import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'static/frontend/dist',
    assetsDir: 'assets',
    rollupOptions: {
      input: {
        main: './src/main.jsx', // Main JavaScript entry
        portfolio: './src/css/portfolio.css',  // CSS entry for Portfolio app
        blog: './src/css/blog.css',  
        a_and_a_plants: './src/css/a_and_a_plants.css',         // CSS entry for Blog app
        complaints: './src/css/complaints.css', // CSS entry for Complaints app
        home: './src/css/home.css',            // CSS entry for Home app
      },
    },
  },
  server: {
    open: true,
    watch: {
      usePolling: true,
    },
  },
});
