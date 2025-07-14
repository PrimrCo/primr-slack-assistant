import os
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import glob

load_dotenv()

# 1. Load all .md files
paths = glob.glob("data/*.md")
all_docs = []
for path in paths:
    loader = TextLoader(path, encoding="utf-8")
    docs = loader.load()
    all_docs.extend(docs)

# 2. Chunk them
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(all_docs)

# 3. Convert chunks to JSON-serializable format
chunks_data = []
for chunk in chunks:
    chunk_data = {
        "page_content": chunk.page_content,
        "metadata": chunk.metadata
    }
    chunks_data.append(chunk_data)

# 4. Save as JSON instead of pickle
with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks_data, f, indent=2, ensure_ascii=False)

print(f"🔖 {len(chunks_data)} chunks saved to chunks.json")
