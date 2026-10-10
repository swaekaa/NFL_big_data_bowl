import os
import re
from pathlib import Path

ROOT = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027")
SRC = ROOT / "frontend/src"
COMPONENTS = SRC / "components"

def main():
    # 1. Create DynamicGradientBackground component
    gradient_tsx = """import { useEffect, useState } from 'react';
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
"""
    with open(COMPONENTS / "DynamicGradientBackground.tsx", "w", encoding="utf-8") as f:
        f.write(gradient_tsx)

    # 2. Create CSS for the background
    gradient_css = """
.dynamic-bg-container {
  position: fixed;
  inset: 0;
  z-index: -10;
  overflow: hidden;
  background-color: #00110F;
}

.bg-base {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at center, #001A18 0%, #00110F 100%);
}

.parallax-wrapper {
  position: absolute;
  inset: -100px;
  pointer-events: none;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(140px);
  will-change: transform, opacity, left, top;
}

@media (prefers-reduced-motion: reduce) {
  .blob {
    transition: none !important;
    animation: none !important;
  }
}

.blob-turquoise {
  width: 70vw;
  height: 70vw;
  background: radial-gradient(circle, #00AFA5 0%, transparent 70%);
}

.blob-cyan {
  width: 50vw;
  height: 50vw;
  background: radial-gradient(circle, rgba(217, 255, 252, 0.8) 0%, #5DEBE2 40%, transparent 70%);
}

.blob-darkteal {
  width: 90vw;
  height: 90vw;
  background: radial-gradient(circle, #002522 0%, transparent 70%);
}

.noise-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.035;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  mix-blend-mode: overlay;
}
"""
    with open(COMPONENTS / "DynamicGradient.css", "w", encoding="utf-8") as f:
        f.write(gradient_css)

    # 3. Clean up App.tsx to include the background
    with open(SRC / "App.tsx", "r", encoding="utf-8") as f:
        app_content = f.read()

    if "import DynamicGradientBackground" not in app_content:
        app_content = app_content.replace(
            "import HeroSection from './components/Hero';",
            "import HeroSection from './components/Hero';\nimport DynamicGradientBackground from './components/DynamicGradientBackground';"
        )
        app_content = app_content.replace(
            "<div className=\"min-h-screen text-white\">",
            "<div className=\"min-h-screen text-white\">\n      <DynamicGradientBackground />"
        )
        with open(SRC / "App.tsx", "w", encoding="utf-8") as f:
            f.write(app_content)

    # 4. Clean up index.css and revert glass panels to dark premium glass
    with open(SRC / "index.css", "r", encoding="utf-8") as f:
        index_css = f.read()

    # Revert .glass
    glass_regex = r'\.glass\s*\{[^}]*\}'
    new_glass = """.glass {
  background: rgba(0, 15, 14, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  color: var(--white);
}"""
    index_css = re.sub(glass_regex, new_glass, index_css)
    
    # Remove all texture-X classes
    index_css = re.sub(r'\.texture-\d+\s*\{[^}]*\}', '', index_css)
    index_css = re.sub(r'\.texture-base\s*\{[^}]*\}', '', index_css)
    index_css = index_css.replace("/* Auto-generated user textures */", "")

    # Clean up heading styles
    index_css = re.sub(
        r'\.section-title\s*\{[^}]*\}',
        """.section-title {
  font-family: var(--font-display);
  font-size: clamp(2.2rem, 6vw, 4.5rem);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.01em;
  margin-bottom: 1.5rem;
  color: var(--white);
  text-shadow: 0 4px 20px rgba(0,0,0,0.5);
}""",
        index_css
    )
    
    # Remove global text-shadows
    index_css = re.sub(r'/\* Global text shadow for readability \*/.*?\}\s*\}?', '', index_css, flags=re.DOTALL)
    index_css = re.sub(r'p\s*\{[^}]*\}', '', index_css)
    index_css = re.sub(r'\.glass p\s*\{[^}]*\}', '', index_css)

    with open(SRC / "index.css", "w", encoding="utf-8") as f:
        f.write(index_css)

    # 5. Clean up all components
    components = sorted(COMPONENTS.glob("*.tsx"))
    for comp_path in components:
        if comp_path.name == "DynamicGradientBackground.tsx": continue
        
        with open(comp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove <div className="texture-base ... />
        content = re.sub(r'\s*<div className="texture-base[^>]*/>', '', content)
        
        # Convert inline white backgrounds back to dark glass
        content = content.replace("background: 'rgba(255,255,255,0.95)'", "background: 'rgba(0, 15, 14, 0.45)', backdropFilter: 'blur(20px)'")
        content = content.replace("border: '1px solid rgba(0,0,0,0.1)'", "border: '1px solid rgba(255,255,255,0.08)'")
        content = content.replace("color: '#122311'", "color: 'var(--white)'")
        
        # Restore chart axes
        content = content.replace("fill: '#444'", "fill: 'rgba(245,245,247,0.5)'")
        content = content.replace("fill: '#666'", "fill: 'rgba(245,245,247,0.35)'")
        content = content.replace("stroke: 'rgba(0,0,0,0.1)'", "stroke: 'rgba(255,255,255,0.04)'")
        content = content.replace('stroke="rgba(0,0,0,0.1)"', 'stroke="rgba(255,255,255,0.04)"')

        with open(comp_path, "w", encoding="utf-8") as f:
            f.write(content)

    print("Background system replaced with global dynamic WebGL-style animated gradient!")

if __name__ == "__main__":
    main()
