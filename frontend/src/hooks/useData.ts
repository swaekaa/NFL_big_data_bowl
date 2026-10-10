import { useState, useEffect } from 'react';
import type { WRPlayer, TrajectoryData, BootstrapData, SummaryData, CorrelationRow } from '../types';

const BASE = (import.meta as any).env.BASE_URL + 'data/';

async function fetchJson<T>(path: string): Promise<T | null> {
  try {
    const res = await fetch(BASE + path);
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export function useWRData() {
  const [data, setData] = useState<WRPlayer[] | null>(null);
  useEffect(() => { fetchJson<WRPlayer[]>('wr_scatter.json').then(setData); }, []);
  return data;
}

export function useTrajectories() {
  const [data, setData] = useState<TrajectoryData | null>(null);
  useEffect(() => { fetchJson<TrajectoryData>('trajectories.json').then(setData); }, []);
  return data;
}

export function useBootstrap() {
  const [data, setData] = useState<BootstrapData | null>(null);
  useEffect(() => { fetchJson<BootstrapData>('bootstrap.json').then(setData); }, []);
  return data;
}

export function useSummary() {
  const [data, setData] = useState<SummaryData | null>(null);
  useEffect(() => { fetchJson<SummaryData>('summary.json').then(setData); }, []);
  return data;
}

export function useCorrelations() {
  const [data, setData] = useState<CorrelationRow[] | null>(null);
  useEffect(() => { fetchJson<CorrelationRow[]>('correlations.json').then(setData); }, []);
  return data;
}
