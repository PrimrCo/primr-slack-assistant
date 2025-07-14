# Primr Slack Assistant

An AI-powered Slack assistant that can answer questions about your company documents using Retrieval-Augmented Generation (RAG).

## Features

- **Document Search**: Semantic search through your markdown documents
- **AI Responses**: Uses OpenAI GPT models for intelligent answers
- **Vector Storage**: Local FAISS or cloud Pinecone options
- **Slack Integration**: Ready for Slack bot deployment

## Prerequisites

- Python 3.9+ (Python 3.13 not supported by faiss-cpu yet)
- OpenAI API key
- macOS (for this setup guide)

## Installation & Setup

### 1. Install Dependencies

Due to faiss-cpu build issues with pip, we use conda for vector search components:

```bash
# Install miniconda (if not already installed)
brew install miniconda

# Create Python 3.9 environment for faiss compatibility
conda create -n faiss-env python=3.9
conda activate faiss-env

# Install faiss-cpu via conda
conda install -c conda-forge faiss-cpu

# Install ALL other packages via pip (one time only)
pip install langchain langchain-community langchain-openai openai tiktoken pinecone
```

### 2. Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
# Optional: only if using Pinecone
#PINECONE_API_KEY=your-pinecone-key
#PINECONE_ENVIRONMENT=your-pinecone-env
```

**Important**: Add `.env` to your `.gitignore` to keep API keys secure.

### 3. Get OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Create account and add billing (minimum $5)
3. Generate API key at [API Keys](https://platform.openai.com/api-keys)
4. Copy key to your `.env` file

**Pricing**: ~$0.001-0.005 per interaction for typical usage.

## Usage

### Step 1: Prepare Documents

Add your markdown files to the `data/` folder:

```bash
mkdir data
# Add your .md files: data/policies.md, data/benefits.md, etc.
```

### Step 2: Process Documents

Always activate your conda environment first:

```bash
conda activate faiss-env
```

Chunk your documents:

```bash
python ingest.py
```

This creates `chunks.json` with processed document chunks.

### Step 3: Build Vector Index

Create the searchable embeddings:

```bash
python build_story.py
```

This creates a `faiss_index/` directory with your vector database.

### Step 4: Test the System

Run the interactive query interface:

```bash
python query.py
```

Ask questions about your documents!

## Complete Workflow Example

```bash
# 1. Activate environment (packages already installed)
conda activate faiss-env

# 2. Add sample document
echo "# Company Policies\nOur vacation policy allows 3 weeks PTO..." > data/policies.md

# 3. Process documents
python ingest.py
# Output: 🔖 X chunks saved to chunks.json

# 4. Build vector index
python build_story.py
# Output: 💾 FAISS index saved to ./faiss_index/

# 5. Test queries
python query.py
# Ask: "What is the vacation policy?"
```

## Architecture

### File Structure
```
primr-slack-assistant/
├── data/                    # Your .md documents
├── faiss_index/            # Generated vector database
├── chunks.json             # Processed document chunks (JSON format)
├── index_info.json         # Index metadata
├── ingest.py              # Document processing
├── build_story.py         # Vector index creation
├── query.py               # Interactive Q&A
├── .env                   # API keys (gitignored)
└── README.md
```

### How It Works

1. **Document Processing** (`ingest.py`):
   - Loads `.md` files from `data/` folder
   - Splits into 1000-character chunks with 200-character overlap
   - Saves chunks to `chunks.json` (secure JSON format)

2. **Vector Index Creation** (`build_story.py`):
   - Loads document chunks from JSON
   - Creates embeddings using OpenAI's `text-embedding-ada-002`
   - Stores vectors in FAISS index for fast similarity search
   - Saves metadata to `index_info.json`

3. **Query Processing** (`query.py`):
   - Loads FAISS vector store
   - Converts user questions to embeddings
   - Finds top 5 most similar document chunks
   - Uses GPT-4 to generate contextual answers

## Vector Storage Options

### FAISS (Local - Default)
- ✅ Free and fast
- ✅ No external dependencies
- ✅ Good for development and small datasets
- ❌ No cloud sync or scaling


## Troubleshooting

### Common Issues

**OpenAI API v1.0+ compatibility errors**:
```bash
# If you get "APIRemovedInV1" errors:
# Make sure you're using ChatOpenAI for chat models:
from langchain_community.chat_models import ChatOpenAI

# And use invoke() instead of run():
result = qa.invoke({"query": query})
print(result["result"])
```

**LangChain deprecation warnings**:
```bash
# If you see "Chain.run was deprecated" warnings:
# Replace:
qa.run(query)
# With:
result = qa.invoke({"query": query})
print(result["result"])
```

**LangChain chat model warnings**:
```bash
# If you see warnings about "chat model" usage:
# Update your imports from:
from langchain_community.llms import OpenAI
# To:
from langchain_community.chat_models import ChatOpenAI

# Then change:
llm=OpenAI(model_name="gpt-4", temperature=0)
# To:
llm=ChatOpenAI(model_name="gpt-4", temperature=0)
```

**faiss-cpu build errors**:
```bash
# Solution: Use conda instead of pip
conda activate faiss-env
conda install -c conda-forge faiss-cpu
```

**Import errors**:
```bash
# Make sure you're in the right environment
conda activate faiss-env
python your_script.py
```

**OpenAI API errors**:
- Check your API key is correct in `.env`
- Verify billing is set up at platform.openai.com
- Ensure you have credits remaining

**No documents found**:
```bash
# Make sure you have .md files in data/
ls data/
# Should show your markdown files
```

### Performance Tips

- **Chunk size**: Adjust `chunk_size=1000` in `ingest.py` for your documents
- **Retrieval count**: Change `k=5` in `query.py` to return more/fewer context chunks
- **Model selection**: Switch between `gpt-4` and `gpt-3.5-turbo` in `query.py` for cost vs quality

## Slack Integration (Coming Soon)

To connect this to Slack:

1. Create a Slack app at [api.slack.com](https://api.slack.com)
2. Add bot tokens to `.env`
3. Deploy Python service for Slack events
4. Configure event subscriptions and slash commands

## Cost Estimation

**OpenAI Usage**:
- Document embedding: ~$0.10 per 100 documents
- Query responses: ~$0.001-0.005 per question
- Monthly usage (small team): $10-50

**Infrastructure**:
- FAISS: Free (local storage)
- Pinecone: $70/month (if using cloud option)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make sure to test with `conda activate faiss-env`
4. Submit a pull request

## Known Issues / Technical Debt

### Security: Pickle Dependency in FAISS
- **Issue**: FAISS vector store uses pickle for metadata serialization
- **Current mitigation**: We only load files we created ourselves
- **Risk level**: Low (controlled environment)
- **Future fix**: Migrate to pickle-free vector store (Chroma, Weaviate, or Pinecone)

### Alternative Vector Stores to Consider
- **Chroma**: Local SQLite-based, no pickle
- **Weaviate**: Open source, REST API
- **Pinecone**: Cloud-hosted, production-ready

```
# Future: query.py without pickle
from langchain_community.vectorstores import Chroma

vs = Chroma(
    persist_directory="./chroma_db",
    embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002")
)
# No allow_dangerous_deserialization needed!
```
