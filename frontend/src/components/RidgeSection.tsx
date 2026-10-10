import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell, ResponsiveContainer, LabelList } from 'recharts';

const RIDGE_DATA = [
  { model: 'Traditional Only', r2: 0.064, color: 'rgba(234,236,230,0.3)' },
  { model: 'Tracking Only', r2: 0.173, color: 'var(--cyan)' },
  { model: 'Trad + Tracking', r2: 0.242, color: 'var(--red)' },
];

const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: 'rgba(0, 15, 14, 0.45)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 8, padding: '0.75rem 1rem', fontFamily: 'var(--font-mono)', fontSize: '0.7rem' }}>
      <div style={{ color: 'var(--white)', marginBottom: '0.3rem' }}>{payload[0]?.payload?.model}</div>
      <div style={{ color: 'var(--cyan)' }}>In-sample R² = {payload[0]?.value?.toFixed(3)}</div>
    </div>
  );
};

export default function RidgeSection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });

  return (
    <section className="section" id="ridge" ref={ref}>
      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <motion.p className="section-eyebrow text-blue" initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}}>
          Model Comparison
        </motion.p>
        <motion.h2 className="section-title" initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.1 }}>
          DOES TRACKING<br />
          <span className="text-cyan">ADD INFORMATION?</span>
        </motion.h2>

        {/* warning banner */}
        <motion.div initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.2 }}
          className="callout-warning" style={{ marginBottom: '2rem', borderColor: 'var(--orange)' }}>
          <strong>Important caveat:</strong> These are <strong>in-sample explanatory R²</strong> values from a Ridge Regression fit on N≈24 players.
          They should not be interpreted as out-of-sample predictive performance or evidence that tracking generalizes to new cohorts.
          N=24 is too small for reliable leave-one-out or temporal validation.
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 24 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.3 }}
          className="glass" style={{ padding: '1.75rem', borderRadius: 12, marginBottom: '2rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)' }}>
              In-sample explanatory R² · Ridge Regression · N≈24 WRs
            </div>
            <span className="badge badge-orange">In-sample only</span>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={RIDGE_DATA} margin={{ top: 20, right: 40, bottom: 40, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="model"
                tick={{ fill: 'rgba(245,245,247,0.5)', fontSize: 11, fontFamily: 'var(--font-mono)' }}
                stroke="rgba(255,255,255,0.06)" />
              <YAxis domain={[0, 0.30]} tickFormatter={(v: number) => v.toFixed(2)}
                label={{ value: 'In-sample R²', angle: -90, position: 'insideLeft', fill: 'rgba(245,245,247,0.35)', fontSize: 11, fontFamily: 'var(--font-mono)' }}
                tick={{ fill: 'rgba(245,245,247,0.35)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
                stroke="rgba(255,255,255,0.06)" />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="r2" radius={[4, 4, 0, 0]}>
                {RIDGE_DATA.map((entry) => (
                  <Cell key={entry.model} fill={entry.color} fillOpacity={0.85} />
                ))}
                <LabelList dataKey="r2" position="top"
                  formatter={(v: number) => v.toFixed(3)}
                  style={{ fontFamily: 'var(--font-mono)', fontSize: 12, fill: 'rgba(245,245,247,0.7)' }} />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* narrative */}
        <motion.div initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.5 }}
          style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          {[
            { title: 'Traditional metrics alone', r2: '0.064', note: '40yd, split, shuttle, vertical, broad jump', color: 'rgba(234,236,230,0.3)' },
            { title: 'Tracking metric alone', r2: '0.173', note: 'direction_change_rate only', color: 'var(--cyan)' },
            { title: 'Combined model', r2: '0.242', note: 'Traditional + tracking features', color: 'var(--red)' },
          ].map(s => (
            <div key={s.title} className="glass" style={{ padding: '1.25rem' }}>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.8rem', color: s.color, marginBottom: '0.3rem' }}>{s.r2}</div>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: '0.85rem', marginBottom: '0.3rem' }}>{s.title}</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--muted)' }}>{s.note}</div>
            </div>
          ))}
        </motion.div>

        <motion.p initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.7 }}
          style={{ marginTop: '1.5rem', color: 'rgba(245,245,247,0.5)', fontFamily: 'var(--font-mono)', fontSize: '0.72rem', lineHeight: 1.7 }}>
          The tracking-only model explains ~2.7× more in-sample variance than traditional metrics alone.
          The combined model outperforms both individually. These are preliminary in-sample results;
          out-of-sample validation with larger cohorts is the appropriate next step.
        </motion.p>
      </div>
    </section>
  );
}
