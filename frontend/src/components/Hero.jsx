import { motion } from "framer-motion";
import "../css/home.css";
import "../css/portfolio.css";
import "../css/blog.css";
import "../css/complaints.css";
import "../css/a_a_plants.css";
import heroImage from "../images/TechExe.jpg";
import { useEffect } from 'react';


const sectionStyle = {
  backgroundImage: `url(${heroImage})`,
  height: "30vh",
  width: "100vw",
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "center",
  backgroundSize: "cover",
  backgroundPosition: "center",
  color: "white",
  textAlign: "center",
};

const buttonVariants = {
  hover: { scale: 1.1, backgroundColor: "#2980b9" },
  tap: { scale: 0.9 },
};

const Hero = () => {
  return (
    <section style={sectionStyle}>
      <motion.h1
        initial={{ opacity: 0, y: -100 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.5 }}
      >
        Welcome to TechExe
      </motion.h1>
      <lottie-player
        src="animation.json"
        background="transparent"
        speed="1"
        style={{ width: "300px", height: "300px" }}
        loop
        autoplay
      ></lottie-player>
      <motion.button
        variants={buttonVariants}
        whileHover="hover"
        whileTap="tap"
        className="cta-button"
      >
        Get Started
      </motion.button>
    </section>
  );
};
const App = () => {
    useEffect(() => {
        const mobileMenu = document.getElementById('mobile-menu');
        const navLinks = document.getElementById('nav-links');

        mobileMenu?.addEventListener('click', () => {
            navLinks?.classList.toggle('active');
        });

        return () => {
            mobileMenu?.removeEventListener('click', () => {
                navLinks?.classList.toggle('active');
            });
        };
    }, []);

    return (
        <nav>
            {/* JSX for Navbar */}
        </nav>
    );
};

const toggleMenu = () => {
  const navLinks = document.getElementById('nav-links');
  navLinks?.classList.toggle('active');
  const expanded = navLinks?.classList.contains('active');
  mobileMenu.setAttribute('aria-expanded', expanded ? 'true' : 'false');
};
export default Hero;
