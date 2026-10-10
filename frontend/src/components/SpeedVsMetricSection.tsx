import { useRef, useState } from 'react';
import { motion, useInView } from 'framer-motion';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { useWRData } from '../hooks/useData';

const METRICS = [
  { key: 'forty', label: '40-Yard Dash', rho: 0.06, unit: 'sec' },
  { key: 'ten_yd_split', label: '10-Yard Split', rho: -0.05, unit: 'sec' },
  { key: 'short_shuttle', label: 'Short Shuttle Time', rho: -0.18, unit: 'sec' },
  { key: 'three_cone', label: '3-Cone Time', rho: 0.40, unit: 'sec' },
  { key: 'vertical', label: 'Vertical Jump', rho: -0.11, unit: 'in' },
  { key: 'broad_jump', label: 'Broad Jump', rho: -0.08, unit: 'in' },
];

const CustomDot = (props: any) => {
  const { cx, cy } = props;
  return <circle cx={cx} cy={cy} r={5} fill="rgba(0,212,255,0.7)" stroke="rgba(0,212,255,0.3)" strokeWidth={1} />;
};

const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div style={{ background: 'rgba(0, 15, 14, 0.45)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 8, padding: '0.75rem 1rem', fontFamily: 'var(--font-mono)', fontSize: '0.7rem' }}>
      <div style={{ color: 'var(--cyan)', marginBottom: '0.3rem' }}>nfl_id: {d.nfl_id}</div>
      <div>DCR: {d.x?.toFixed(4)}</div>
      <div>Traditional: {d.y?.toFixed(3)}</div>
    </div>
  );
};

export default function SpeedVsMetricSection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });
  const wrData = useWRData();
  const [selected, setSelected] = useState(0);

  const metric = METRICS[selected];
  const chartData = (wrData ?? [])
    .filter(d => d[metric.key as keyof typeof d] != null)
    .map(d => ({ x: d.direction_change_rate_SHORT_SHUTTLE, y: d[metric.key as keyof typeof d], nfl_id: d.nfl_id }));

  const rhoColor = Math.abs(metric.rho) < 0.15 ? 'var(--cyan)' : metric.rho < -0.3 ? 'var(--red)' : 'var(--orange)';

  return (
    <section className="section" id="speed-comparison" ref={ref} >
      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <motion.p className="section-eyebrow" initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}}>Movement vs Speed</motion.p>
        <motion.h2 className="section-title" initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.1 }}>
          NOT JUST<br />
          <span className="text-cyan">STRAIGHT-LINE SPEED.</span>
        </motion.h2>
        <motion.p initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.2 }}
          style={{ color: 'rgba(245,245,247,0.6)', maxWidth: 560, marginBottom: '2rem', lineHeight: 1.7 }}>
          If <code style={{ color: 'var(--orange)' }}>direction_change_rate</code> were simply measuring speed,
          we would expect a strong correlation with the 40-yard dash. The near-zero correlation suggests it is
          capturing a different movement characteristic.
        </motion.p>

        {/* metric picker */}
        <motion.div initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.3 }}
          style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '2rem' }}>
          {METRICS.map((m, i) => (
            <button key={m.key} onClick={() => setSelected(i)}
              style={{
                padding: '0.4rem 0.9rem', borderRadius: 100, fontFamily: 'var(--font-mono)', fontSize: '0.65rem',
                letterSpacing: '0.05em', border: '1px solid', cursor: 'pointer', transition: 'all 0.2s',
                background: selected === i ? 'rgba(0,212,255,0.12)' : 'transparent',
                borderColor: selected === i ? 'rgba(0,212,255,0.5)' : 'var(--border)',
                color: selected === i ? 'var(--cyan)' : 'var(--muted)',
              }}>
              {m.label}
            </button>
          ))}
        </motion.div>

        {/* rho display */}
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={inView ? { opacity: 1, scale: 1 } : {}} transition={{ delay: 0.35 }}
          style={{ display: 'flex', gap: '2rem', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
          <div className="stat-block">
            <div className="stat-value" style={{ fontSize: 'clamp(2.5rem, 6vw, 4rem)', color: rhoColor }}>
              ρ = {metric.rho > 0 ? '+' : ''}{metric.rho.toFixed(2)}
            </div>
            <div className="stat-label">Spearman correlation with {metric.label}</div>
          </div>
          {Math.abs(metric.rho) < 0.2 && (
            <div className="badge badge-cyan" style={{ fontSize: '0.7rem', padding: '0.4rem 0.9rem' }}>
              Near-zero → distinct dimension
            </div>
          )}
        </motion.div>

        {/* scatter chart */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.45 }}
          className="glass" style={{ padding: '1.5rem', borderRadius: 12 }}>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)', marginBottom: '1rem' }}>
            direction_change_rate vs {metric.label} (N={chartData.length} WRs with full data)
          </div>
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <ScatterChart margin={{ top: 10, right: 30, bottom: 30, left: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="x" name="DCR" type="number" domain={['auto', 'auto']}
                  label={{ value: 'Direction Change Rate (events/s)', position: 'bottom', offset: 12, fill: 'rgba(245,245,247,0.35)', fontSize: 11, fontFamily: 'var(--font-mono)' }}
                  tick={{ fill: 'rgba(245,245,247,0.35)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
                  stroke="rgba(255,255,255,0.06)" />
                <YAxis dataKey="y" name={metric.label} type="number" domain={['auto', 'auto']}
                  label={{ value: metric.label, angle: -90, position: 'left', offset: 0, fill: 'rgba(245,245,247,0.35)', fontSize: 11, fontFamily: 'var(--font-mono)' }}
                  tick={{ fill: 'rgba(245,245,247,0.35)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
                  stroke="rgba(255,255,255,0.06)" />
                <Tooltip content={<CustomTooltip />} />
                <Scatter data={chartData} shape={<CustomDot />} />
              </ScatterChart>
            </ResponsiveContainer>
          ) : (
            <div style={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--muted)', fontFamily: 'var(--font-mono)', fontSize: '0.75rem' }}>
              No data available for this metric combination
            </div>
          )}
        </motion.div>
      </div>
    </section>
  );
}
