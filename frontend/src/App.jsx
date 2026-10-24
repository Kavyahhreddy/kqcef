import { useEffect, useMemo, useState } from "react";
import { Activity, AlertTriangle, ArrowDownRight, ArrowUpRight, CalendarDays, CheckCircle2, CloudWind, ExternalLink, RefreshCw, Wind } from "lucide-react";
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis, Legend } from "recharts";
import { getAccuracy } from "./api.js";

const number = (value, digits = 1) => value == null ? "—" : Number(value).toLocaleString("en-GB", { maximumFractionDigits: digits });

function MetricCard({ title, value, unit, hint, icon: Icon }) {
  return <article className="metric-card">
    <div className="metric-top"><span>{title}</span><span className="metric-icon"><Icon size={18} /></span></div>
    <div className="metric-value">{value}<small>{unit}</small></div>
    <div className="metric-hint">{hint}</div>
  </article>;
}

export default function App() {
  const [payload, setPayload] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [refreshedAt, setRefreshedAt] = useState(null);

  async function load() {
    setLoading(true);
    setError("");
    try {
      const data = await getAccuracy();
      setPayload(data);
      setRefreshedAt(new Date());
    } catch (e) {
      setError(e?.message || "Could not load data.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  const rows = useMemo(() => (payload?.observations || []).map((row) => ({
    ...row,
    label: row.startTime ? new Date(row.startTime).toLocaleString("en-GB", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit", timeZone: "Europe/London" }) : "",
  })), [payload]);

  const metrics = payload?.metrics || {};
  const validCount = metrics.observations || 0;

  return <main className="app-shell">
    <header className="topbar">
      <a className="brand" href="#" aria-label="Wind Intelligence home"><span className="brand-mark"><Wind size={22} /></span><span>WIND<span className="brand-light">INTELLIGENCE</span></span></a>
      <div className="topbar-right"><span className="live-dot"></span><span>UK NATIONAL GRID · WIND</span><span className="period-pill">JAN 2026</span></div>
    </header>

    <section className="hero">
      <div className="hero-copy">
        <div className="eyebrow"><span className="eyebrow-line"></span> DAY-AHEAD MARKET ANALYTICS</div>
        <h1>Forecast the wind.<br /><em>Understand the gap.</em></h1>
        <p>Compare UK national wind generation forecasts with actual output and understand where prediction accuracy matters.</p>
        <div className="hero-meta"><span><CalendarDays size={15} /> 01 — 31 JANUARY 2026</span><span><Activity size={15} /> HALF-HOURLY OBSERVATIONS</span></div>
      </div>
      <div className="hero-graphic" aria-hidden="true"><div className="orbit orbit-one"></div><div className="orbit orbit-two"></div><div className="orbit orbit-three"></div><div className="hero-sun"></div><div className="wind-turbine turbine-a"><div className="turbine-blade blade-1"></div><div className="turbine-blade blade-2"></div><div className="turbine-blade blade-3"></div><div className="turbine-hub"></div><div className="turbine-stem"></div></div><div className="wind-turbine turbine-b"><div className="turbine-blade blade-1"></div><div className="turbine-blade blade-2"></div><div className="turbine-blade blade-3"></div><div className="turbine-hub"></div><div className="turbine-stem"></div></div><div className="wind-turbine turbine-c"><div className="turbine-blade blade-1"></div><div className="turbine-blade blade-2"></div><div className="turbine-blade blade-3"></div><div className="turbine-hub"></div><div className="turbine-stem"></div></div></div>
    </section>

    <section className="data-section">
      <div className="section-heading"><div><div className="section-kicker">01 / PERFORMANCE SNAPSHOT</div><h2>Forecast accuracy overview</h2><p>Metrics from forecast intervals matched to observed generation.</p></div><button className="refresh-button" onClick={load} disabled={loading}><RefreshCw size={15} className={loading ? "spin" : ""} /> {loading ? "Refreshing" : "Refresh data"}</button></div>

      {error && <div className="notice error-notice"><AlertTriangle size={19} /><div><strong>Live data could not be loaded</strong><p>{error}</p><span>Confirm Elexon stream parameter names and availability in the current API documentation.</span></div></div>}

      <div className="metric-grid">
        <MetricCard title="Mean absolute error" value={loading ? "…" : number(metrics.mae)} unit="MW" hint="Average absolute forecast gap" icon={Activity} />
        <MetricCard title="Root mean square error" value={loading ? "…" : number(metrics.rmse)} unit="MW" hint="Penalises larger misses" icon={ArrowUpRight} />
        <MetricCard title="Mean bias error" value={loading ? "…" : number(metrics.bias)} unit="MW" hint={metrics.bias > 0 ? "Forecasts high on average" : metrics.bias < 0 ? "Forecasts low on average" : "Signed forecast error"} icon={ArrowDownRight} />
        <MetricCard title="Mean absolute percentage error" value={loading ? "…" : number(metrics.mape)} unit="%" hint="Absolute error as a share of actual" icon={Activity} />
        <MetricCard title="Matched intervals" value={loading ? "…" : number(validCount, 0)} unit="" hint="Forecast and actual pairs" icon={CheckCircle2} />
      </div>

      <div className="chart-panel">
        <div className="chart-title-row"><div><div className="section-kicker">02 / GENERATION PROFILE</div><h3>Forecast vs actual generation</h3><p>Wind generation in MW · timestamps shown in UK local time</p></div><span className="chart-unit">MW</span></div>
        {loading ? <div className="empty-state"><div className="loader-ring"></div><p>Loading Elexon generation data…</p></div> : rows.length ? <div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><LineChart data={rows} margin={{ top: 16, right: 14, left: 0, bottom: 8 }}><CartesianGrid strokeDasharray="3 5" stroke="#263646" vertical={false} /><XAxis dataKey="label" tick={{ fill: "#899bac", fontSize: 11 }} tickLine={false} axisLine={{ stroke: "#314253" }} minTickGap={40} /><YAxis tick={{ fill: "#899bac", fontSize: 11 }} tickLine={false} axisLine={false} width={60} /><Tooltip contentStyle={{ background: "#101d2b", border: "1px solid #30465a", borderRadius: 10, color: "#eaf1f7" }} labelStyle={{ color: "#9eafc0" }} /><Legend /><Line type="monotone" dataKey="forecast" name="Forecast" stroke="#86a9ff" strokeWidth={2} dot={false} activeDot={{ r: 4 }} connectNulls /><Line type="monotone" dataKey="actual" name="Actual" stroke="#63dfba" strokeWidth={2} dot={false} activeDot={{ r: 4 }} connectNulls /></LineChart></ResponsiveContainer></div> : <div className="empty-state"><CloudWind size={28} /><p>No matched observations returned for January 2026.</p><span>Review the Elexon API response and the forecast publication cutoff.</span></div>}
      </div>

      <div className="bottom-grid">
        <article className="info-panel"><div className="section-kicker">03 / METHODOLOGY</div><h3>How the comparison works</h3><div className="method-step"><span>01</span><div><strong>Collect</strong><p>Retrieve national wind generation actuals and forecast records from the Elexon BMRS API.</p></div></div><div className="method-step"><span>02</span><div><strong>Match</strong><p>For each delivery interval, select the latest forecast published before the configured decision cutoff.</p></div></div><div className="method-step"><span>03</span><div><strong>Measure</strong><p>Join forecast and actual values by delivery start time, then calculate error metrics.</p></div></div></article>
        <article className="info-panel cutoff-panel"><div className="section-kicker">04 / ASSUMPTIONS</div><h3>Decision cutoff</h3><div className="cutoff-number">{number(payload?.cutoff_hours_before_delivery ?? 12, 0)}<small>h</small></div><p>Forecast publication cutoff before each delivery interval, configurable through the backend environment.</p><div className="assumption-note">This default is an analytical assumption for the challenge, not an official Elexon market deadline.</div><a href="https://bmrs.elexon.co.uk/api-documentation" target="_blank" rel="noreferrer">Elexon API documentation <ExternalLink size={13} /></a></article>
      </div>

      <footer className="footer"><span>WIND INTELLIGENCE <span className="footer-muted">/ DATA-LED ENERGY ANALYTICS</span></span><span>{refreshedAt ? "Last refreshed " + refreshedAt.toLocaleTimeString("en-GB") : "Ready to analyse"} · Source: Elexon BMRS</span></footer>
    </section>
  </main>;
}