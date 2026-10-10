import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

const container = { hidden: {}, show: { transition: { staggerChildren: 0.15 } } };
const item = { hidden: { opacity: 0, y: 24 }, show: { opacity: 1, y: 0, transition: { duration: 0.6 } } };

function TrajectoryComparison() {
  // Two illustrative SVG paths representing "jerky" vs "smooth" movement
  const smooth = "M 20 160 C 60 80, 100 40, 140 80 C 160 100, 160 120, 140 140 C 110 165, 80 165, 50 145 Z";
  const jerky  = "M 20 160 L 55 100 L 90 135 L 110 70 L 140 110 L 125 140 L 90 155 L 50 145 Z";

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginTop: '2rem' }}>
      {[
        { path: smooth, label: 'Player A', time: '4.42s', color: 'var(--cyan)', dcr: 'Lower direction-change rate', sep: '3.4 yds avg separation' },
        { path: jerky,  label: 'Player B', time: '4.43s', color: 'var(--red)',  dcr: 'Higher direction-change rate', sep: '2.2 yds avg separation' },
      ].map((p) => (
        <div key={p.label} className="glass" style={{ padding: '1.5rem', borderRadius: 12 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem', alignItems: 'center' }}>
            <span style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem' }}>{p.label}</span>
            <span className="badge" style={{ color: 'var(--white)', borderColor: 'var(--border)', background: 'rgba(255,255,255,0.05)', fontFamily: 'var(--font-mono)', fontSize: '0.7rem' }}>
              40yd: {p.time}
            </span>
          </div>
          <svg viewBox="0 0 160 180" style={{ width: '100%', height: 140 }}>
            <motion.path id={`path-${p.label.replace(' ', '-')}`} d={p.path} fill="none" stroke={p.color} strokeWidth={2.5}
              initial={{ pathLength: 0, opacity: 0 }} whileInView={{ pathLength: 1, opacity: 1 }}
              transition={{ duration: 1.8, ease: 'easeInOut' }} viewport={{ once: true }} />
            <motion.circle r={5} fill={p.color}
              initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} transition={{ delay: 1.6 }} viewport={{ once: true }}>
              <animateMotion dur="2s" repeatCount="indefinite" begin="1.8s">
                <mpath href={`#path-${p.label.replace(' ', '-')}`} />
              </animateMotion>
            </motion.circle>
          </svg>
          <div style={{ marginTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.3rem' }}>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: p.color }}>{p.dcr}</span>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)' }}>↳ {p.sep}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

export default function ProblemSection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });

  return (
    <section className="section" id="problem" ref={ref} >
      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <motion.div variants={container} initial="hidden" animate={inView ? 'show' : 'hidden'}>
          <motion.p className="section-eyebrow" variants={item}>The Problem</motion.p>
          <motion.h2 className="section-title" variants={item}>
            THE STOPWATCH SEES<br />
            <span className="text-red">THE FINISH.</span><br />
            TRACKING SEES<br />
            <span className="text-cyan">THE JOURNEY.</span>
          </motion.h2>

          <motion.p variants={item}
            style={{ fontSize: '1.05rem', color: 'rgba(245,245,247,0.65)', maxWidth: 580, lineHeight: 1.7, marginBottom: '1rem' }}>
            Traditional Combine measurements compress complex, multi-directional movement into single numbers.
            Two receivers can record nearly identical 40-yard dash times while taking meaningfully different paths
            through space. Route running requires far more than straight-line speed.
          </motion.p>

          <motion.div variants={item} className="divider" />

          <motion.div variants={item} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
            {[
              { icon: '→', label: 'Accelerate', color: 'var(--cyan)' },
              { icon: '↘', label: 'Decelerate', color: 'var(--cyan)' },
              { icon: '↺', label: 'Change Direction', color: 'var(--red)' },
              { icon: '→', label: 'Re-accelerate', color: 'var(--cyan)' },
            ].map((s) => (
              <div key={s.label} className="glass" style={{ padding: '1rem 1.25rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ fontSize: '1.4rem', color: s.color }}>{s.icon}</span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', letterSpacing: '0.05em' }}>{s.label}</span>
              </div>
            ))}
          </motion.div>

          <motion.p variants={item}
            style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--muted)', marginBottom: '0.5rem' }}>
            The following two hypothetical athletes share nearly identical 40-yard dash times.
            Their tracking signatures differ substantially.
          </motion.p>

          <motion.div variants={item}>
            <TrajectoryComparison />
          </motion.div>

          <motion.p variants={item}
            style={{ marginTop: '1.5rem', fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'rgba(245,245,247,0.3)', fontStyle: 'italic' }}>
            * Paths are illustrative. Same-stopwatch comparisons using actual project data appear in a later section.
          </motion.p>
        </motion.div>
      </div>
    </section>
  );
}
