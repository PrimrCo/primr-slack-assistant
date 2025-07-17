import os
import json
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
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

# 4. Generate embeddings for each chunk and store as JSON
vector_data = []
for i, chunk in enumerate(chunks):
    embedding = embedder.embed_query(chunk.page_content)
    vector_data.append({
        "id": i,
        "content": chunk.page_content,
        "metadata": chunk.metadata,
        "embedding": embedding
    })

# 5. Save vector data as JSON
with open("vector_store.json", "w", encoding="utf-8") as f:
    json.dump(vector_data, f, indent=2, ensure_ascii=False)

print("💾 Vector store saved to vector_store.json")

# Save index metadata
index_info = {
    "embedding_model": "text-embedding-ada-002",
    "chunk_count": len(chunks),
    "vector_dimension": len(vector_data[0]["embedding"]) if vector_data else 0,
    "index_created": True
}

with open("index_info.json", "w") as f:
    json.dump(index_info, f, indent=2)

print("📋 Index metadata saved to index_info.json")