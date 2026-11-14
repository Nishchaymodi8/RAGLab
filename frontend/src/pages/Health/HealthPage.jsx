import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Activity, ArrowLeft, CheckCircle, XCircle, RefreshCw } from "lucide-react";
import "./HealthPage.css";

export default function HealthPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [latency, setLatency] = useState(null);
  const [lastChecked, setLastChecked] = useState(null);

  const fetchHealth = async (isManual = false) => {
    if (isManual) setLoading(true);
    const start = performance.now();
    try {
      const response = await fetch("/api/health/");
      const elapsed = Math.round(performance.now() - start);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const json = await response.json();
      setData(json);
      setError(null);
      setLatency(elapsed);
      setLastChecked(new Date().toLocaleTimeString());
    } catch (err) {
      const elapsed = Math.round(performance.now() - start);
      setError(err.message || "Failed to reach /api/health/");
      setData(null);
      setLatency(elapsed);
      setLastChecked(new Date().toLocaleTimeString());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  return (
    <div className="health-page">
      <div className="health-card">
        <div className="health-card-header">
          <Link to="/" className="health-back-link">
            <ArrowLeft size={18} />
            <span>Back to App</span>
          </Link>
          <button
            className="health-card-refresh"
            onClick={() => fetchHealth(true)}
            disabled={loading}
          >
            <RefreshCw size={16} className={loading ? "spin" : ""} />
            <span>Re-check</span>
          </button>
        </div>

        <div className="health-title-section">
          <div className="health-title-icon">
            <Activity size={28} />
          </div>
          <div>
            <h1>RAGLab System Health</h1>
            <p className="health-subtitle">
              Phase 1 Full-Stack Connection Check (Django + PostgreSQL + React)
            </p>
          </div>
        </div>

        <div className="health-status-banner">
          {loading && (
            <div className="health-banner loading">
              <RefreshCw size={20} className="spin" />
              <span>Querying backend endpoint at <code>/api/health/</code>...</span>
            </div>
          )}

          {!loading && data && (
            <div className="health-banner success">
              <CheckCircle size={22} />
              <div>
                <strong>Backend Connected Successfully</strong>
                <p>Django is running and responding via the Vite proxy.</p>
              </div>
            </div>
          )}

          {!loading && error && (
            <div className="health-banner error">
              <XCircle size={22} />
              <div>
                <strong>Backend Connection Failed</strong>
                <p>{error}</p>
              </div>
            </div>
          )}
        </div>

        <div className="health-grid">
          <div className="health-stat">
            <span className="health-stat-label">Endpoint</span>
            <span className="health-stat-value"><code>/api/health/</code></span>
          </div>

          <div className="health-stat">
            <span className="health-stat-label">Reported Service</span>
            <span className="health-stat-value">
              {data?.service ? <code>{data.service}</code> : "—"}
            </span>
          </div>

          <div className="health-stat">
            <span className="health-stat-label">Latency</span>
            <span className="health-stat-value">
              {latency !== null ? `${latency} ms` : "—"}
            </span>
          </div>

          <div className="health-stat">
            <span className="health-stat-label">Last Checked</span>
            <span className="health-stat-value">{lastChecked || "—"}</span>
          </div>
        </div>

        {data && (
          <div className="health-raw-section">
            <h3>Raw API Response</h3>
            <pre className="health-raw-json">
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>
        )}

        <div className="health-footer-links">
          <Link to="/chat" className="health-btn primary">Go to Chat</Link>
          <Link to="/" className="health-btn secondary">Go to Login / Sign up</Link>
        </div>
      </div>
    </div>
  );
}
