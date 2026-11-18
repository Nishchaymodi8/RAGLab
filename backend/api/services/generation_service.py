import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3.5:4b"


def generate_answer(query, retrieved_chunks):
    context_parts = []

    for index, item in enumerate(retrieved_chunks, start=1):
        chunk = item["chunk"]

        context_parts.append(
            f"""[Context {index}]
Document: {chunk.document_version.document.source_name}

{chunk.text}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""You are a helpful RAG assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided documents."

Do not invent information.
Do not use outside knowledge.
Keep the answer clear and concise.

Context:
{context}

User question:
{query}

Answer:
"""
    print("PROMPT LENGTH:", len(prompt))
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 300,
            },
        },
        
        timeout=600,
    )

    response.raise_for_status()

    data = response.json()
    print("OLLAMA RESPONSE:", data)
    print("OLLAMA STATUS:", response.status_code)
    print("OLLAMA RESPONSE:", repr(data.get("response")))
    print("OLLAMA THINKING:", repr(data.get("thinking")))
    print("OLLAMA DONE REASON:", data.get("done_reason"))


    return data["response"].strip()