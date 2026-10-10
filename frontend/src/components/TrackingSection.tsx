import { useRef, useEffect, useState } from 'react';
import { motion, useInView } from 'framer-motion';
import { useTrajectories } from '../hooks/useData';
import type { TrajectoryPoint } from '../types';

function TrajectoryCanvas({ points, color, label, dcr }: {
  points: TrajectoryPoint[]; color: string; label: string; dcr: number;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [drawn, setDrawn] = useState(false);

  useEffect(() => {
    if (!points || points.length === 0 || drawn) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx: any = canvas.getContext('2d');

    const xs = points.map(p => p.x);
    const ys = points.map(p => p.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs);
    const minY = Math.min(...ys), maxY = Math.max(...ys);
    const W = canvas.width, H = canvas.height;
    const pad = 24;

    function toCanvas(px: number, py: number): [number, number] {
      const cx = ((px - minX) / (maxX - minX + 0.001)) * (W - 2 * pad) + pad;
      const cy = H - (((py - minY) / (maxY - minY + 0.001)) * (H - 2 * pad) + pad);
      return [cx, cy];
    }

    let i = 0;
    const speed = 3; // frames per animation tick

    function draw() {
      if (!ctx) return;
      if (i >= points.length) { setDrawn(true); return; }
      const end = Math.min(i + speed, points.length - 1);
      for (let j = i; j < end; j++) {
        const [x1, y1] = toCanvas(points[j].x, points[j].y);
        const [x2, y2] = toCanvas(points[j + 1]?.x ?? points[j].x, points[j + 1]?.y ?? points[j].y);
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.globalAlpha = 0.8;
        ctx.stroke();

        // Mark direction-change events
        if (j > 0) {
          const a1 = points[j - 1].dir, a2 = points[j].dir;
          const diff = Math.abs(((a2 - a1 + 180) % 360) - 180);
          if (diff > 20 && points[j].s >= 1.0) {
            ctx.beginPath();
            ctx.arc(x1, y1, 5, 0, Math.PI * 2);
            ctx.fillStyle = '#FF0055';
            ctx.globalAlpha = 0.9;
            ctx.fill();
          }
        }
      }
      // Moving dot
      ctx.clearRect(0, 0, W, H); // slight flicker approach — just redraw full path each frame
      ctx.globalAlpha = 1;

      // redraw all path so far
      for (let j = 0; j < Math.min(end, points.length - 1); j++) {
        const [x1, y1] = toCanvas(points[j].x, points[j].y);
        const [x2, y2] = toCanvas(points[j + 1].x, points[j + 1].y);
        const t = j / points.length;
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.globalAlpha = 0.5 + t * 0.5;
        ctx.stroke();
      }

      // Highlight direction-change events
      for (let j = 1; j < Math.min(end, points.length); j++) {
        const a1 = points[j - 1].dir, a2 = points[j].dir;
        const diff = Math.abs(((a2 - a1 + 180) % 360) - 180);
        if (diff > 20 && points[j].s >= 1.0) {
          const [cx, cy] = toCanvas(points[j].x, points[j].y);
          ctx.beginPath();
          ctx.arc(cx, cy, 4, 0, Math.PI * 2);
          ctx.fillStyle = '#FF0055';
          ctx.globalAlpha = 0.85;
          ctx.fill();
        }
      }

      // Moving head
      const [hx, hy] = toCanvas(points[end].x, points[end].y);
      ctx.beginPath();
      ctx.arc(hx, hy, 6, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.globalAlpha = 1;
      ctx.fill();

      i = end;
      requestAnimationFrame(draw);
    }

    requestAnimationFrame(draw);
  }, [points, color, drawn]);

  return (
    <div className="glass" style={{ padding: '1.25rem', borderRadius: 12 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem', alignItems: 'center' }}>
        <span style={{ fontFamily: 'var(--font-display)', fontSize: '0.95rem' }}>{label}</span>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color }}>
          DCR: {dcr.toFixed(3)} events/s
        </span>
      </div>
      <canvas ref={canvasRef} width={340} height={200}
        style={{ width: '100%', height: 200, display: 'block', borderRadius: 8, background: 'rgba(0,0,0,0.25)', backgroundImage: 'linear-gradient(to right, rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.05) 1px, transparent 1px)', backgroundSize: '20px 20px', border: '1px solid rgba(255,255,255,0.05)' }} />
      <div style={{ marginTop: '0.75rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <div style={{ width: 24, height: 2, background: color }} />
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--muted)' }}>Path</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <div style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--red)' }} />
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--muted)' }}>Direction-change event (&gt;20°, speed ≥1 yd/s)</span>
        </div>
      </div>
    </div>
  );
}

