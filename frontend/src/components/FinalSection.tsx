import { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';

export default function FinalSection() {
  const [phase, setPhase] = useState(0);
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(([e]) => {
      if (e.isIntersecting && !visible) {
        setVisible(true);
        const timers = [
          setTimeout(() => setPhase(1), 400),
          setTimeout(() => setPhase(2), 2000),
          setTimeout(() => setPhase(3), 3800),
          setTimeout(() => setPhase(4), 5000),
        ];
        return () => timers.forEach(clearTimeout);
      }
    }, { threshold: 0.4 });
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [visible]);

  const easeOutExpo = [0.16, 1, 0.3, 1];

  return (
    <section className="section" id="conclusion" ref={ref}
      style={{ minHeight: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center', position: 'relative', overflow: 'hidden' }}>

      {/* Reverted dramatic radial gradient */}
      <div style={{
        position: 'absolute', inset: 0, pointerEvents: 'none',
        background: 'radial-gradient(ellipse 70% 60% at 50% 50%, rgba(255,45,85,0.07) 0%, transparent 70%)',
      }} />

      <div className="container" style={{ position: 'relative', zIndex: 1, padding: '0 2rem' }}>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: '4rem', 
          alignItems: 'center' 
        }}>
          
          {/* Left Column: The Big Statements */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            
            {/* Part 1 */}
            <motion.div 
              initial={{ opacity: 0, x: -30 }} 
              animate={{ opacity: phase >= 1 ? 1 : 0, x: phase >= 1 ? 0 : -30 }} 
              transition={{ duration: 1.5, ease: easeOutExpo }}>
              <p style={{ fontFamily: 'var(--font-display)', fontSize: 'clamp(1.5rem, 4vw, 2.5rem)', fontWeight: 700, lineHeight: 1.1, color: 'rgba(245,245,247,0.7)' }}>
                THE STOPWATCH<br />
                COMPRESSES MOVEMENT<br />
                INTO A NUMBER.
              </p>
            </motion.div>

            {/* Part 2 */}
            <motion.div 
              initial={{ opacity: 0, x: -30 }} 
              animate={{ opacity: phase >= 2 ? 1 : 0, x: phase >= 2 ? 0 : -30 }} 
              transition={{ duration: 1.5, ease: easeOutExpo }}>
              <p style={{ fontFamily: 'var(--font-display)', fontSize: 'clamp(1.5rem, 4vw, 2.5rem)', fontWeight: 700, lineHeight: 1.1, color: 'var(--cyan)' }}>
                TRACKING<br />
                PRESERVES<br />
                THE MOVEMENT ITSELF.
              </p>
            </motion.div>

            {/* Divider */}
            <motion.div 
              initial={{ scaleX: 0, opacity: 0 }} 
              animate={{ scaleX: phase >= 3 ? 1 : 0, opacity: phase >= 3 ? 1 : 0 }} 
              transition={{ duration: 1.2, ease: easeOutExpo }}
              style={{ height: 1, width: '100%', background: 'linear-gradient(to right, var(--red), transparent)', transformOrigin: 'left' }} />

            {/* Main title */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }} 
              animate={{ opacity: phase >= 3 ? 1 : 0, y: phase >= 3 ? 0 : 20 }} 
              transition={{ duration: 1.5, ease: easeOutExpo }}>
              <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 'clamp(3rem, 8vw, 6.5rem)', fontWeight: 700, lineHeight: 0.9, letterSpacing: '-0.02em', background: 'linear-gradient(135deg, var(--red), var(--orange))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
                BEYOND THE<br />STOPWATCH
              </h2>
            </motion.div>
          </div>

          {/* Right Column: Conclusion & CTA */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem' }}>
            
            {/* Final conclusion block */}
            <motion.div
              initial={{ opacity: 0, x: 30 }} 
              animate={{ opacity: phase >= 3 ? 1 : 0, x: phase >= 3 ? 0 : 30 }} 
              transition={{ duration: 1.2, delay: 0.4, ease: easeOutExpo }}>
              <p style={{ 
                color: 'rgba(245,245,247,0.7)', 
                lineHeight: 1.8, 
                fontSize: '1rem',
                background: 'rgba(0,15,14,0.45)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255,255,255,0.08)',
                padding: '2rem',
                borderRadius: '16px'
              }}>
                High-frequency tracking data from the Combine reveals a whole new layer of movement that a standard stopwatch just misses. 
                By looking at 28 wide receiver prospects, we found that how they handle changes of direction in the Short Shuttle drill 
                strongly predicts how much separation they will get during their rookie season in the NFL. Even after running rigorous 
                statistical tests, this connection held up strong, proving that there is real value hidden in the tracking data.
              </p>
            </motion.div>

            {/* CTA buttons */}
            <motion.div 
              initial={{ opacity: 0, y: 15 }} 
              animate={{ opacity: phase >= 4 ? 1 : 0, y: phase >= 4 ? 0 : 15 }} 
              transition={{ duration: 1, ease: easeOutExpo }}
              style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              <a className="btn badge-red" href="https://www.kaggle.com/competitions/nfl-big-data-bowl-2027" target="_blank" rel="noreferrer"
                style={{ padding: '0.8rem 2rem', fontSize: '0.9rem', fontWeight: 700, textDecoration: 'none', borderRadius: '100px' }}>
                VIEW ON KAGGLE
              </a>
              <a className="btn btn-ghost" href="https://github.com" target="_blank" rel="noreferrer"
                style={{ padding: '0.8rem 2rem', fontSize: '0.9rem', fontWeight: 600 }}>
                VIEW CODE
              </a>
            </motion.div>

            {/* Badge */}
            <motion.div 
              initial={{ opacity: 0 }} 
              animate={{ opacity: phase >= 4 ? 1 : 0 }} 
              transition={{ duration: 1, delay: 0.3 }}>
              <span className="badge badge-red" style={{ fontSize: '0.75rem', padding: '0.4rem 1rem' }}>
                NFL Big Data Bowl 2027
              </span>
            </motion.div>
          </div>
          
        </div>
      </div>
    </section>
  );
}
