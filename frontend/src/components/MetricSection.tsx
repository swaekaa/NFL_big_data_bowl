import { useRef, useState } from 'react';
import { motion, useInView } from 'framer-motion';

const FORMULA = '( angle_diff + 180 ) % 360 − 180';

function AngleWrapDemo() {
  const [fromAngle, setFromAngle] = useState(359);
  const toAngle = 1;
  const naive = Math.abs(toAngle - fromAngle);
  const correct = Math.abs(((toAngle - fromAngle + 180) % 360) - 180);

  return (
    <div className="glass" style={{ padding: '1.5rem 2rem', borderRadius: 12, marginTop: '1.5rem' }}>
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--cyan)', letterSpacing: '0.1em', marginBottom: '1rem', textTransform: 'uppercase' }}>
        Interactive: Angular Wraparound
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '2rem', alignItems: 'center' }}>
        <div>
          <label style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)', display: 'block', marginBottom: '0.4rem' }}>
            From angle: {fromAngle}°
          </label>
          <input type="range" min={270} max={359} value={fromAngle}
            onChange={e => setFromAngle(Number(e.target.value))}
            style={{ width: 160, accentColor: 'var(--cyan)' }} />
        </div>
        <div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'var(--muted)' }}>To angle: {toAngle}°</div>
        </div>
        <div style={{ display: 'flex', gap: '1.5rem' }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--red)', marginBottom: '0.25rem' }}>NAÏVE |b−a|</div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.8rem', color: 'var(--red)' }}>{naive}°</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', color: 'rgba(255,45,85,0.6)' }}>WRONG</div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--cyan)', marginBottom: '0.25rem' }}>CIRCULAR DIFF</div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.8rem', color: 'var(--cyan)' }}>{correct}°</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', color: 'rgba(0,212,255,0.6)' }}>CORRECT</div>
          </div>
        </div>
      </div>
      <div style={{ marginTop: '1rem', fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'rgba(245,245,247,0.4)', borderTop: '1px solid var(--border)', paddingTop: '0.75rem' }}>
        Formula: <span style={{ color: 'var(--cyan)' }}>{FORMULA}</span>
      </div>
    </div>
  );
}

function ThresholdDemo() {
  const [threshold, setThreshold] = useState(20);
  // Illustrative: as threshold increases, fewer events detected
  const events = Math.round(18 * Math.max(0, (45 - threshold) / 35));

  return (
    <div className="glass" style={{ padding: '1.5rem 2rem', borderRadius: 12, marginTop: '1rem' }}>
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--orange)', letterSpacing: '0.1em', marginBottom: '1rem', textTransform: 'uppercase' }}>
        Interactive: Direction-Change Threshold (Illustrative)
      </div>
      <label style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)', display: 'block', marginBottom: '0.4rem' }}>
        Threshold: {threshold}°
      </label>
      <input type="range" min={5} max={45} step={5} value={threshold}
        onChange={e => setThreshold(Number(e.target.value))}
        style={{ width: '100%', accentColor: 'var(--orange)', marginBottom: '1rem' }} />
      <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
        <div className="stat-block">
          <div className="stat-value text-orange" style={{ fontSize: 'clamp(2rem, 5vw, 3rem)' }}>{events}</div>
          <div className="stat-label">Events detected per attempt</div>
        </div>
        <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'var(--muted)', maxWidth: 280, lineHeight: 1.6 }}>
          We used a threshold of <strong style={{ color: 'var(--orange)' }}>20°</strong>. This was chosen specifically to detect meaningful changes in direction while filtering out tiny micro-corrections.
        </div>
      </div>
      <div style={{ marginTop: '0.75rem', fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'rgba(245,245,247,0.3)', fontStyle: 'italic' }}>
        Event counts are illustrative. Actual counts vary by player.
      </div>
    </div>
  );
}

