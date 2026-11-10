import {
  FileText,
  Database,
  Activity,
  ArrowUpRight,
} from "lucide-react";

import "./Suggestions.css";

function Suggestions() {
  const suggestions = [
    {
      icon: FileText,
      title: "Explore documents",
      description: "Ask about your indexed knowledge",
    },
    {
      icon: Database,
      title: "Understand retrieval",
      description: "Explore how your RAG retrieves context",
    },
    {
      icon: Activity,
      title: "Check evaluation",
      description: "Review RAG performance and results",
    },
  ];

  return (
    <section className="suggestions">
      {suggestions.map((suggestion) => {
        const Icon = suggestion.icon;

        return (
          <button
            key={suggestion.title}
            className="suggestion-card"
          >
            <div className="suggestion-card-top">
              <Icon size={22} strokeWidth={1.8} />

              <ArrowUpRight
                size={20}
                strokeWidth={1.8}
              />
            </div>

            <div className="suggestion-card-content">
              <h3>{suggestion.title}</h3>

              <p>{suggestion.description}</p>
            </div>
          </button>
        );
      })}
    </section>
  );
}

export default Suggestions;