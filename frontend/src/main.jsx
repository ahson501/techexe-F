import React from 'react';
import ReactDOM from 'react-dom';
import Hero from './components/Hero';
import { initAnimations } from './components/Animations';

// Initialize animations when the DOM content is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  initAnimations();
});

ReactDOM.render(
  <React.StrictMode>
    <Hero />
  </React.StrictMode>,
  document.getElementById('root')
);


console.log("Main application logic initialized with Vite!");
