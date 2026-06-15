import os
import gradio as gr
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Initialize Groq Client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize Embedding Model and Vector DB
print("Loading embedding model...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Connecting to ChromaDB...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="internship_guide")

def ask_rag(question):
    """Retrieves context from ChromaDB and passes it to Groq LLM for a grounded answer."""
    
    # 1. Embed the query and retrieve top 4 chunks
    query_embedding = embed_model.encode([question]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=4
    )
    
    # Safely extract documents and metadata
    documents = results.get('documents', [[]])[0]
    metadatas = results.get('metadatas', [[]])[0]
    
    # 2. Extract unique sources for attribution
    unique_sources = set()
    for meta in metadatas:
        if meta and 'source' in meta:
            unique_sources.add(meta['source'])
            
    # 3. Format the retrieved chunks into a single context block
    context_text = "\n\n---\n\n".join(documents)
    
    # 4. Construct the Strict System Prompt for Grounding
    system_prompt = (
        "You are a helpful academic and career advisor for university students. "
        "You must answer the user's question using ONLY the context provided below. "
        "If the answer is not explicitly stated in the context, you must reply: "
        "'I don't have enough information on that based on the provided documents.' "
        "Do not use outside knowledge or hallucinate information. "
        "Context:\n"
        f"{context_text}"
    )

    # 5. Call the Groq LLM
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.0 # Strict deterministic output to prevent hallucination
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Error connecting to LLM: {str(e)}"
        unique_sources = {"N/A"}

    return {"answer": answer, "sources": list(unique_sources)}

# --- Gradio UI Setup ---
def handle_query(question):
    """Wrapper function to map the RAG output to Gradio UI elements."""
    result = ask_rag(question)
    # Format sources as bullet points
    sources_formatted = "\n".join(f"• {s}" for s in result["sources"]) if result["sources"] else "No sources retrieved."
    return result["answer"], sources_formatted

# Build the Web Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 The Unofficial Guide: Tech Internships")
    gr.Markdown("Ask questions about SWE and Cybersecurity internship timelines, interviews, and experiences.")
    
    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(label="Your Question", placeholder="e.g., What technical questions are asked at Google?")
            btn = gr.Button("Search the Guide", variant="primary")
            
        with gr.Column():
            answer_box = gr.Textbox(label="Answer", lines=8, interactive=False)
            sources_box = gr.Textbox(label="Retrieved From", lines=3, interactive=False)
            
    # Trigger the function on button click or hitting 'Enter'
    btn.click(handle_query, inputs=inp, outputs=[answer_box, sources_box])
    inp.submit(handle_query, inputs=inp, outputs=[answer_box, sources_box])

if __name__ == "__main__":
    print("Launching Gradio UI...")
    demo.launch()