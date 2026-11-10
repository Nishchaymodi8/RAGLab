import {
  Plus,
  Search,
  MessageSquare,
  MoreHorizontal,
} from "lucide-react";

import "./Sidebar.css";

function Sidebar() {
  return (
    <aside className="chat-sidebar">

      {/* New Chat */}
      <button className="new-chat-button">
        <Plus size={21} />
        <span>New Chat</span>
      </button>

      {/* Search */}
      <div className="chat-search">
        <Search size={19} />
        <input
          type="text"
          placeholder="Search chats"
        />
      </div>

      {/* Chat History */}
      <div className="chat-history">

        {/* Today */}
        <div className="chat-group">
          <h3>TODAY</h3>

          <div className="chat-item active">
            <MessageSquare size={19} />

            <span>Welcome to RAGLab</span>

            <MoreHorizontal
              size={18}
              className="chat-more"
            />
          </div>

          <div className="chat-item">
            <MessageSquare size={19} />
            <span>Testing document retrieval</span>
          </div>
        </div>

        {/* Yesterday */}
        <div className="chat-group">
          <h3>YESTERDAY</h3>

          <div className="chat-item">
            <MessageSquare size={19} />
            <span>Understanding embeddings</span>
          </div>

          <div className="chat-item">
            <MessageSquare size={19} />
            <span>RAG evaluation</span>
          </div>
        </div>

        {/* Older */}
        <div className="chat-group">
          <h3>OLDER</h3>

          <div className="chat-item">
            <MessageSquare size={19} />
            <span>Chunking strategies</span>
          </div>

          <div className="chat-item">
            <MessageSquare size={19} />
            <span>Retrieval experiments</span>
          </div>
        </div>

      </div>
    </aside>
  );
}

export default Sidebar;