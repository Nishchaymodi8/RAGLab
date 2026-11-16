import { useState } from "react";
import "./chat.css";


import Navbar from "../../components/Navbar/Navbar";
import Sidebar from "../../components/chat/sidebar/Sidebar";
import Greeting from "../../components/chat/Greeting/Greeting";
import ChatInput from "../../components/chat/ChatInput/ChatInput";
import Suggestions from "../../components/chat/Suggestions/Suggestions";
import Footer from "../../components/Footer/Footer";
function Chat() {
  const [hasSearched, setHasSearched] = useState(false);

  return (
    <div className="chat-page">
      <Navbar />

      <main className="chat-layout">
        <Sidebar />

        <section className="chat-content">
          {!hasSearched ? (
            <>
              <Greeting />
              <Suggestions />
            </>
          ) : null}

          <ChatInput onSearch={() => setHasSearched(true)} />
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default Chat;