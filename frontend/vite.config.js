import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    outDir: 'static/frontend/dist',  // Adjust the outDir to be within the project root
    assetsDir: 'assets',  // Directory for bundled assets
    rollupOptions: {
      input: {
        main: '/src/main.js',  // Entry point for JavaScript
        portfolio: '/src/css/portfolio.css',  // Entry point for CSS
        blog: '/src/css/blog.css',
        complaints: '/src/css/complaints.css',
      },
    },
  },
});
