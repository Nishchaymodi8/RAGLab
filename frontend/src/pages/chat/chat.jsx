import "./chat.css";
import Navbar from "../../components/Navbar/Navbar";
import Sidebar from "../../components/chat/sidebar/Sidebar";
import Greeting from "../../components/chat/Greeting/Greeting";
import ChatInput from "../../components/chat/ChatInput/ChatInput";
import Suggestions from "../../components/chat/Suggestions/Suggestions";
import Footer from "../../components/Footer/Footer";

function Chat() {
  return (
    <div className="chat-page">
      <Navbar />

      <main className="chat-layout">
  <Sidebar />
  
  <section className="chat-content">
    <Greeting />
    <Suggestions />
     <ChatInput />
     
  </section>
  
</main>

      <Footer />
    </div>
  );
}

export default Chat;