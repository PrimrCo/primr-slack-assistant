"""
Simple vector search utility that works with JSON-based embeddings (no pickle)
"""
import json
import numpy as np
from typing import List, Tuple
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SimpleVectorStore:
    """Simple vector store using JSON storage (no pickle dependencies)"""

    def __init__(self, vectors_file="vectors.json"):
        self.vectors_file = vectors_file
        self.embeddings_model = OpenAIEmbeddings()
        self.data = None
        self.load()

    def load(self):
        """Load vectors from JSON file"""
        try:
            with open(self.vectors_file, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            print(f"✅ Loaded {len(self.data.get('texts', []))} vectors from {self.vectors_file}")
        except FileNotFoundError:
            print(f"❌ Vector file {self.vectors_file} not found")
            self.data = None
        except Exception as e:
            print(f"❌ Error loading vectors: {e}")
            self.data = None

    def similarity_search(self, query: str, k: int = 5) -> List[Tuple[str, dict, float]]:
        """
        Search for similar texts to the query
        Returns list of (text, metadata, similarity_score) tuples
        """
        if not self.data or not self.data.get("embeddings"):
            return []

        try:
            # Get query embedding
            query_embedding = self.embeddings_model.embed_query(query)
            query_vec = np.array(query_embedding)

            # Calculate similarities
            similarities = []
            for i, doc_embedding in enumerate(self.data["embeddings"]):
                doc_vec = np.array(doc_embedding)
                # Cosine similarity
                similarity = np.dot(query_vec, doc_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(doc_vec))
                similarities.append((i, similarity))

            # Sort by similarity (highest first)
            similarities.sort(key=lambda x: x[1], reverse=True)

            # Return top k results
            results = []
            for i, score in similarities[:k]:
                text = self.data["texts"][i]
                metadata = self.data.get("metadata", [{}])[i] if i < len(self.data.get("metadata", [])) else {}
                results.append((text, metadata, score))

            return results

        except Exception as e:
            print(f"❌ Error during search: {e}")
            return []

    def get_all_texts(self) -> List[str]:
        """Get all stored texts"""
        if not self.data:
            return []
        return self.data.get("texts", [])

    def get_stats(self) -> dict:
        """Get statistics about the vector store"""
        if not self.data:
            return {"status": "not_loaded"}

        return {
            "status": "loaded",
            "total_vectors": len(self.data.get("texts", [])),
            "embedding_model": self.data.get("embedding_model", "unknown"),
            "dimensions": self.data.get("dimensions", 0),
            "created_at": self.data.get("created_at", "unknown")
        }


if __name__ == "__main__":
    # Test the vector store
    vs = SimpleVectorStore()

    if vs.data:
        print("\n📊 Vector store stats:")
        stats = vs.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")

        # Test search
        query = input("\n🔍 Enter search query: ")
        if query.strip():
            results = vs.similarity_search(query, k=3)
            print(f"\n📝 Top {len(results)} results:")
            for i, (text, metadata, score) in enumerate(results, 1):
                print(f"\n{i}. Score: {score:.4f}")
                print(f"   Text: {text[:200]}...")
                print(f"   Source: {metadata.get('source', 'unknown')}")
    else:
        print("❌ No vector data available. Run enhanced_ingest.py first.")
