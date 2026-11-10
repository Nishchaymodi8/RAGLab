import "./Greeting.css";

function Greeting() {
  return (
    <section className="chat-greeting">
      <span className="greeting-label">RAG SYSTEM</span>

      <h1>How can I help you?</h1>

      <p>
        Ask questions about your documents, retrieval pipeline and evaluation
        results.
      </p>
    </section>
  );
}

export default Greeting;