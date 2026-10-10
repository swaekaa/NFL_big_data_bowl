import { useRef, useState, useEffect, useCallback } from 'react';
import HeroSection from './components/Hero';
import DynamicGradientBackground from './components/DynamicGradientBackground';
import ProblemSection from './components/ProblemSection';
import DataSection from './components/DataSection';
import TrackingSection from './components/TrackingSection';
import MetricSection from './components/MetricSection';
import SpeedVsMetricSection from './components/SpeedVsMetricSection';
import DiscoverySection from './components/DiscoverySection';
import MultipleTestingSection from './components/MultipleTestingSection';
import BootstrapSection from './components/BootstrapSection';
import RidgeSection from './components/RidgeSection';
import SameStopwatchSection from './components/SameStopwatchSection';
import LimitationsSection from './components/LimitationsSection';
import FinalSection from './components/FinalSection';

const SECTIONS = [
  { id: 'hero', label: 'Intro' },
  { id: 'problem', label: 'Problem' },
  { id: 'data', label: 'Data' },
  { id: 'tracking', label: 'Tracking' },
  { id: 'metric', label: 'Metric' },
  { id: 'speed-comparison', label: 'Speed vs Metric' },
  { id: 'discovery', label: 'Discovery' },
  { id: 'multiple-testing', label: 'Multiple Testing' },
  { id: 'bootstrap', label: 'Bootstrap' },
  { id: 'ridge', label: 'Model Comparison' },
  { id: 'same-stopwatch', label: 'Same Stopwatch' },
  { id: 'limitations', label: 'Limitations' },
  { id: 'conclusion', label: 'Conclusion' },
];

function useActiveSection() {
  const [active, setActive] = useState('hero');

  useEffect(() => {
    const observers: IntersectionObserver[] = [];
    SECTIONS.forEach(({ id }) => {
      const el = document.getElementById(id);
      if (!el) return;
      const obs = new IntersectionObserver(
        ([entry]) => { if (entry.isIntersecting) setActive(id); },
        { threshold: 0.35 }
      );
      obs.observe(el);
      observers.push(obs);
    });
    return () => observers.forEach(o => o.disconnect());
  }, []);

  return active;
}

export default function App() {
  const heroRef = useRef<HTMLElement | null>(null);
  const active = useActiveSection();

  // get the hero section element for scrollToNext
  useEffect(() => {
    heroRef.current = document.getElementById('problem');
  }, []);

  const scrollToNext = useCallback(() => {
    document.getElementById('problem')?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  const scrollTo = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <>
      <DynamicGradientBackground />
      {/* Navigation */}
      <nav>
        <div className="nav-logo">
          NFL BIG DATA BOWL
        </div>
        <ul className="nav-links">
          {['problem', 'data', 'metric', 'discovery', 'conclusion'].map(id => (
            <li key={id}>
              <a href={`#${id}`} style={{ color: active === id ? 'var(--white)' : undefined }}
                onClick={e => { e.preventDefault(); scrollTo(id); }}>
                {SECTIONS.find(s => s.id === id)?.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>

      {/* Progress dots */}
      <div className="progress-dots" role="navigation" aria-label="Section progress">
        {SECTIONS.map(s => (
          <button key={s.id}
            className={`progress-dot${active === s.id ? ' active' : ''}`}
            title={s.label}
            aria-label={`Go to ${s.label}`}
            onClick={() => scrollTo(s.id)}
            style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}>
            <div className={`progress-dot${active === s.id ? ' active' : ''}`} style={{ pointerEvents: 'none' }} />
          </button>
        ))}
      </div>

      {/* Sections */}
      <main>
        <HeroSection scrollToNext={scrollToNext} />
        <ProblemSection />
        <DataSection />
        <TrackingSection />
        <MetricSection />
        <SpeedVsMetricSection />
        <DiscoverySection />
        <MultipleTestingSection />
        <BootstrapSection />
        <RidgeSection />
        <SameStopwatchSection />
        <LimitationsSection />
        <FinalSection />
      </main>
    </>
  );
}