export default function MetricSection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });
  const [showFormula, setShowFormula] = useState(false);

  return (
    <section className="section" id="metric" ref={ref}>
      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <motion.p className="section-eyebrow" initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}}>The Metric</motion.p>
        <motion.h2 className="section-title" initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.1 }}>
          ENGINEERING THE<br />
          <span className="text-orange">MOVEMENT METRIC.</span>
        </motion.h2>

        {/* metric definition */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.2 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
            <code style={{ fontFamily: 'var(--font-mono)', fontSize: '1.1rem', color: 'var(--orange)', background: 'rgba(255,107,0,0.1)', padding: '0.4rem 0.8rem', borderRadius: 6, border: '1px solid rgba(255,107,0,0.2)' }}>
              direction_change_rate
            </code>
            <span className="badge badge-orange">Tracking-derived</span>
          </div>
          <p style={{ color: 'rgba(245,245,247,0.65)', maxWidth: 600, lineHeight: 1.7, marginBottom: '2rem' }}>
            This metric measures how frequently an athlete changes their heading
            changes by more than 20° per tracking frame (0.1 s), only while moving at speed.
            It is not a physiological measurement and does not directly measure hip mechanics or biomechanics.
          </p>
        </motion.div>

        {/* step-by-step definition */}
        <motion.div initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.3 }}
          style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
          {[
            { n: '1', label: 'Filter low-speed frames', detail: 'Speed ≥ 1 yd/s', color: 'var(--cyan)' },
            { n: '2', label: 'Compute angular change', detail: 'Circular diff: correct 0°/360° wraparound', color: 'var(--orange)' },
            { n: '3', label: 'Count threshold events', detail: '|Δangle| > 20° per frame', color: 'var(--red)' },
            { n: '4', label: 'Normalize by duration', detail: 'Events ÷ moving time → events/sec', color: 'var(--blue)' },
          ].map(s => (
            <div key={s.n} className="glass" style={{ padding: '1.25rem' }}>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: s.color, marginBottom: '0.4rem' }}>STEP {s.n}</div>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: '0.9rem', marginBottom: '0.3rem' }}>{s.label}</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)' }}>{s.detail}</div>
            </div>
          ))}
        </motion.div>

        {/* angular wraparound interactive */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.4 }}>
          <AngleWrapDemo />
        </motion.div>

        {/* threshold slider */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.5 }}>
          <ThresholdDemo />
        </motion.div>

        {/* expand formula */}
        <motion.div initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.6 }} style={{ marginTop: '1.5rem' }}>
          <button className="btn btn-ghost" onClick={() => setShowFormula(v => !v)} style={{ fontSize: '0.75rem' }}>
            {showFormula ? 'Hide' : 'Show'} Implementation Details
          </button>
          {showFormula && (
            <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}
              className="glass" style={{ marginTop: '1rem', padding: '1.5rem', borderRadius: 12, fontFamily: 'var(--font-mono)', fontSize: '0.75rem', lineHeight: 2, color: 'rgba(245,245,247,0.7)' }}>
              <div style={{ color: 'var(--muted)', marginBottom: '0.5rem' }}># Python (src/combine_features.py)</div>
              <div><span style={{ color: 'var(--orange)' }}>DT</span> = 0.1  <span style={{ color: 'var(--muted)' }}># 10 Hz</span></div>
              <div><span style={{ color: 'var(--orange)' }}>MIN_SPEED</span> = 1.0  <span style={{ color: 'var(--muted)' }}># yards/s</span></div>
              <div><span style={{ color: 'var(--orange)' }}>THRESHOLD</span> = 20.0  <span style={{ color: 'var(--muted)' }}># degrees</span></div>
              <div style={{ marginTop: '0.5rem' }}>
                <span style={{ color: 'var(--cyan)' }}>_circular_diff</span>(a, b) = (a − b + 180) % 360 − 180
              </div>
              <div>event_mask = |_circular_diff(d[i], d[i−1])| &gt; THRESHOLD</div>
              <div>direction_change_rate = sum(event_mask) / (n_frames × DT)</div>
            </motion.div>
          )}
        </motion.div>
      </div>
    </section>
  );
}
