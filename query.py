import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Load FAISS index (we trust our own generated files)
# TODO: Security - Replace FAISS with pickle-free vector store (e.g., Chroma, Weaviate)
# Current risk: Low (we control file creation), but should eliminate pickle entirely
vs = FAISS.load_local(
    "faiss_index",
    OpenAIEmbeddings(model="text-embedding-ada-002"),
    allow_dangerous_deserialization=True  # FIXME: Remove pickle dependency
)

retriever = vs.as_retriever(search_kwargs={"k": 5})

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4", temperature=0),
    chain_type="stuff",
    retriever=retriever,
)

while True:
    query = input("🔍 Ask Primr: ")
    if not query.strip():
        break

    # Use invoke instead of deprecated run method
    result = qa.invoke({"query": query})
    print("\n💡", result["result"])
