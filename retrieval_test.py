import os
import chromadb
from sentence_transformers import SentenceTransformer

# Import our working ingestion pipeline from Milestone 3
from ingest import load_raw_documents, clean_reddit_text, chunk_text

# Define parameters cleanly in one place
CHUNK_SIZE = 700
OVERLAP = 150

print("Loading embedding model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Initializing ChromaDB...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "internship_guide"

collection = chroma_client.get_or_create_collection(name=collection_name)

def build_vector_store():
    """Runs the ingestion pipeline and stores embeddings in ChromaDB."""
    RAW_DIR = "data/raw"
    
    if collection.count() > 0:
        print(f"Vector store already populated with {collection.count()} chunks. Skipping ingestion.")
        return

    print("Building vector store from scratch...")
    raw_docs = load_raw_documents(RAW_DIR)
    
    all_chunks = []
    for doc in raw_docs:
        cleaned_text = clean_reddit_text(doc["text"])
        # Pass the parameters dynamically here
        doc_chunks = chunk_text(
            {"source": doc["source"], "text": cleaned_text}, 
            chunk_size=CHUNK_SIZE, 
            overlap=OVERLAP
        )
        all_chunks.extend(doc_chunks)

    texts = []
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(all_chunks):
        texts.append(chunk["text"])
        # Fallback to an empty dict if metadata is somehow missing
        metadatas.append(chunk.get("metadata", {"source": "unknown"}))
        ids.append(f"chunk_{i}")

    print(f"Embedding {len(texts)} chunks and adding to ChromaDB...")
    embeddings = model.encode(texts).tolist()
    
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    print("Successfully populated ChromaDB!")

def test_retrieval(query, top_k=4):
    """Embeds a user query, searches ChromaDB, and prints the top results safely."""
    print(f"\n{'='*60}")
    print(f"QUERY: {query}")
    print(f"{'='*60}")
    
    query_embedding = model.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    
    # Extract results safely
    documents = results.get('documents', [[]])[0]
    distances = results.get('distances', [[]])[0]
    metadatas = results.get('metadatas', [[]])[0]
    
    for i in range(len(documents)):
        # Safely extract source name with a fallback string
        metadata_entry = metadatas[i] if (metadatas and i < len(metadatas)) else {}
        source_name = metadata_entry.get('source', 'unknown') if metadata_entry else 'unknown'
        dist_score = distances[i] if (distances and i < len(distances)) else 0.0
        
        print(f"\n[Result {i+1}] Distance Score: {dist_score:.4f} | Source: {source_name}")
        print("-" * 60)
        print(documents[i])

if __name__ == "__main__":
    build_vector_store()
    
    test_retrieval("What is the reported application timeline for the Amazon SDE Intern position for Summer 2026?")
    test_retrieval("What specific technical topics or coding questions were asked during the Google SWE Intern interview?")
    test_retrieval("What are the core technical concepts a candidate must study for a SOC Analyst Tier 1 interview?")