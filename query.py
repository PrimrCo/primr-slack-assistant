# query.py
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
# from langchain.vectorstores import Pinecone
# import pinecone

load_dotenv()

# === For FAISS ===
vs = FAISS.load_local("faiss_index", OpenAIEmbeddings(model="text-embedding-ada-002"))

# === For Pinecone ===
# pinecone.init(api_key=os.getenv("PINECONE_API_KEY"),
#               environment=os.getenv("PINECONE_ENVIRONMENT"))
# index = pinecone.Index("primr-docs")
# vs = Pinecone(index, OpenAIEmbeddings(model="text-embedding-ada-002"))

retriever = vs.as_retriever(search_kwargs={"k": 5})

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(model_name="gpt-4", temperature=0),
    chain_type="stuff",
    retriever=retriever,
)

while True:
    query = input("🔍 Ask Primr: ")
    if not query.strip():
        break
    print("\n💡", qa.run(query))
