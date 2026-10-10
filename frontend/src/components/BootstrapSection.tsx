import { useRef, useMemo } from 'react';
import { motion, useInView } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, ResponsiveContainer, Cell } from 'recharts';
import { useBootstrap } from '../hooks/useData';

const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: 'rgba(0, 15, 14, 0.45)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 8, padding: '0.75rem 1rem', fontFamily: 'var(--font-mono)', fontSize: '0.7rem' }}>
      <div>ρ range: {payload[0]?.payload?.range}</div>
      <div style={{ color: 'var(--cyan)' }}>Count: {payload[0]?.value}</div>
    </div>
  );
};

function buildHistogram(rhos: number[], bins = 30) {
  const min = Math.min(...rhos);
  const max = Math.max(...rhos);
  const step = (max - min) / bins;
  const data = Array.from({ length: bins }, (_, i) => ({
    x: min + i * step + step / 2,
    count: 0,
    range: `${(min + i * step).toFixed(3)} – ${(min + (i + 1) * step).toFixed(3)}`,
  }));
  for (const r of rhos) {
    const idx = Math.min(bins - 1, Math.floor((r - min) / step));
    data[idx].count++;
  }
  return data;
}

export default function BootstrapSection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });
  const boot = useBootstrap();

  const histData = useMemo(() => (boot ? buildHistogram(boot.rhos) : []), [boot]);

  return (
    <section className="section" id="bootstrap" ref={ref} >
      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <motion.p className="section-eyebrow text-cyan" initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}}>
          Statistical Robustness
        </motion.p>
        <motion.h2 className="section-title" initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.1 }}>
          5,000 RESAMPLES.<br />
          <span className="text-cyan">ALL NEGATIVE.</span>
        </motion.h2>
        <motion.p initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.2 }}
          style={{ color: 'rgba(245,245,247,0.6)', maxWidth: 560, marginBottom: '2.5rem', lineHeight: 1.7 }}>
          To test whether the correlation is driven by a few unusual players, we used
          player-level bootstrap resampling (5,000 iterations, seed=42). Across all resamples,
          the estimated Spearman ρ remained negative.
        </motion.p>

        {/* Bootstrap histogram from real data */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.3 }}
          className="glass" style={{ padding: '1.75rem', borderRadius: 12, marginBottom: '2rem' }}>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)', marginBottom: '1rem' }}>
            Bootstrap distribution of Spearman ρ · 5,000 iterations · player-level resampling
          </div>
          {histData.length > 0 && boot ? (
            <>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={histData} margin={{ top: 10, right: 30, bottom: 30, left: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                  <XAxis dataKey="x" type="number" domain={['auto', 'auto']}
                    label={{ value: 'Spearman ρ', position: 'bottom', offset: 12, fill: 'rgba(245,245,247,0.35)', fontSize: 11, fontFamily: 'var(--font-mono)' }}
                    tickFormatter={(v: number) => v.toFixed(2)}
                    tick={{ fill: 'rgba(245,245,247,0.35)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
                    stroke="rgba(255,255,255,0.06)" />
                  <YAxis tick={{ fill: 'rgba(245,245,247,0.35)', fontSize: 10, fontFamily: 'var(--font-mono)' }} stroke="rgba(255,255,255,0.06)" />
                  <Tooltip content={<CustomTooltip />} />
                  <ReferenceLine x={boot.ci_lower} stroke="rgba(255,255,255,0.4)" strokeDasharray="4 3"
                    label={{ value: `CI: ${boot.ci_lower.toFixed(3)}`, position: 'top', fill: 'rgba(255,255,255,0.5)', fontSize: 9, fontFamily: 'var(--font-mono)' }} />
                  <ReferenceLine x={boot.ci_upper} stroke="rgba(255,255,255,0.4)" strokeDasharray="4 3"
                    label={{ value: `CI: ${boot.ci_upper.toFixed(3)}`, position: 'top', fill: 'rgba(255,255,255,0.5)', fontSize: 9, fontFamily: 'var(--font-mono)' }} />
                  <ReferenceLine x={0} stroke="rgba(255,45,85,0.6)" strokeWidth={2}
                    label={{ value: '0', position: 'top', fill: 'rgba(255,45,85,0.8)', fontSize: 10, fontFamily: 'var(--font-mono)' }} />
                  <Bar dataKey="count" radius={[2, 2, 0, 0]}>
                    {histData.map((entry) => (
                      <Cell key={`cell-${entry.x}`}
                        fill={entry.x < boot.ci_lower || entry.x > boot.ci_upper
                          ? 'rgba(68,79,36,0.3)'
                          : 'var(--blue)'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', marginTop: '0.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <div style={{ width: 12, height: 12, borderRadius: 2, background: 'var(--blue)' }} />
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--muted)' }}>Within 95% CI</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <div style={{ width: 24, height: 2, borderTop: '2px dashed rgba(255,255,255,0.5)' }} />
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--muted)' }}>95% CI bounds</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <div style={{ width: 24, height: 2, borderTop: '2px solid rgba(255,45,85,0.6)' }} />
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--muted)' }}>ρ = 0 (no association)</span>
                </div>
              </div>
            </>
          ) : (
            <div style={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--muted)', fontFamily: 'var(--font-mono)', fontSize: '0.75rem' }}>
              Loading bootstrap data…
            </div>
          )}
        </motion.div>

        {/* Key numbers */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
          {[
            { label: '95% CI', val: '[−0.812, −0.337]', color: 'var(--cyan)', note: 'Entirely negative' },
            { label: 'Iterations', val: '5,000', color: 'var(--white)', note: 'Player-level resampling' },
            { label: 'Huber p', val: '0.0234', color: 'var(--orange)', note: 'Robust regression result' },
          ].map(s => (
            <motion.div key={s.label} initial={{ opacity: 0, y: 16 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.7 }}
              className="glass" style={{ padding: '1.25rem' }}>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: 'clamp(1.1rem, 3vw, 1.6rem)', color: s.color, marginBottom: '0.3rem' }}>
                {s.val}
              </div>
              <div className="stat-label">{s.label}</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'rgba(245,245,247,0.35)', marginTop: '0.3rem' }}>{s.note}</div>
            </motion.div>
          ))}
        </div>

        <motion.div initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.9 }}
          className="callout-warning" style={{ marginTop: '1.5rem' }}>
          <strong>Important:</strong> While bootstrap testing and Huber regression help reduce the impact of outliers, they don't eliminate the uncertainty completely. The
          multiple-testing concern. The BH-adjusted p-value (≈ 0.168) remains the primary multiple-testing summary.
        </motion.div>
      </div>
    </section>
  );
}
