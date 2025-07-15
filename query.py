import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from vector_search import SimpleVectorStore

load_dotenv()

# Load our custom vector store (no pickle)
vs = SimpleVectorStore("vectors.json")

# Create a simple QA system without RetrievalQA
def answer_question(query: str) -> str:
    # Get relevant documents
    results = vs.similarity_search(query, k=5)

    if not results:
        return "I don't have information to answer that question."

    # Format context from results
    context = "\n\n".join([f"Document {i+1}:\n{text}" for i, (text, _, _) in enumerate(results)])

    # Create prompt
    prompt_template = """Use the following context to answer the question. If you cannot answer based on the context, say so.

Context:
{context}

Question: {question}

Answer:"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    # Create LLM chain
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)

    # Get answer
    response = chain.run(context=context, question=query)
    return response

if __name__ == "__main__":
    while True:
        query = input("🔍 Ask Primr: ")
        if not query.strip():
            break

        answer = answer_question(query)
        print(f"\n🤖 Answer: {answer}\n")
