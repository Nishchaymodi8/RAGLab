import { useEffect, useState, useCallback } from "react";
import { Activity, RefreshCw } from "lucide-react";
import "./HealthStatus.css";

export default function HealthStatus({ compact = false }) {
  const [state, setState] = useState({
    status: "loading", // "loading" | "ok" | "error"
    data: null,
    error: null,
    latency: null,
  });
  const [isRefreshing, setIsRefreshing] = useState(false);

  const checkHealth = useCallback(async (isManualRefresh = false) => {
    if (isManualRefresh) {
      setIsRefreshing(true);
    }
    const startTime = performance.now();
    try {
      const response = await fetch("/api/health/");
      const elapsed = Math.round(performance.now() - startTime);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      setState({
        status: "ok",
        data,
        error: null,
        latency: elapsed,
      });
    } catch (err) {
      const elapsed = Math.round(performance.now() - startTime);
      setState({
        status: "error",
        data: null,
        error: err.message || "Failed to connect to backend",
        latency: elapsed,
      });
    } finally {
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    checkHealth();
  }, [checkHealth]);

  if (compact) {
    return (
      <div
        className={`health-pill health-pill--${state.status}`}
        title={
          state.status === "ok"
            ? `Connected to ${state.data?.service} (${state.latency}ms)`
            : state.status === "error"
            ? `API Error: ${state.error}`
            : "Checking connection..."
        }
        onClick={() => checkHealth(true)}
        role="button"
        tabIndex={0}
      >
        <span className="health-dot" />
        <span className="health-label">
          {state.status === "ok"
            ? `API: ${state.data?.status} (${state.latency}ms)`
            : state.status === "error"
            ? "API: Offline"
            : "API: Checking..."}
        </span>
        <RefreshCw
          size={12}
          className={`health-refresh ${isRefreshing ? "spin" : ""}`}
        />
      </div>
    );
  }

  return (
    <div className={`health-badge health-badge--${state.status}`}>
      <div className="health-badge-header">
        <div className="health-badge-indicator">
          <span className="health-dot" />
          <Activity size={16} />
          <strong>Backend API</strong>
        </div>
        <button
          className="health-refresh-btn"
          onClick={() => checkHealth(true)}
          disabled={isRefreshing}
          title="Refresh health check"
          aria-label="Refresh health check"
        >
          <RefreshCw
            size={14}
            className={isRefreshing ? "spin" : ""}
          />
        </button>
      </div>

      <div className="health-badge-body">
        {state.status === "loading" && (
          <p className="health-message">Connecting to /api/health/...</p>
        )}
        {state.status === "ok" && (
          <div className="health-details">
            <span className="health-success">
              Status: <strong>{state.data?.status}</strong>
            </span>
            <span className="health-service">
              Service: <code>{state.data?.service}</code>
            </span>
            {state.latency !== null && (
              <span className="health-latency">
                Latency: {state.latency}ms
              </span>
            )}
          </div>
        )}
        {state.status === "error" && (
          <div className="health-details">
            <span className="health-error-text">Disconnected</span>
            <span className="health-error-hint">{state.error}</span>
          </div>
        )}
      </div>
    </div>
  );
}
