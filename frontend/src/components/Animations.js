import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export const initAnimations = () => {
  // Example animations
  gsap.from(".hero h1", { y: -50, opacity: 0, duration: 1 });
  gsap.from(".cta-button", { scale: 0.9, opacity: 0, delay: 0.5, duration: 1 });

  // Scroll-triggered animations
  gsap.from(".feature", {
    scrollTrigger: ".feature",
    y: 100,
    opacity: 0,
    duration: 1.5,
    stagger: 0.3,
  });
};
