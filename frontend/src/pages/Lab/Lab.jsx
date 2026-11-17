import "./Lab.css";
import Navbar from "../../components/Navbar/Navbar";
function Lab() {
  return (
    <div className="lab-container">
        <Navbar />
    <main className="lab-page">
      <div className="lab-header">
        <div>
          <p className="lab-eyebrow">RAG ENGINEERING LAB</p>
          <h1>Lab</h1>
          <p className="lab-description">
            Inspect retrieval, ranking, context selection, and answer generation.
          </p>
        </div>

        <div className="lab-status">
          <span className="status-dot"></span>
          Ready
        </div>
      </div>

      <section className="lab-dashboard">
  <div className="section-heading">
    <div>
      <div className="section-label">OVERVIEW</div>
      <h2>Run Overview</h2>
    </div>

    <span className="dashboard-status">
      No run selected
    </span>
  </div>

  <div className="dashboard-grid">

    <div className="dashboard-card">
      <span className="dashboard-card-label">
        LATEST RUN
      </span>

      <div className="dashboard-value">
        —
      </div>

      <p>No evaluation run yet</p>
    </div>

    <div className="dashboard-card">
      <span className="dashboard-card-label">
        DOCUMENTS
      </span>

      <div className="dashboard-value">
        —
      </div>

      <p>Indexed documents</p>
    </div>

    <div className="dashboard-card">
      <span className="dashboard-card-label">
        CHUNKS
      </span>

      <div className="dashboard-value">
        —
      </div>

      <p>Available chunks</p>
    </div>

    <div className="dashboard-card">
      <span className="dashboard-card-label">
        RETRIEVAL LATENCY
      </span>

      <div className="dashboard-value">
        —
      </div>

      <p>Latest retrieval</p>
    </div>

    <div className="dashboard-card dashboard-card-highlight">
      <span className="dashboard-card-label">
        BEST METHOD
      </span>

      <div className="dashboard-value">
        —
      </div>

      <p>Based on evaluation results</p>
    </div>

  </div>
</section>

      <section className="lab-query-section">
        <div className="section-label">QUERY</div>

        <div className="lab-query-box">
          <span>
            Run a query from Chat to inspect the RAG pipeline here.
          </span>
        </div>
      </section>

      <section className="lab-section">
        <div className="section-heading">
          <div>
            <div className="section-label">PIPELINE</div>
            <h2>Retrieval Pipeline</h2>
          </div>

          <span className="pipeline-status">Waiting for run</span>
        </div>

        <div className="pipeline">
          <div className="pipeline-node">
            <span className="node-number">01</span>
            <h3>Semantic</h3>
            <p>Vector similarity</p>
          </div>

          <div className="pipeline-connector"></div>

          <div className="pipeline-node">
            <span className="node-number">02</span>
            <h3>BM25</h3>
            <p>Lexical matching</p>
          </div>

          <div className="pipeline-connector"></div>

          <div className="pipeline-node">
            <span className="node-number">03</span>
            <h3>Hybrid</h3>
            <p>RRF fusion</p>
          </div>

          <div className="pipeline-connector"></div>

          <div className="pipeline-node">
            <span className="node-number">04</span>
            <h3>Reranker</h3>
            <p>Relevance scoring</p>
          </div>

          <div className="pipeline-connector"></div>

          <div className="pipeline-node pipeline-node-final">
            <span className="node-number">05</span>
            <h3>Context</h3>
            <p>Selected passages</p>
          </div>
        </div>
      </section>

      <section className="lab-section">
        <div className="section-heading">
          <div>
            <div className="section-label">RESULTS</div>
            <h2>Retrieval Comparison</h2>
          </div>
        </div>

        <div className="comparison-grid">
          <div className="result-panel">
            <div className="result-panel-header">
              <div>
                <span className="method-label">SEMANTIC</span>
                <h3>Semantic Retrieval</h3>
              </div>
              <span className="result-count">—</span>
            </div>

            <div className="empty-result">
              No retrieval run yet.
            </div>
          </div>

          <div className="result-panel">
            <div className="result-panel-header">
              <div>
                <span className="method-label">LEXICAL</span>
                <h3>BM25 Retrieval</h3>
              </div>
              <span className="result-count">—</span>
            </div>

            <div className="empty-result">
              No retrieval run yet.
            </div>
          </div>

          <div className="result-panel">
            <div className="result-panel-header">
              <div>
                <span className="method-label">FUSION</span>
                <h3>Hybrid Retrieval</h3>
              </div>
              <span className="result-count">—</span>
            </div>

            <div className="empty-result">
              No retrieval run yet.
            </div>
          </div>

          <div className="result-panel">
            <div className="result-panel-header">
              <div>
                <span className="method-label">RANKING</span>
                <h3>Reranker</h3>
              </div>
              <span className="result-count">—</span>
            </div>

            <div className="empty-result">
              No reranking run yet.
            </div>
          </div>
        </div>
      </section>

      <section className="lab-section">
        <div className="section-heading">
          <div>
            <div className="section-label">CONTEXT</div>
            <h2>Selected Context</h2>
          </div>

          <span className="context-count">0 passages</span>
        </div>

        <div className="context-empty">
          <div className="context-icon">+</div>

          <h3>No context selected</h3>

          <p>
            Run a query from Chat to inspect which passages are selected
            for answer generation.
          </p>
        </div>
      </section>
    </main>
    </div>
  );
}

export default Lab;