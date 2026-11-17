import { Send } from "lucide-react";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./ChatInput.css";

function ChatInput({ onSearch }) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSend = async () => {
    const query = message.trim();

    if (!query || loading) return;

    onSearch();

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: query,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    setMessage("");
    setLoading(true);
    setError("");

    try {
      const token = localStorage.getItem("access_token");

      const response = await fetch(
        "http://127.0.0.1:8000/api/rag/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            query,
            top_k: 5,
            strategy: "hybrid",
            rerank: true,
          }),
        }
      );

      const data = await response.json();

      console.log("RAG response:", data);

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to generate an answer."
        );
      }

      const assistantMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: data.answer,
        sources: data.sources || [],
      };

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ]);
    } catch (error) {
      console.error("RAG error:", error);
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
        messages.length > 0 ? "has-results" : ""
      }`}
    >

      {messages.length > 0 && (
        <div className="chat-messages">

          {messages.map((message) => (
            <div
              key={message.id}
              className={`chat-message ${message.role}`}
            >

              <div className="chat-message-label">
                {message.role === "user"
                  ? "YOU"
                  : "RAGLAB"}
              </div>

              <div className="chat-message-content">

                {message.role === "assistant" ? (
                  <>
                    <ReactMarkdown>
                      {message.content}
                    </ReactMarkdown>

                    {message.sources &&
                      message.sources.length > 0 && (
                        <div className="message-sources">

                          <div className="message-sources-header">
                            <span>RETRIEVED CONTEXT</span>
                            <span>
                              {message.sources.length} passages
                            </span>
                          </div>

                          {message.sources.map((source) => (
                            <div
                              key={source.chunk_id}
                              className="message-source"
                            >
                              <div className="message-source-top">
                                <span>
                                  Rank {source.rank}
                                </span>

                                <span>
                                  Score{" "}
                                  {source.score.toFixed(4)}
                                </span>
                              </div>

                              <div className="message-source-document">
                                {source.document}
                              </div>

                              <p>{source.text}</p>
                            </div>
                          ))}

                        </div>
                      )}

                  </>
                ) : (
                  <p>{message.content}</p>
                )}

              </div>

            </div>
          ))}

        </div>
      )}

      {loading && (
  <div className="thinking-loader">
    <div
      aria-label="Orange and tan hamster running in a metal wheel"
      role="img"
      className="wheel-and-hamster"
    >
      <div className="wheel"></div>

      <div className="hamster">
        <div className="hamster__body">
          <div className="hamster__head">
            <div className="hamster__ear"></div>
            <div className="hamster__eye"></div>
            <div className="hamster__nose"></div>
          </div>

          <div className="hamster__limb hamster__limb--fr"></div>
          <div className="hamster__limb hamster__limb--fl"></div>
          <div className="hamster__limb hamster__limb--br"></div>
          <div className="hamster__limb hamster__limb--bl"></div>
          <div className="hamster__tail"></div>
        </div>
      </div>

      <div className="spoke"></div>
    </div>

    <div className="thinking-text">
      RAGLab is thinking
    </div>
  </div>
)}

      {error && (
        <div className="retrieval-error">
          {error}
        </div>
      )}

      <div className="chat-input-wrapper">

        <textarea
          value={message}
          onChange={(event) =>
            setMessage(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Message RAGLab..."
          rows={1}
          disabled={loading}
        />

        <button
          className="chat-send-button"
          onClick={handleSend}
          disabled={loading || !message.trim()}
          aria-label="Send message"
        >
          <Send size={21} />
        </button>

      </div>

    </div>
  );
}

export default ChatInput;