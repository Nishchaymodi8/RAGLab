import { useState } from "react";
import {
  Plus,
  Settings,
  Send,
  MessageSquare,
  Search,
  MoreHorizontal,
} from "lucide-react";
import { Link } from "react-router-dom";
import "./Chat.css";

function Chat() {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (!message.trim()) return;

    // Backend integration will be added later.
    console.log("Message:", message);

    setMessage("");
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-page">
      {/* Navbar */}
      <nav className="chat-navbar">

  {/* Logo */}
  <div className="raglab-logo glass">
    <div className="raglab-logo-mark">
      R
    </div>

    <span>RAGLab</span>
  </div>

  {/* Navigation */}
  <div className="main-navigation glass">

    <Link to="/" className="nav-item active">
      Chat
    </Link>

    <Link to="/documents" className="nav-item">
      Documents
    </Link>

    <Link to="/lab" className="nav-item">
      Lab
    </Link>

  </div>

  {/* Settings */}
  <Link
    to="/settings"
    className="settings-button glass"
  >
    <Settings size={19} strokeWidth={1.8} />
  </Link>

</nav>

      {/* Main Chat Layout */}
      <main className="chat-layout">
        {/* Chat History */}
        <aside className="chat-sidebar glass">
          <button className="new-chat-button">
            <Plus size={18} />
            <span>New Chat</span>
          </button>

          <div className="chat-search">
            <Search size={16} />
            <input
              type="text"
              placeholder="Search chats"
            />
          </div>

          <div className="chat-history">
            <div className="history-section">
              <span className="history-title">Today</span>

              <button className="history-item active-chat">
                <MessageSquare size={16} />
                <span>Welcome to RAGLab</span>
                <MoreHorizontal size={16} />
              </button>

              <button className="history-item">
                <MessageSquare size={16} />
                <span>Testing document retrieval</span>
              </button>
            </div>

            <div className="history-section">
              <span className="history-title">Yesterday</span>

              <button className="history-item">
                <MessageSquare size={16} />
                <span>Understanding embeddings</span>
              </button>

              <button className="history-item">
                <MessageSquare size={16} />
                <span>RAG evaluation</span>
              </button>
            </div>

            <div className="history-section">
              <span className="history-title">Older</span>

              <button className="history-item">
                <MessageSquare size={16} />
                <span>Chunking strategies</span>
              </button>
            </div>
          </div>
        </aside>

        {/* Conversation */}
        <section className="conversation">
          {/* Welcome State */}
          <div className="welcome-container">
            <div className="welcome-icon glass">
              <span>R</span>
            </div>

            <h1>How can I help you?</h1>

            <p>
              Ask questions about your documents and explore
              your RAG system.
            </p>

            <div className="suggestion-grid">
              <button
                className="suggestion-card glass"
                onClick={() =>
                  setMessage("What documents are available?")
                }
              >
                <span>Explore documents</span>
                <small>
                  Ask about your indexed knowledge
                </small>
              </button>

              <button
                className="suggestion-card glass"
                onClick={() =>
                  setMessage("How does retrieval work?")
                }
              >
                <span>Understand retrieval</span>
                <small>
                  Explore how your RAG retrieves context
                </small>
              </button>

              <button
                className="suggestion-card glass"
                onClick={() =>
                  setMessage("Show me my latest evaluation")
                }
              >
                <span>Check evaluation</span>
                <small>
                  Review RAG performance and results
                </small>
              </button>
            </div>
          </div>

          {/* Input */}
          <div className="input-area">
            <div className="message-input glass">
              <textarea
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Message RAGLab..."
                rows={1}
              />

              <button
                className="send-button"
                onClick={handleSend}
                disabled={!message.trim()}
              >
                <Send size={18} />
              </button>
            </div>

            <p className="input-disclaimer">
              RAGLab uses your configured retrieval pipeline to
              generate answers.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}

export default Chat;