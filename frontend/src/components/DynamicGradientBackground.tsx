import { useEffect, useState } from 'react';
import { motion, useScroll, useSpring, useTransform } from 'framer-motion';
import './DynamicGradient.css';

export default function DynamicGradientBackground() {
  const { scrollYProgress } = useScroll();
  // Smooth the scroll progress to avoid jitter
  const smoothProgress = useSpring(scrollYProgress, { damping: 40, stiffness: 200, mass: 1 });

  // Mouse Parallax
  const [mouse, setMouse] = useState({ x: 0, y: 0 });
  
  useEffect(() => {
    // Disable parallax on touch devices
    if (window.matchMedia('(pointer: coarse)').matches) return;

    const handleMouseMove = (e: MouseEvent) => {
      const x = (e.clientX / window.innerWidth) * 2 - 1;
      const y = (e.clientY / window.innerHeight) * 2 - 1;
      setMouse({ x, y });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Map scroll progress to blob properties for storytelling:
  // Top -> dark + mysterious
  // Data -> teal emerges
  // Tracking -> cyan intensifies
  // Discovery (climax ~0.5-0.6) -> brightest point
  // Multiple testing -> darkens
  // Conclusion -> returns to the opening atmosphere

  // Blob 1: Turquoise (Base Teal Aura)
  const b1X = useTransform(smoothProgress, [0, 0.3, 0.6, 0.8, 1], ["0%", "30%", "10%", "80%", "0%"]);
  const b1Y = useTransform(smoothProgress, [0, 0.3, 0.6, 0.8, 1], ["0%", "40%", "10%", "50%", "0%"]);
  const b1Scale = useTransform(smoothProgress, [0, 0.3, 0.6, 0.8, 1], [0.8, 1.2, 1.5, 0.9, 0.8]);
  const b1Opacity = useTransform(smoothProgress, [0, 0.2, 0.5, 0.8, 1], [0.3, 0.7, 0.9, 0.2, 0.3]);

  // Blob 2: Cyan Glow (The bright climax)
  const b2X = useTransform(smoothProgress, [0, 0.4, 0.6, 0.8, 1], ["100%", "60%", "40%", "20%", "100%"]);
  const b2Y = useTransform(smoothProgress, [0, 0.4, 0.6, 0.8, 1], ["10%", "50%", "60%", "90%", "10%"]);
  const b2Scale = useTransform(smoothProgress, [0, 0.4, 0.6, 0.8, 1], [0.3, 0.8, 2.0, 0.4, 0.3]);
  const b2Opacity = useTransform(smoothProgress, [0, 0.4, 0.6, 0.8, 1], [0.0, 0.4, 1.0, 0.05, 0.0]);

  // Blob 3: Deep Dark Teal (Creates depth and contrast)
  const b3X = useTransform(smoothProgress, [0, 0.5, 1], ["70%", "20%", "80%"]);
  const b3Y = useTransform(smoothProgress, [0, 0.5, 1], ["80%", "80%", "60%"]);

  return (
    <div className="dynamic-bg-container">
      <div className="bg-base" />
      
      <motion.div 
        className="parallax-wrapper"
        animate={{ x: mouse.x * -20, y: mouse.y * -20 }}
        transition={{ type: 'tween', ease: 'easeOut', duration: 1.5 }}
      >
        <motion.div 
          className="blob blob-turquoise"
          style={{ left: b1X, top: b1Y, scale: b1Scale, opacity: b1Opacity, x: '-50%', y: '-50%' }}
        />
        
        <motion.div 
          className="blob blob-cyan"
          style={{ left: b2X, top: b2Y, scale: b2Scale, opacity: b2Opacity, x: '-50%', y: '-50%' }}
        />

        <motion.div 
          className="blob blob-darkteal"
          style={{ left: b3X, top: b3Y, x: '-50%', y: '-50%' }}
        />
      </motion.div>

      <div className="noise-overlay" />
    </div>
  );
}
