import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, ResponsiveContainer } from 'recharts';
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
  return <circle cx={cx} cy={cy} r={6} fill={`rgba(${r},${g},${b},0.85)`} stroke="rgba(255,255,255,0.12)" strokeWidth={1} />;
};

const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div style={{ background: 'rgba(0, 15, 14, 0.45)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 8, padding: '0.75rem 1rem', fontFamily: 'var(--font-mono)', fontSize: '0.7rem' }}>
      <div style={{ color: 'var(--white)', marginBottom: '0.3rem' }}>nfl_id: {d.nfl_id}</div>
      <div>40-yd dash: <span style={{ color: 'var(--orange)' }}>{d.forty?.toFixed(2)}s</span></div>
      <div>DCR: <span style={{ color: 'var(--cyan)' }}>{d.direction_change_rate_SHORT_SHUTTLE?.toFixed(4)}</span></div>
      <div>Separation: <span style={{ color: d.mean_separation > 3 ? 'var(--cyan)' : 'var(--red)' }}>{d.mean_separation?.toFixed(2)} yds</span></div>
    </div>
  );
};

export default function SameStopwatchSection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });
  const wrData = useWRData();

  const chartData = (wrData ?? []).filter(d => d.forty != null).map(d => ({
    ...d,
    x: d.forty,
    y: d.direction_change_rate_SHORT_SHUTTLE,
  }));

  // find median forty
  const forties = chartData.map(d => d.forty!).sort((a, b) => a - b);
  const medianForty = forties.length ? forties[Math.floor(forties.length / 2)] : 4.47;

  return (
    <section className="section" id="same-stopwatch" ref={ref} >
      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <motion.p className="section-eyebrow" initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}}>
          The Scouting Idea
        </motion.p>
        <motion.h2 className="section-title" initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.1 }}>
          SAME STOPWATCH.<br />
          <span className="text-cyan">DIFFERENT MOVEMENT.</span>
        </motion.h2>

        <motion.p initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.2 }}
          style={{ color: 'rgba(245,245,247,0.6)', maxWidth: 580, marginBottom: '2.5rem', lineHeight: 1.7 }}>
          The vertical axis shows direction-change rate. The horizontal axis shows 40-yard dash time.
          Color represents NFL separation. Receivers sharing nearly identical 40-yard dash times
          can actually move completely differently on the field, leading to totally different outcomes in the NFL.
          Tracking provides the additional context that the stopwatch cannot.
        </motion.p>

        <motion.div initial={{ opacity: 0, y: 24 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.3 }}
          className="glass" style={{ padding: '1.75rem', borderRadius: 12, marginBottom: '2rem' }}>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)', marginBottom: '1rem' }}>
            40-yd dash vs direction_change_rate · color = mean NFL separation · N={chartData.length} WRs
          </div>
          <ResponsiveContainer width="100%" height={340}>
            <ScatterChart margin={{ top: 10, right: 40, bottom: 40, left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="x" type="number" name="40yd" domain={['auto', 'auto']}
                label={{ value: '40-Yard Dash Time (sec)', position: 'bottom', offset: 16, fill: 'rgba(245,245,247,0.35)', fontSize: 11, fontFamily: 'var(--font-mono)' }}
                tick={{ fill: 'rgba(245,245,247,0.35)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
                stroke="rgba(255,255,255,0.06)" tickFormatter={(v: number) => v.toFixed(2)} />
              <YAxis dataKey="y" type="number" name="DCR" domain={['auto', 'auto']}
                label={{ value: 'Direction Change Rate', angle: -90, position: 'insideLeft', fill: 'rgba(245,245,247,0.35)', fontSize: 11, fontFamily: 'var(--font-mono)' }}
                tick={{ fill: 'rgba(245,245,247,0.35)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
                stroke="rgba(255,255,255,0.06)" tickFormatter={(v: number) => v.toFixed(3)} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine x={medianForty} stroke="rgba(255,255,255,0.12)" strokeDasharray="4 4"
                label={{ value: `Median 40: ${medianForty.toFixed(2)}s`, position: 'top', fill: 'rgba(255,255,255,0.3)', fontSize: 9, fontFamily: 'var(--font-mono)' }} />
              <Scatter data={chartData} shape={<CustomDot />} />
            </ScatterChart>
          </ResponsiveContainer>
          {/* legend */}
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.75rem' }}>
            {[
              { color: 'rgba(0,212,255,0.8)', label: 'High separation' },
              { color: 'rgba(255,45,85,0.8)', label: 'Low separation' },
              { color: 'rgba(255,255,255,0.12)', label: 'Median 40-yd time' },
            ].map(l => (
              <div key={l.label} style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <div style={{ width: 10, height: 10, borderRadius: '50%', background: l.color }} />
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--muted)' }}>{l.label}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* message */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.5 }}
          className="glass" style={{ padding: '1.5rem 2rem' }}>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.2rem', marginBottom: '0.5rem', color: 'var(--cyan)' }}>
            Tracking should complement, not replace.
          </div>
          <div style={{ color: 'rgba(245,245,247,0.65)', lineHeight: 1.7, fontSize: '0.9rem' }}>
            The goal of this research isn't to dismiss the traditional 40-yard dash.
            it is to demonstrate that 10 Hz tracking may provide additional movement context
            that traditional stopwatch measurements cannot capture. When combined, they offer
            a more complete picture of an athlete's movement profile.
          </div>
        </motion.div>
      </div>
    </section>
  );
}
