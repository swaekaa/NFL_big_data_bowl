import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

const PIPELINE = [
  { step: '01', label: 'COMBINE RESULTS', sub: '510 prospects · 2023–2025 draft classes', color: 'var(--red)' },
  { step: '02', label: '10 Hz TRACKING', sub: 'combine_tracking.csv · 463k+ frames', color: 'var(--orange)' },
  { step: '03', label: 'FEATURE ENGINEERING', sub: 'direction_change_rate + 20+ kinematic features', color: 'var(--cyan)' },
  { step: '04', label: 'PLAYER MAPPING', sub: 'nfl_id join · WR rookie-season filter', color: 'var(--blue)' },
  { step: '05', label: 'NFL GAME TRACKING', sub: 'player_play.csv + game_tracking 2023–2025', color: 'var(--orange)' },
  { step: '06', label: 'ROOKIE-SEASON OUTCOME', sub: 'mean_separation at pass forward · N=28 WRs', color: 'var(--red)' },
];

export default function DataSection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });

  return (
    <section className="section" id="data" ref={ref}>
      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <motion.div initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ duration: 0.6 }}>
          <p className="section-eyebrow">The Data</p>
          <h2 className="section-title">
            FROM COMBINE<br />
            <span className="text-cyan">TO THE FIELD.</span>
          </h2>
          <p style={{ color: 'rgba(245,245,247,0.6)', maxWidth: 560, marginBottom: '3rem', lineHeight: 1.7 }}>
            The pipeline uses strictly pre-draft Combine data to predict strictly post-draft rookie NFL outcomes.
            This preserves the scouting direction and avoids temporal leakage.
          </p>
        </motion.div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
          {PIPELINE.map((step, i) => (
            <motion.div key={step.step}
              initial={{ opacity: 0, x: -32 }}
              animate={inView ? { opacity: 1, x: 0 } : {}}
              transition={{ duration: 0.5, delay: i * 0.12 }}
              style={{ display: 'flex', gap: '1.5rem', alignItems: 'flex-start' }}>
              {/* connector */}
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', flexShrink: 0, width: 48 }}>
                <div style={{
                  width: 36, height: 36, borderRadius: '50%', border: `2px solid ${step.color}`,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: step.color,
                  background: `${step.color}15`, flexShrink: 0,
                }}>
                  {step.step}
                </div>
                {i < PIPELINE.length - 1 && (
                  <motion.div
                    initial={{ scaleY: 0 }} animate={inView ? { scaleY: 1 } : {}}
                    transition={{ duration: 0.4, delay: i * 0.12 + 0.3 }}
                    style={{ width: 1, height: 48, background: `linear-gradient(to bottom, ${step.color}60, ${PIPELINE[i+1].color}30)`, transformOrigin: 'top', marginTop: 4 }} />
                )}
              </div>
              {/* content */}
              <div style={{ paddingBottom: i < PIPELINE.length - 1 ? '1.5rem' : 0, paddingTop: '0.25rem' }}>
                <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.05rem', fontWeight: 600, color: 'var(--white)', marginBottom: '0.2rem' }}>
                  {step.label}
                </div>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'rgba(245,245,247,0.45)' }}>
                  {step.sub}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* key numbers */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.9, duration: 0.6 }}
          style={{ marginTop: '3rem', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '1rem' }}>
          {[
            { val: '510', label: 'Prospects' },
            { val: '463k+', label: 'Tracking Frames' },
            { val: '28', label: 'WR Observations' },
            { val: '10 Hz', label: 'Sampling Frequency' },
          ].map(s => (
            <div key={s.label} className="glass" style={{ padding: '1.25rem 1rem', textAlign: 'center' }}>
              <div className="stat-value text-cyan" style={{ fontSize: 'clamp(1.8rem, 4vw, 2.5rem)' }}>{s.val}</div>
              <div className="stat-label" style={{ marginTop: '0.25rem' }}>{s.label}</div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
