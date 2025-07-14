import os
import pickle
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

load_dotenv()

#1. Load chunks
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# 2. Create embeddings
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")

# === FAISS ===
vector_store = FAISS.from_documents(chunks, embedder)
vector_store.save_local("faiss_index")
print("💾 FAISS index saved to ./faiss_index/")

# === Option B: Pinecone ===
# pinecone.init(api_key=os.getenv("PINECONE_API_KEY"),
#               environment=os.getenv("PINECONE_ENVIRONMENT"))
# index_name = "primr-docs"
# if index_name not in pinecone.list_indexes():
#     pinecone.create_index(index_name, dimension=1536)
# index = pinecone.Index(index_name)
# vector_store = Pinecone.from_documents(chunks, embedder, index)
# print(f"☁️ Pinecone index '{index_name}' ready")
