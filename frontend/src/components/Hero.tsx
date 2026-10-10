import { useEffect, useRef, useState } from 'react';
import { motion, useInView } from 'framer-motion';

// Animated tracking-path background for the hero
function HeroCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx: any = canvas.getContext('2d');

    let W = canvas.width = canvas.offsetWidth;
    let H = canvas.height = canvas.offsetHeight;

    type Particle = { x: number; y: number; vx: number; vy: number; age: number; maxAge: number };
    const particles: Particle[] = [];

    function spawn() {
      particles.push({
        x: Math.random() * W,
        y: Math.random() * H,
        vx: (Math.random() - 0.5) * 0.6,
        vy: (Math.random() - 0.5) * 0.6,
        age: 0,
        maxAge: 200 + Math.random() * 300,
      });
    }
    for (let i = 0; i < 40; i++) spawn();

    let af: number;
    function tick() {
      ctx.clearRect(0, 0, W, H);
      if (particles.length < 40) spawn();
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        // occasional direction jitter
        if (Math.random() < 0.02) {
          p.vx += (Math.random() - 0.5) * 0.4;
          p.vy += (Math.random() - 0.5) * 0.4;
          p.vx *= 0.7; p.vy *= 0.7;
        }
        p.age++;
        const life = p.age / p.maxAge;
        const alpha = life < 0.2 ? life / 0.2 : life > 0.8 ? (1 - life) / 0.2 : 1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 1.5, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0,212,255,${alpha * 0.35})`;
        ctx.fill();
        if (i > 0) {
          const prev = particles[i - 1];
          const dist = Math.hypot(p.x - prev.x, p.y - prev.y);
          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(prev.x, prev.y);
            ctx.strokeStyle = `rgba(0,212,255,${alpha * 0.06 * (1 - dist / 120)})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
        if (p.age >= p.maxAge) { particles.splice(i, 1); spawn(); }
      }
      af = requestAnimationFrame(tick);
    }
    tick();

    const ro = new ResizeObserver(() => {
      W = canvas.width = canvas.offsetWidth;
      H = canvas.height = canvas.offsetHeight;
    });
    ro.observe(canvas);
    return () => { cancelAnimationFrame(af); ro.disconnect(); };
  }, []);

  return (
    <canvas ref={canvasRef}
      style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0.6 }} />
  );
}

export default function HeroSection({ scrollToNext }: { scrollToNext: () => void }) {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 400),
      setTimeout(() => setPhase(2), 1200),
      setTimeout(() => setPhase(3), 2200),
      setTimeout(() => setPhase(4), 3200),
    ];
    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <section className="section" id="hero"
      style={{ minHeight: '100vh', overflow: 'hidden', position: 'relative', justifyContent: 'center', alignItems: 'center', textAlign: 'center' }}>
      <HeroCanvas />

      {/* Radial glow */}
      <div style={{
        position: 'absolute', inset: 0, pointerEvents: 'none',
        background: 'radial-gradient(ellipse 60% 50% at 50% 50%, rgba(255,45,85,0.07) 0%, transparent 70%)',
      }} />

      <div className="container" style={{ position: 'relative', zIndex: 2 }}>
        {/* Badge */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: phase >= 1 ? 1 : 0, y: phase >= 1 ? 0 : 16 }}
          transition={{ duration: 0.6 }} style={{ display: 'flex', justifyContent: 'center', marginBottom: '2rem' }}>
          <span className="badge badge-red">NFL Big Data Bowl 2027</span>
        </motion.div>

        {/* Main title */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: phase >= 2 ? 1 : 0 }} transition={{ duration: 0.8 }}>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 'clamp(3.5rem, 12vw, 9rem)', fontWeight: 700, lineHeight: 0.9, letterSpacing: '-0.02em', marginBottom: '1.5rem' }}>
            <span style={{ display: 'block', color: 'var(--white)' }}>BEYOND</span>
            <span style={{ display: 'block', color: 'var(--white)' }}>THE</span>
            <span className="text-cyan" style={{ display: 'block' }}>STOPWATCH</span>
          </h1>
        </motion.div>

        {/* Subtitle */}
        <motion.p initial={{ opacity: 0, y: 12 }} animate={{ opacity: phase >= 3 ? 1 : 0, y: phase >= 3 ? 0 : 12 }}
          transition={{ duration: 0.7 }}
          style={{ fontSize: 'clamp(1rem, 2.5vw, 1.3rem)', color: 'rgba(245,245,247,0.7)', maxWidth: 640, margin: '0 auto 1rem', lineHeight: 1.5 }}>
          Measuring Route-Ready Movement
        </motion.p>
        <motion.p initial={{ opacity: 0 }} animate={{ opacity: phase >= 3 ? 1 : 0 }} transition={{ duration: 0.7, delay: 0.2 }}
          style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'rgba(245,245,247,0.4)', maxWidth: 560, margin: '0 auto 3rem', lineHeight: 1.7 }}>
          How 10 Hz Combine tracking reveals movement characteristics that traditional stopwatch metrics may miss
        </motion.p>

        {/* CTA */}
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: phase >= 4 ? 1 : 0, y: phase >= 4 ? 0 : 12 }}
          transition={{ duration: 0.7 }}
          style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button className="btn btn-primary" onClick={scrollToNext}>
            Explore the Data ↓
          </button>
          <a className="btn btn-ghost" href="https://www.kaggle.com/competitions/nfl-big-data-bowl-2027" target="_blank" rel="noreferrer">
            Competition Page
          </a>
        </motion.div>

        {/* Scroll hint */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: phase >= 4 ? 1 : 0 }} transition={{ duration: 1, delay: 0.5 }}
          className="animate-float"
          style={{ marginTop: '4rem', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.15em', textTransform: 'uppercase', color: 'rgba(245,245,247,0.25)' }}>Scroll</span>
          <div style={{ width: 1, height: 40, background: 'linear-gradient(to bottom, rgba(255,45,85,0.5), transparent)' }} />
        </motion.div>
      </div>
    </section>
  );
}
