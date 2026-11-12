import { useNavigate } from "react-router-dom";
import "./Chat.css";

import Navbar from "../../components/Navbar/Navbar";
import Sidebar from "../../components/Chat/Sidebar/Sidebar";
import Greeting from "../../components/Chat/Greeting/Greeting";
import ChatInput from "../../components/Chat/ChatInput/ChatInput";
import Suggestions from "../../components/Chat/Suggestions/Suggestions";
import Footer from "../../components/Footer/Footer";

import { logout } from "../../utils/auth";

function Chat() {
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="chat-page">
      <Navbar />

      <main className="chat-layout">
        <Sidebar />

        <section className="chat-content">
          <Greeting />
          <Suggestions />
          <ChatInput />

          <button onClick={handleLogout}>
            Logout
          </button>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default Chat;