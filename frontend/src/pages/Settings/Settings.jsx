import { useState } from "react";
import {
  Settings as SettingsIcon,
  Palette,
  Database,
  SlidersHorizontal,
  Link,
  ChevronDown,
} from "lucide-react";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import "./Settings.css";

function Settings() {
  const [retrievalStrategy, setRetrievalStrategy] =
    useState("baseline");

  const [topK, setTopK] = useState(5);

  const [chunkSize, setChunkSize] = useState(500);

  const [chunkOverlap, setChunkOverlap] = useState(50);

  return (
    <div className="settings-page">
      <Navbar />

      <main className="settings-container">
        <section className="settings-header">
          <div className="settings-header-icon">
            <SettingsIcon size={25} />
          </div>

          <div>
            <span className="settings-label">CONFIGURATION</span>
            <h1>Settings</h1>
            <p>
              Configure your RAGLab workspace and default RAG behavior.
            </p>
          </div>
        </section>

        <div className="settings-sections">

          {/* GENERAL */}

          <section className="settings-section">
            <div className="settings-section-heading">
              <Palette size={20} />
              <div>
                <h2>General</h2>
                <p>Basic workspace preferences.</p>
              </div>
            </div>

            <div className="settings-card">

              <div className="settings-row">
                <div>
                  <h3>Appearance</h3>
                  <p>Choose how RAGLab appears across your workspace.</p>
                </div>

                <select defaultValue="dark">
                  <option value="dark">Dark</option>
                  <option value="light">Light</option>
                  <option value="system">System</option>
                </select>
              </div>

              <div className="settings-divider" />

              <div className="settings-row">
                <div>
                  <h3>Default dataset</h3>
                  <p>
                    Dataset used when creating a new experiment.
                  </p>
                </div>

                <select defaultValue="none">
                  <option value="none">None selected</option>
                </select>
              </div>

            </div>
          </section>

          {/* RAG DEFAULTS */}

          <section className="settings-section">
            <div className="settings-section-heading">
              <SlidersHorizontal size={20} />
              <div>
                <h2>RAG Defaults</h2>
                <p>Default configuration for new RAG experiments.</p>
              </div>
            </div>

            <div className="settings-card">

              <div className="settings-row">
                <div>
                  <h3>Retrieval strategy</h3>
                  <p>
                    Default retrieval approach for new experiments.
                  </p>
                </div>

                <select
                  value={retrievalStrategy}
                  onChange={(event) =>
                    setRetrievalStrategy(event.target.value)
                  }
                >
                  <option value="baseline">
                    Baseline vector retrieval
                  </option>
                  <option value="semantic">
                    Semantic chunking
                  </option>
                  <option value="hybrid">
                    Hybrid retrieval
                  </option>
                  <option value="reranking">
                    Hybrid + reranking
                  </option>
                </select>
              </div>

              <div className="settings-divider" />

              <div className="settings-row">
                <div>
                  <h3>Top K</h3>
                  <p>Number of passages retrieved per query.</p>
                </div>

                <input
                  className="settings-number"
                  type="number"
                  min="1"
                  max="50"
                  value={topK}
                  onChange={(event) =>
                    setTopK(Number(event.target.value))
                  }
                />
              </div>

              <div className="settings-divider" />

              <div className="settings-row">
                <div>
                  <h3>Chunk size</h3>
                  <p>Default number of tokens per chunk.</p>
                </div>

                <input
                  className="settings-number"
                  type="number"
                  min="50"
                  max="5000"
                  value={chunkSize}
                  onChange={(event) =>
                    setChunkSize(Number(event.target.value))
                  }
                />
              </div>

              <div className="settings-divider" />

              <div className="settings-row">
                <div>
                  <h3>Chunk overlap</h3>
                  <p>Overlap between consecutive chunks.</p>
                </div>

                <input
                  className="settings-number"
                  type="number"
                  min="0"
                  max="1000"
                  value={chunkOverlap}
                  onChange={(event) =>
                    setChunkOverlap(Number(event.target.value))
                  }
                />
              </div>

            </div>
          </section>

          {/* INTEGRATIONS */}

          <section className="settings-section">
            <div className="settings-section-heading">
              <Link size={20} />
              <div>
                <h2>Integrations</h2>
                <p>Connect RAGLab with external systems.</p>
              </div>
            </div>

            <div className="settings-card integration-card">

              <div className="integration-icon">
                <Database size={24} />
              </div>

              <div className="integration-content">
                <div className="integration-title-row">
                  <h3>External RAG Integration</h3>
                  <span className="coming-soon">
                    Coming Soon
                  </span>
                </div>

                <p>
                  Connect an existing RAG system to RAGLab and
                  evaluate it using the same evaluation engine.
                </p>
              </div>

              <button className="integration-button" disabled>
                Coming Soon
              </button>

            </div>
          </section>

        </div>
      </main>

      <Footer />
    </div>
  );
}

export default Settings;