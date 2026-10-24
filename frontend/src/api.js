// In production the UI and API share one origin, so use relative URLs.
// Vite development keeps the local FastAPI server on port 8000.
const API_BASE = (
  import.meta.env.VITE_API_BASE_URL ??
  (import.meta.env.DEV ? "http://localhost:8000" : "")
).replace(/\/$/, "");

async function request(path) {
  const response = await fetch(`${API_BASE}${path}`);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.detail || `Request failed (HTTP ${response.status})`);
  }
  return body;
}

export function getAccuracy(start = "2026-01-01", end = "2026-01-31") {
  return request(`/api/accuracy?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`);
}

export function getObservations(date) {
  return request(`/api/observations?date=${encodeURIComponent(date)}`);
}
