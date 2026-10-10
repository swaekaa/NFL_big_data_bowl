import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

export default function MultipleTestingSection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });

  // show dots for 140+ hypotheses
  const N_HYPO = 140;
  const dots = Array.from({ length: N_HYPO }, (_, i) => i);

  return (
    <section className="section" id="multiple-testing" ref={ref}
      style={{ }}>
      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <motion.p className="section-eyebrow text-orange" initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}}>
          The Catch
        </motion.p>
        <motion.h2 className="section-title" initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.1 }}>
          STRONG SIGNAL ≠<br />
          <span className="text-orange">PROVEN DISCOVERY.</span>
        </motion.h2>

        <motion.p initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.2 }}
          style={{ color: 'rgba(245,245,247,0.65)', maxWidth: 580, marginBottom: '2.5rem', lineHeight: 1.7 }}>
          During exploratory analysis, more than <strong style={{ color: 'var(--orange)' }}>140 feature/outcome combinations</strong> were
          investigated across positions, drills, and outcomes. When this many hypotheses are tested,
          raw p-values alone can be misleading. The Benjamini-Hochberg False Discovery Rate (FDR)
          correction accounts for this.
        </motion.p>

        {/* 140 dots grid */}
        <motion.div initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.3 }}
          className="glass" style={{ padding: '1.5rem 2rem', borderRadius: 12, marginBottom: '2rem' }}>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)', marginBottom: '1rem' }}>
            {N_HYPO}+ hypotheses tested across positions × drills × outcomes
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(12px, 1fr))', gap: '6px', marginBottom: '1.5rem' }}>
            {dots.map(i => {
              // 1 primary result (red), 9 other raw significant (cyan), rest non-significant (dim)
              let bg = 'rgba(255,255,255,0.06)';
              let border = '1px solid rgba(255,255,255,0.02)';
              let shadow = 'none';
              
              if (i === 12) {
                bg = 'var(--red)';
                border = '1px solid rgba(255,45,85,0.5)';
                shadow = '0 0 8px rgba(255,45,85,0.6)';
              } else if ([4, 27, 45, 62, 88, 103, 115, 129, 137].includes(i)) {
                bg = 'var(--cyan)';
                border = '1px solid rgba(0,240,255,0.5)';
                shadow = '0 0 6px rgba(0,240,255,0.4)';
              }

              return (
                <motion.div key={i}
                  initial={{ opacity: 0, scale: 0.5 }} animate={inView ? { opacity: 1, scale: 1 } : {}}
                  transition={{ delay: 0.35 + i * 0.005 }}
                  style={{
                    aspectRatio: '1/1', borderRadius: 2,
                    background: bg, border, boxShadow: shadow
                  }}
                />
              );
            })}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontFamily: 'var(--font-mono)', fontSize: '0.65rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{ width: 10, height: 10, background: 'var(--red)', borderRadius: 2, boxShadow: '0 0 8px rgba(255,45,85,0.6)' }} />
              <span style={{ color: 'var(--red)' }}>Our primary result (WR direction_change_rate → mean_separation)</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{ width: 10, height: 10, background: 'var(--cyan)', borderRadius: 2, boxShadow: '0 0 6px rgba(0,240,255,0.4)' }} />
              <span style={{ color: 'var(--cyan)' }}>"Significant" before FDR correction (Raw p &lt; 0.05)</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{ width: 10, height: 10, background: 'rgba(255,255,255,0.06)', borderRadius: 2, border: '1px solid rgba(255,255,255,0.02)' }} />
              <span style={{ color: 'var(--muted)' }}>Not significant</span>
            </div>
          </div>
        </motion.div>

        {/* p-value transformation */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.6 }}
          style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
          <div className="glass" style={{ padding: '1.5rem', textAlign: 'center' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)', marginBottom: '0.5rem' }}>RAW p-VALUE</div>
            <div className="stat-value text-cyan" style={{ fontSize: '2.5rem' }}>0.0002</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'rgba(245,245,247,0.4)', marginTop: '0.4rem', lineHeight: 1.5 }}>
              Strong, but tested among 140+ hypotheses
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '2rem', color: 'var(--orange)' }}>
            →
          </div>

          <div className="glass" style={{ padding: '1.5rem', textAlign: 'center' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)', marginBottom: '0.5rem' }}>BH ADJUSTED p</div>
            <div className="stat-value text-orange" style={{ fontSize: '2.5rem' }}>≈ 0.168</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'rgba(245,245,247,0.4)', marginTop: '0.4rem', lineHeight: 1.5 }}>
              Does not meet conventional 0.05 threshold
            </div>
          </div>
        </motion.div>

        {/* honest callout */}
        <motion.div initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.8 }}
          className="callout-warning">
          <strong>Honest interpretation:</strong> The association is promising and robust under bootstrapping and
          outlier-resistant regression. However, because many hypotheses were tested and the FDR-adjusted
          p-value is 0.168, this result should be treated as an exploratory signal that warrants further
          validation with a larger group of players, rather than treating this as a confirmed finding just yet.
        </motion.div>
      </div>
    </section>
  );
}
