import { useEffect, useState } from "react";
import {
  Upload,
  FileText,
  RefreshCw,
  CheckCircle,
  Clock,
  AlertCircle,
  LoaderCircle,
} from "lucide-react";

import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";

import "./Documents.css";

function Documents() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const fetchDocuments = async () => {
    setLoading(true);
    setError("");

    const token = localStorage.getItem("access_token");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/documents/",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to load documents."
        );
      }

      setDocuments(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUpload = async (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    setUploading(true);
    setError("");

    const token = localStorage.getItem("access_token");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/documents/",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Document upload failed."
        );
      }

      setDocuments((previous) => [data, ...previous]);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

  const getStatusIcon = (status) => {
    if (status === "ready") {
      return <CheckCircle size={16} />;
    }

    if (status === "failed") {
      return <AlertCircle size={16} />;
    }

    if (status === "processing") {
      return <LoaderCircle size={16} className="spin" />;
    }

    return <Clock size={16} />;
  };

  const getStatusClass = (status) => {
    return `document-status status-${status}`;
  };

  return (
    <div className="documents-page">
      <Navbar />

      <main className="documents-container">

        <section className="documents-header">
          <div>
            <span className="documents-label">
              KNOWLEDGE BASE
            </span>

            <h1>Documents</h1>

            <p>
              Import and manage the documents used by your RAG system.
            </p>
          </div>

          <div className="documents-actions">
            <button
              className="documents-refresh-button"
              onClick={fetchDocuments}
              disabled={loading || uploading}
            >
              <RefreshCw size={18} />
              Refresh
            </button>

            <label className="documents-upload-button">
              {uploading ? (
                <>
                  <LoaderCircle size={19} className="spin" />
                  Uploading...
                </>
              ) : (
                <>
                  <Upload size={19} />
                  Import Documents
                </>
              )}

              <input
                type="file"
                accept=".txt,.md,.markdown"
                onChange={handleUpload}
                disabled={uploading}
                hidden
              />
            </label>
          </div>
        </section>

        {error && (
          <div className="documents-error">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <section className="documents-card">

          <div className="documents-table-header">
            <span>Document</span>
            <span>Type</span>
            <span>Status</span>
            <span>Chunks</span>
            <span>Version</span>
            <span>Added</span>
          </div>

          {loading ? (
            <div className="documents-empty">
              <LoaderCircle size={26} className="spin" />
              <p>Loading documents...</p>
            </div>
          ) : documents.length === 0 ? (
            <div className="documents-empty">
              <FileText size={32} />
              <h3>No documents yet</h3>
              <p>
                Import a TXT or Markdown document to start building
                your knowledge base.
              </p>
            </div>
          ) : (
            documents.map((document) => (
              <div
                className="document-row"
                key={document.id}
              >
                <div className="document-name">
                  <div className="document-icon">
                    <FileText size={19} />
                  </div>

                  <div>
                    <strong>{document.source_name}</strong>

                    <span>
                      {document.source_uri || "Local document"}
                    </span>
                  </div>
                </div>

                <div className="document-type">
                  {document.source_type.toUpperCase()}
                </div>

                <div>
                  <span
                    className={getStatusClass(document.status)}
                  >
                    {getStatusIcon(document.status)}
                    {document.status}
                  </span>
                </div>

                <div className="document-value">
                  {document.chunks}
                </div>

                <div className="document-value">
                  v{document.version}
                </div>

                <div className="document-date">
                  {new Date(
                    document.created_at
                  ).toLocaleDateString()}
                </div>
              </div>
            ))
          )}

        </section>
      </main>

      <Footer />
    </div>
  );
}

export default Documents;