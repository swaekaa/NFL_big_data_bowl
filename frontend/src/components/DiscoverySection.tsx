import { useRef, useState } from 'react';
import { motion, useInView } from 'framer-motion';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Line, ComposedChart } from 'recharts';
import { useWRData } from '../hooks/useData';

const CustomDot = (props: any) => {
  const { cx, cy, payload } = props;
  const sep = payload?.mean_separation ?? 2.5;
  // Normalize separation between roughly 2.0 (Low) and 3.5 (High)
  const t = Math.min(1, Math.max(0, (sep - 2.0) / 1.5));
  
  // Interpolate between Red (255,0,85) and Cyan (0,240,255)
  const r = Math.round(255 + (0 - 255) * t);
  const g = Math.round(0 + (240 - 0) * t);
  const b = Math.round(85 + (255 - 85) * t);
  
  return (
    <g>
      <circle cx={cx} cy={cy} r={6} fill={`rgba(${r},${g},${b},0.85)`} stroke="rgba(255,255,255,0.15)" strokeWidth={1} />
    </g>
  );
};

const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div style={{ background: 'rgba(0, 15, 14, 0.45)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 8, padding: '0.75rem 1rem', fontFamily: 'var(--font-mono)', fontSize: '0.7rem', minWidth: 180 }}>
      <div style={{ color: 'var(--red)', marginBottom: '0.3rem', fontSize: '0.65rem', letterSpacing: '0.08em', textTransform: 'uppercase' }}>WR Prospect</div>
      <div>Direction Change Rate: {d.direction_change_rate_SHORT_SHUTTLE?.toFixed(4)}</div>
      <div>Mean Separation: {d.mean_separation?.toFixed(2)} yds</div>
      {d.forty && <div>40-yd dash: {d.forty?.toFixed(2)}s</div>}
    </div>
  );
};

function LinearRegression(data: Array<{ x: number; y: number }>) {
  const n = data.length;
  if (n < 2) return null;
  const sumX = data.reduce((s, d) => s + d.x, 0);
  const sumY = data.reduce((s, d) => s + d.y, 0);
  const sumXY = data.reduce((s, d) => s + d.x * d.y, 0);
  const sumX2 = data.reduce((s, d) => s + d.x * d.x, 0);
  const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
  const intercept = (sumY - slope * sumX) / n;
  return { slope, intercept };
}

export default function DiscoverySection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });
  const wrData = useWRData();
  const [revealed, setRevealed] = useState(0);

  const chartData = (wrData ?? []).map(d => ({
    ...d,
    x: d.direction_change_rate_SHORT_SHUTTLE,
    y: d.mean_separation,
  }));

  const reg = chartData.length > 2 ? LinearRegression(chartData) : null;
  const xs = chartData.map(d => d.x);
  const lineData = reg && xs.length ? [
    { x: Math.min(...xs), y: reg.slope * Math.min(...xs) + reg.intercept },
    { x: Math.max(...xs), y: reg.slope * Math.max(...xs) + reg.intercept },
  ] : [];

  const STATS = [
    { label: 'Spearman ρ', val: '−0.645', note: 'Strong negative association', color: 'var(--red)' },
    { label: 'N', val: '28', note: 'WR prospects with full data', color: 'var(--white)' },
    { label: 'Raw p', val: '0.0002', note: 'Before multiple-testing correction', color: 'var(--cyan)' },
    { label: 'BH adj p', val: '≈ 0.168', note: 'After 140+ hypotheses correction', color: 'var(--orange)' },
  ];

  return (
    <section className="section" id="discovery" ref={ref} style={{ position: 'relative' }}>
      {/* dramatic red spotlight */}
      <div style={{
        position: 'absolute', inset: 0, pointerEvents: 'none',
        background: 'radial-gradient(ellipse 70% 40% at 50% 60%, rgba(255,45,85,0.06) 0%, transparent 70%)',
      }} />

      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <motion.p className="section-eyebrow text-red" initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}}>
          The Discovery
        </motion.p>
        <motion.h2 className="section-title" initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.1 }}>
          THEN WE LOOKED<br />
          <span className="text-red glow-red">AT THE NFL.</span>
        </motion.h2>
        <motion.p initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.2 }}
          style={{ color: 'rgba(245,245,247,0.6)', maxWidth: 560, marginBottom: '2.5rem', lineHeight: 1.7 }}>
          Receivers with higher Short Shuttle direction-change rates showed a negative exploratory association
          with how much separation they create as rookies when the ball is thrown. This negative trend is pretty clear across the board.
          not driven by a single outlier.
        </motion.p>

        {/* animated chart */}
        <motion.div initial={{ opacity: 0, y: 24 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.3 }}
          className="glass" style={{ padding: '1.75rem', borderRadius: 12, marginBottom: '2rem' }}>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)', marginBottom: '1rem' }}>
            direction_change_rate (Short Shuttle) vs mean_separation (Rookie Season, yards) · N=28 WRs
          </div>
          <ResponsiveContainer width="100%" height={360}>
            <ComposedChart data={chartData} margin={{ top: 20, right: 30, bottom: 40, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="x" name="DCR" type="number" domain={['dataMin - 0.05', 'dataMax + 0.05']}
                label={{ value: 'Direction Change Rate (events/s)', position: 'bottom', offset: 16, fill: 'rgba(245,245,247,0.35)', fontSize: 11, fontFamily: 'var(--font-mono)' }}
                tick={{ fill: 'rgba(245,245,247,0.35)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
                stroke="rgba(255,255,255,0.06)" />
              <YAxis dataKey="y" name="Separation" type="number" domain={['dataMin - 0.2', 'dataMax + 0.2']}
                label={{ value: 'Mean Separation (yds)', angle: -90, position: 'left', fill: 'rgba(245,245,247,0.35)', fontSize: 11, fontFamily: 'var(--font-mono)' }}
                tick={{ fill: 'rgba(245,245,247,0.35)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
                stroke="rgba(255,255,255,0.06)" />
              <Tooltip content={<CustomTooltip />} />
              <Scatter data={chartData} shape={<CustomDot />} />
              {lineData.length > 0 && (
                <Line data={lineData} dataKey="y" dot={false} stroke="rgba(255,45,85,0.6)"
                  strokeWidth={2} strokeDasharray="6 3" isAnimationActive={false} />
              )}
            </ComposedChart>
          </ResponsiveContainer>
          <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap', marginTop: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{ width: 12, height: 12, borderRadius: '50%', background: 'rgba(0,212,255,0.8)' }} />
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--muted)' }}>High separation</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{ width: 12, height: 12, borderRadius: '50%', background: 'rgba(255,45,85,0.8)' }} />
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--muted)' }}>Low separation</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{ width: 24, height: 2, background: 'rgba(255,45,85,0.5)', borderTop: '2px dashed rgba(255,45,85,0.5)' }} />
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--muted)' }}>OLS trend</span>
            </div>
          </div>
        </motion.div>

        {/* animated stats reveal */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '1rem' }}>
          {STATS.map((s, i) => (
            <motion.div key={s.label}
              initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.5 + i * 0.15 }}
              className="glass" style={{ padding: '1.25rem' }}>
              <div className="stat-value" style={{ fontSize: 'clamp(1.5rem, 3.5vw, 2.2rem)', color: s.color, marginBottom: '0.4rem' }}>
                {s.val}
              </div>
              <div className="stat-label">{s.label}</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'rgba(245,245,247,0.35)', marginTop: '0.3rem', lineHeight: 1.5 }}>
                {s.note}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
