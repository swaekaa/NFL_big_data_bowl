import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

const LIMITATIONS = [
  { val: '28', label: 'Wide Receivers', detail: 'Small Sample Size', sub: 'The dataset consists of only 28 wide receiver prospects who completed all drills and recorded subsequent rookie season separation metrics. This is too small for definitive conclusions, requiring validation against much larger multi-year Combine cohorts.' },
  { val: '140+', label: 'Hypotheses Tested', detail: 'Multiple Testing Bias', sub: 'By examining over 140 different feature-to-outcome combinations, the likelihood of finding false positives increases significantly. After applying rigorous Benjamini-Hochberg FDR correction, our primary result yields an adjusted p-value of ≈0.168, meaning it does not meet conventional strict significance thresholds.' },
  { val: 'Observational', label: 'Study Type', detail: 'No Causal Inference', sub: 'The associations observed between Combine tracking metrics and NFL separation are strictly correlational. We cannot prove that superior deceleration mechanics directly cause increased separation at the professional level without controlled experimental data.' },
  { val: 'In-Sample', label: 'R² Validation', detail: 'Lack of Generalization', sub: 'The explanatory power (R² values) reported by our Ridge regression model is strictly in-sample. Because N=24 is insufficient for reliable leave-one-out cross-validation or out-of-sample temporal validation, these R² metrics should not be treated as true predictive performance.' },
  { val: 'Unmeasured', label: 'Confounders', detail: 'Complex Football Context', sub: 'NFL separation is a highly complex metric influenced by dozens of external variables we did not control for, including quarterback quality, offensive scheme, defensive coverage schemes, route types, opponent talent, and target volume.' },
  { val: 'Controlled', label: 'Drill Context', detail: 'Not a Live Environment', sub: 'The Short Shuttle is a highly controlled, predictable environment in shorts and t-shirts. Moving optimally around stationary cones is fundamentally different from decelerating against live NFL defensive backs while processing complex zone coverages.' },
];

export default function LimitationsSection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });

  return (
    <section className="section" id="limitations" ref={ref} >
      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <motion.p className="section-eyebrow text-orange" initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}}>
          Limitations
        </motion.p>
        <motion.h2 className="section-title" initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.1 }}>
          PROMISING ≠<br />
          <span className="text-orange">PROVEN.</span>
        </motion.h2>
        <motion.p initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.2 }}
          style={{ color: 'rgba(245,245,247,0.6)', maxWidth: 560, marginBottom: '2.5rem', lineHeight: 1.7 }}>
          Scientific credibility requires transparency about what this analysis can and cannot conclude.
          The following limitations are important context for interpreting the findings.
        </motion.p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1rem' }}>
          {LIMITATIONS.map((lim, i) => (
            <motion.div key={lim.label}
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.3 + i * 0.1 }}
              className="glass"
              style={{ padding: '1.5rem', display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.6rem', marginBottom: '0.4rem', flexWrap: 'wrap' }}>
                  <span style={{ fontFamily: 'var(--font-display)', fontSize: '1.2rem', color: 'var(--orange)' }}>{lim.val}</span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'var(--muted)', letterSpacing: '0.05em', textTransform: 'uppercase' }}>{lim.label}</span>
                </div>
                <div style={{ fontFamily: 'var(--font-display)', fontSize: '1rem', marginBottom: '0.5rem', color: 'var(--white)' }}>{lim.detail}</div>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'rgba(245,245,247,0.5)', lineHeight: 1.6 }}>{lim.sub}</div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
