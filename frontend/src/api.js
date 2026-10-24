const API_BASE = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");

export async function getAccuracy() {
  const response = await fetch(`${API_BASE}/api/accuracy?start=2026-01-01&end=2026-01-31`);
  if (!response.ok) {
    let detail = `Request failed with HTTP ${response.status}`;
    try {
      const body = await response.json();
      if (body.detail) detail = body.detail;
    } catch {}
    throw new Error(detail);
  }
  return response.json();
}