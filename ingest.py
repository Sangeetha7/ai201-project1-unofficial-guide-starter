import os
import re

def load_raw_documents(data_dir):
    """Loads all text files from the specified directory."""
    documents = []
    if not os.path.exists(data_dir):
        print(f"Warning: Directory '{data_dir}' not found. Please create it and add your .txt files.")
        return documents
        
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                documents.append({
                    "source": filename,
                    "text": content
                })
    return documents

def clean_reddit_text(text):
    """Removes typical forum noise, markdown clutter, and formatting artifacts."""
    # 1. Remove URLs/links completely so they don't corrupt embeddings
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # 2. Clean up common HTML remnants if any crawled text snuck in
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&#39;', "'", text)
    
    # 3. Strip out explicit Reddit bot text or standard boilerplate lines
    text = re.sub(r'(?i)edit: thanks for the gold|tl;dr|bot action|moderator note.*', '', text)
    
    # 4. Strip out Reddit UI copy-paste artifacts
    text = re.sub(r'\d+:\d+\s*/\s*\d+:\d+', '', text) # Removes "0:00 / 0:00"
    text = re.sub(r'u/[\w-]+\s*avatar', '', text)       # Removes "u/username avatar"
    text = re.sub(r'•\n\d+[a-zA-Z]+\s*ago', '', text)   # Removes "•\n8mo ago"
    text = re.sub(r'^\d+$\n', '', text, flags=re.MULTILINE) # Removes standalone upvote numbers
    
    # 5. Collapse consecutive spaces and massive newlines into clean paragraphs
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()

def chunk_text(doc, chunk_size=500, overlap=100):
    """Splits text into chunks of specified character length with an overlap window."""
    text = doc["text"]
    source = doc["source"]
    chunks = []
    
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk_content = text[start:end]
        
        # Avoid saving tiny dangling remnants at the very end of a file
        if len(chunk_content.strip()) > 30:
            chunks.append({
                "text": chunk_content.strip(),
                "metadata": {"source": source, "start_char": start}
            })
            
        start += (chunk_size - overlap)
        
    return chunks

if __name__ == "__main__":
    RAW_DIR = "data/raw"
    
    print("--- Step 1: Loading Documents ---")
    raw_docs = load_raw_documents(RAW_DIR)
    print(f"Successfully loaded {len(raw_docs)} documents.")
    
    if not raw_docs:
        print("\nPlease create the directory 'data/raw' and drop your 10 text files there to proceed.")
        exit()

    print("\n--- Step 2: Cleaning and Normalizing Text ---")
    cleaned_docs = []
    for doc in raw_docs:
        cleaned_text = clean_reddit_text(doc["text"])
        cleaned_docs.append({"source": doc["source"], "text": cleaned_text})
    
    # Print a quick sample of document #1 to verify cleaning sanity
    print(f"\n[Verification] Cleaned sample from {cleaned_docs[0]['source']}:\n")
    print(cleaned_docs[0]['text'][:300] + "...\n")
    
    print("--- Step 3: Chunking (Size=500, Overlap=100) ---")
    all_chunks = []
    for doc in cleaned_docs:
        doc_chunks = chunk_text(doc, chunk_size=500, overlap=100)
        all_chunks.append(doc_chunks)
        
    # Flatten the list of lists
    flat_chunks = [c for sublist in all_chunks for c in sublist]
    print(f"Total chunks generated across all documents: {len(flat_chunks)}")
    
    print("\n--- Step 4: Inspecting 5 Representative Chunks ---")
    # Take a diverse slice of chunks to verify quality
    sample_indices = [0, len(flat_chunks)//4, len(flat_chunks)//2, (3*len(flat_chunks))//4, len(flat_chunks)-1]
    
    for idx in sample_indices:
        if idx < len(flat_chunks):
            chunk = flat_chunks[idx]
            print(f"\n[Chunk #{idx}] Source: {chunk['metadata']['source']}")
            print("-" * 50)
            print(chunk['text'])
            print("-" * 50)