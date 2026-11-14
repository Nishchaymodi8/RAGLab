import { Send } from "lucide-react";
import { useState } from "react";
import "./ChatInput.css";

function ChatInput({ onSearch }) {
  const [message, setMessage] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSend = async () => {
    const query = message.trim();

    if (!query || loading) return;
    onSearch();

    console.log("Sending query:", query);

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const token = localStorage.getItem("access_token");

      const response = await fetch(
        "http://127.0.0.1:8000/api/retrieval/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            query,
            top_k: 5,
          }),
        }
      );

      const data = await response.json();

      console.log("Retrieval response:", data);

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to retrieve relevant documents."
        );
      }

      setResults(data.results);
      setMessage("");
    } catch (error) {
      console.error("Retrieval error:", error);
      setError(error.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <div
      className={`chat-input-area ${
        results.length > 0 ? "has-results" : ""
      }`}
    >
      <div className="chat-input-wrapper">
        <textarea
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message RAGLab..."
          rows={1}
          disabled={loading}
        />

        <button
          className="chat-send-button"
          onClick={handleSend}
          disabled={loading}
          aria-label="Send message"
        >
          <Send size={21} />
        </button>
      </div>

      {loading && (
        <div className="retrieval-status">
          Searching your documents...
        </div>
      )}

      {error && (
        <div className="retrieval-error">
          {error}
        </div>
      )}

      {results.length > 0 && (
        <div className="retrieval-results">
          <div className="retrieval-results-header">
            <span>RETRIEVED CONTEXT</span>
            <span>{results.length} passages</span>
          </div>

          {results.map((result) => (
            <div
              key={result.chunk_id}
              className="retrieval-result"
            >
              <div className="retrieval-result-top">
                <span>Rank {result.rank}</span>
                <span>
                  Score {result.score.toFixed(4)}
                </span>
              </div>

              <div className="retrieval-result-document">
                {result.document}
              </div>

              <p>{result.text}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ChatInput;