const API_BASE = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000').replace(/\/+$/, '') + '/api';

async function fetchAPI<T>(endpoint: string, timeoutMs = 30000): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, { signal: controller.signal });
    if (!res.ok) throw new Error(`API error: ${res.statusText}`);
    return res.json();
  } finally {
    clearTimeout(timer);
  }
}

export async function waitForBackend(maxRetries = 15, delayMs = 1000): Promise<boolean> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(5000) });
      if (res.ok) return true;
    } catch {}
    await new Promise(r => setTimeout(r, delayMs));
  }
  return false;
}

export interface SummaryStats {
  total_incidents: number;
  most_common_crime: string;
  highest_risk_location: string;
  avg_severity: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  trend_direction: string;
  monthly_change: number;
}

export interface TrendData {
  monthly_totals: { month: string; count: number }[];
  months: string[];
  crime_breakdown: { crime: string; data: number[] }[];
}

export interface CategoryData {
  name: string;
  value: number;
  percentage: number;
}

export interface HotspotCluster {
  cluster_id: number;
  centroid_lat: number;
  centroid_lng: number;
  point_count: number;
  avg_severity: number;
  risk_score: number;
  risk_level: string;
  dominant_crime: string;
  radius: number;
}

export interface RiskZone {
  location_name: string;
  latitude: number;
  longitude: number;
  incident_count: number;
  risk_score: number;
  risk_level: string;
  dominant_crime: string;
  recent_count: number;
  severity_breakdown: Record<string, number>;
}

export interface PredictionData {
  predicted_total_next_month: number;
  peak_hour: number;
  peak_day: string;
  growth_rate: number;
  overall_risk_trend: string;
  predicted_crime_probabilities: { crime: string; probability: number; current_count: number }[];
  high_risk_zones: {
    location_name: string;
    latitude: number;
    longitude: number;
    predicted_risk_score: number;
    current_risk_score: number;
    risk_level: string;
    confidence: number;
  }[];
  high_risk_time_windows: {
    window: string;
    incident_count: number;
    risk_score: number;
    risk_level: string;
  }[];
}

export interface Alert {
  id: number;
  type: string;
  title: string;
  message: string;
  severity: string;
  timestamp: string;
  read: boolean;
}

export interface Incident {
  id: number;
  crime_type: string;
  location_name: string;
  latitude: number;
  longitude: number;
  date_time: string;
  severity: string;
  description: string | null;
}

export interface CrimeStat {
  id: number;
  law_category: string;
  crime_section: string;
  reason: string;
  cases_jan_aug_2025: number;
  cases_aug_2024: number;
  cases_jul_2025: number;
  cases_aug_2025: number;
}

export interface CrimeStatSummary {
  law_category: string;
  crime_section: string;
  total_jan_aug_2025: number;
  total_aug_2025: number;
}

export interface CrimeStatCategory {
  name: string;
  total: number;
  percentage: number;
}

export const api = {
  getSummary: () => fetchAPI<SummaryStats>('/analytics/summary'),
  getTrends: () => fetchAPI<TrendData>('/analytics/trends'),
  getCategories: () => fetchAPI<CategoryData[]>('/analytics/categories'),
  getHotspots: () => fetchAPI<{ clusters: HotspotCluster[]; n_clusters: number }>('/analytics/hotspots'),
  getRiskZones: () => fetchAPI<RiskZone[]>('/analytics/risk-zones'),
  getPredictions: () => fetchAPI<PredictionData>('/predictions'),
  getAlerts: () => fetchAPI<Alert[]>('/alerts'),
  getIncidents: (skip = 0, limit = 5000, search = '', crime_type = '', severity = '', location = '') => {
    const params = new URLSearchParams({ skip: String(skip), limit: String(limit) });
    if (search) params.set('search', search);
    if (crime_type) params.set('crime_type', crime_type);
    if (severity) params.set('severity', severity);
    if (location) params.set('location', location);
    return fetchAPI<Incident[]>(`/incidents?${params}`);
  },
  createIncident: (data: any) =>
    fetch(`${API_BASE}/incidents`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
      signal: AbortSignal.timeout(15000),
    }).then(r => r.json()),
  getCrimeStats: () => fetchAPI<CrimeStat[]>('/crime-stats'),
  getCrimeStatsSummary: () => fetchAPI<CrimeStatSummary[]>('/crime-stats/summary'),
  getCrimeStatsCategories: () => fetchAPI<CrimeStatCategory[]>('/crime-stats/categories'),
  getLocations: () => fetchAPI<{ name: string; lat: number; lng: number; count: number }[]>('/locations'),
  geocode: (q: string) => fetchAPI<{ name: string; lat: number; lng: number; source: string }>(`/geocode?q=${encodeURIComponent(q)}`),
  geocodeSuggest: (q: string) => fetchAPI<{ name: string; full_name: string; lat: number; lng: number; type: string }[]>(`/geocode/search?q=${encodeURIComponent(q)}`),
  uploadFile: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData, signal: AbortSignal.timeout(60000) });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Upload failed');
    }
    return res.json();
  },
};
