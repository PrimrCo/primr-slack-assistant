import os
import json
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

load_dotenv()

# 1. Load chunks from JSON
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# 2. Convert back to Document objects
chunks = []
for chunk_data in chunks_data:
    doc = Document(
        page_content=chunk_data["page_content"],
        metadata=chunk_data["metadata"]
    )
    chunks.append(doc)

# 3. Create embeddings
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")

# 4. Create FAISS index
vector_store = FAISS.from_documents(chunks, embedder)

# 5. Save FAISS index securely (without pickle for documents)
vector_store.save_local("faiss_index")
print("💾 FAISS index saved to ./faiss_index/")

# Optional: Save just the embeddings and metadata separately as JSON backup
index_info = {
    "embedding_model": "text-embedding-ada-002",
    "chunk_count": len(chunks),
    "index_created": True
}

with open("index_info.json", "w") as f:
    json.dump(index_info, f, indent=2)

print("📋 Index metadata saved to index_info.json")
