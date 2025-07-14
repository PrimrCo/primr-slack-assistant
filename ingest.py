import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import glob
import pickle

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

# 3. Save chunks for reuse
with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print(f"🔖 {len(chunks)} chunks saved to chunks.pkl")
