import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import glob

load_dotenv()

def log_status(message, status="info"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {status.upper()}: {message}")

def main():
    success = False  # Track if vector creation was successful
    try:
        log_status("Starting knowledge base ingestion...")

        # Debug: Check environment variables
        openai_key = os.getenv("OPENAI_API_KEY")
        log_status(f"OpenAI API Key loaded: {'Yes' if openai_key else 'No'}")
        if openai_key:
            log_status(f"Key preview: {openai_key[:20]}...{openai_key[-10:]}")

        # 1. Load all .md and .txt files
        data_paths = glob.glob("data/*.md") + glob.glob("data/*.txt")

        if not data_paths:
            log_status("No markdown or text files found in data/ directory", "warning")
            return

        log_status(f"Found {len(data_paths)} files to process")

        all_docs = []
        for path in data_paths:
            try:
                loader = TextLoader(path, encoding="utf-8")
                docs = loader.load()
                all_docs.extend(docs)
                log_status(f"Loaded: {path}")
            except Exception as e:
                log_status(f"Failed to load {path}: {e}", "error")
                continue

        if not all_docs:
            log_status("No documents were successfully loaded", "error")
            return

        # 2. Chunk them
        log_status("Splitting documents into chunks...")
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(all_docs)
        log_status(f"Created {len(chunks)} chunks")

        # 3. Convert chunks to JSON-serializable format
        chunks_data = []
        for i, chunk in enumerate(chunks):
            chunk_data = {
                "id": i,
                "page_content": chunk.page_content,
                "metadata": {
                    **chunk.metadata,
                    "chunk_index": i,
                    "processed_at": datetime.now().isoformat()
                }
            }
            chunks_data.append(chunk_data)

        # 4. Save chunks to JSON
        log_status("Saving chunks to chunks.json...")
        with open("chunks.json", "w", encoding="utf-8") as f:
            json.dump(chunks_data, f, indent=2, ensure_ascii=False)

        # 5. Create embeddings and simple vector index (no pickle)
        try:
            from langchain_openai import OpenAIEmbeddings
            import numpy as np

            log_status("Creating embeddings...")

            # Set environment variable explicitly to ensure it's not masked
            os.environ["OPENAI_API_KEY"] = openai_key

            # Create embeddings model without passing key (let it use env var)
            embeddings_model = OpenAIEmbeddings(
                model="text-embedding-ada-002"
            )

            log_status("Building vector index...")

            # Get embeddings for all chunks
            texts = [chunk.page_content for chunk in chunks]
            embeddings = embeddings_model.embed_documents(texts)

            # Save embeddings and metadata as JSON (no pickle)
            vector_data = {
                "embeddings": [emb for emb in embeddings],  # Convert to regular lists
                "texts": texts,
                "metadata": [chunk.metadata for chunk in chunks],
                "created_at": datetime.now().isoformat(),
                "embedding_model": "text-embedding-ada-002",
                "dimensions": len(embeddings[0]) if embeddings else 0
            }

            # Save to JSON file
            log_status("Saving vector index to vectors.json...")
            with open("vectors.json", "w", encoding="utf-8") as f:
                json.dump(vector_data, f, indent=2, ensure_ascii=False)

            log_status("✅ Vector index created successfully!")
            success = True  # Only set to True if we get here

        except ImportError as e:
            log_status(f"Import error: {e}", "error")
            log_status("OpenAI embeddings not available, skipping vector index creation", "warning")
            success = False
        except Exception as e:
            log_status(f"❌ Failed to create vector index: {e}", "error")
            import traceback
            log_status(f"Full traceback: {traceback.format_exc()}", "error")
            success = False  # Explicitly set to False on error

        # 6. Create metadata file
        metadata = {
            "last_updated": datetime.now().isoformat(),
            "total_files": len(data_paths),
            "total_chunks": len(chunks_data),
            "files_processed": [os.path.basename(path) for path in data_paths],
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "vector_index_created": success
        }

        with open("index_info.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        # Final status based on whether vector index was created
        if success:
            log_status(f"✅ Ingestion completed successfully!")
            log_status(f"📊 Processed {len(data_paths)} files into {len(chunks_data)} chunks with vector index")
        else:
            log_status(f"⚠️ Ingestion completed with errors (no vector index created)", "error")
            log_status(f"📊 Processed {len(data_paths)} files into {len(chunks_data)} chunks (chunks only)")
            log_status("❌ Vector search will not be available until embedding creation succeeds", "error")

    except Exception as e:
        log_status(f"❌ Ingestion failed completely: {e}", "error")
        raise

if __name__ == "__main__":
    main()