export default function TrackingSection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });
  const traj = useTrajectories();

  return (
    <section className="section" id="tracking" ref={ref} >
      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <motion.p className="section-eyebrow" initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}}>
          Why 10 Hz Tracking
        </motion.p>
        <motion.h2 className="section-title" initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.1 }}>
          ONE STOPWATCH.<br />
          <span className="text-cyan">HUNDREDS OF OBSERVATIONS.</span>
        </motion.h2>
        <motion.p initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.2 }}
          style={{ color: 'rgba(245,245,247,0.6)', maxWidth: 560, marginBottom: '3rem', lineHeight: 1.7 }}>
          At 10 Hz, each second of the Short Shuttle drill produces 10 position, speed, and direction observations.
          Below are actual Short Shuttle tracking paths from two wide receiver prospects in our dataset.
          red circles mark frames where direction changed by more than 20° while moving at speed.
        </motion.p>

        {/* 10 Hz explainer */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ delay: 0.3 }}
          className="glass" style={{ padding: '1.5rem 2rem', marginBottom: '2rem', display: 'flex', flexWrap: 'wrap', gap: '2rem', alignItems: 'center' }}>
          <div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)', marginBottom: '0.5rem' }}>TRADITIONAL</div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--orange)' }}>1 NUMBER</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)' }}>Stopwatch result</div>
          </div>
          <div style={{ fontSize: '1.5rem', color: 'var(--muted)' }}>→</div>
          <div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)', marginBottom: '0.5rem' }}>10 Hz TRACKING</div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--cyan)' }}>~40+ FRAMES</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)' }}>x, y, speed, direction at each tick</div>
          </div>
          <div style={{ fontSize: '1.5rem', color: 'var(--muted)' }}>→</div>
          <div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)', marginBottom: '0.5rem' }}>FEATURES</div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--red)' }}>20+ METRICS</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--muted)' }}>Including direction_change_rate</div>
          </div>
        </motion.div>

        {/* Actual trajectory canvases */}
        {inView && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }}
            style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
            {traj ? (
              <>
                <TrajectoryCanvas points={traj.low_dcr.points} color="#00F0FF"
                  label="Lower direction-change rate" dcr={traj.low_dcr.dcr} />
                <TrajectoryCanvas points={traj.high_dcr.points} color="#FF0055"
                  label="Higher direction-change rate" dcr={traj.high_dcr.dcr} />
              </>
            ) : (
              <div className="glass" style={{ padding: '2rem', textAlign: 'center', gridColumn: '1/-1' }}>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--muted)' }}>
                  Loading trajectory data…
                </span>
              </div>
            )}
          </motion.div>
        )}

        <motion.p initial={{ opacity: 0 }} animate={inView ? { opacity: 1 } : {}} transition={{ delay: 0.8 }}
          style={{ marginTop: '1rem', fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'rgba(245,245,247,0.3)', fontStyle: 'italic' }}>
          * Trajectories are from actual competition tracking data (combine_tracking.csv). Red dots mark detected direction-change events.
        </motion.p>
      </div>
    </section>
  );
}
