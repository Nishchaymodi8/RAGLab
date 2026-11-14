import { Settings } from "lucide-react";
import { Link } from "react-router-dom";
import HealthStatus from "../HealthStatus/HealthStatus";
import "./Navbar.css";

function Navbar() {
  return (
    <header className="navbar">
      <Link to="/" className="navbar-brand">
        <div className="navbar-logo">R</div>
        <span>RAGLab</span>
      </Link>

      <nav className="navbar-nav">
        <Link to="/chat" className="navbar-link active">
          Chat
        </Link>

        <Link to="/documents" className="navbar-link">
          Documents
        </Link>

        <Link to="/lab" className="navbar-link">
          Lab
        </Link>

        <Link to="/health" className="navbar-link">
          Health
        </Link>
      </nav>

      <div className="navbar-actions">
        <HealthStatus compact />
        <Link to="/settings" className="navbar-settings" title="Settings">
          <Settings size={22} />
        </Link>
      </div>
    </header>
  );
}

export default Navbar;
