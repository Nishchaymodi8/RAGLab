import { Send } from "lucide-react";
import { useState } from "react";

import "./ChatInput.css";

function ChatInput() {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (!message.trim()) return;

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
    <div className="chat-input-wrapper">
      <textarea
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Message RAGLab..."
        rows={1}
      />

      <button
        className="chat-send-button"
        onClick={handleSend}
        aria-label="Send message"
      >
        <Send size={21} />
      </button>
    </div>
  );
}

export default ChatInput;