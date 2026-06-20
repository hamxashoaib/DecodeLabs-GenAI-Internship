# Task 3 – The Knowledge Analyst (RAG Concepts) 📚

## Objective
Simulate a Retrieval-Augmented Generation (RAG) workflow that allows a user to upload a long legal/technical document and ask questions about it — with the AI forced to cite specific sections for every answer.

## What's Included

| File | Description |
|------|-------------|
| `rag_pipeline.py` | Core RAG pipeline: load PDF → chunk → embed → retrieve → generate |
| `dashboard.py` | Streamlit dashboard to upload docs and extract Risks, Dates, Stakeholders |
| `sample_document.txt` | Sample legal contract used for testing |
| `requirements.txt` | Python dependencies |

## How It Works

```
[PDF/TXT Upload]
      ↓
[Text Chunking - LangChain RecursiveCharacterTextSplitter]
      ↓
[Embedding - OpenAI text-embedding-ada-002 / sentence-transformers]
      ↓
[Vector Store - FAISS]
      ↓
[User Query] → [Similarity Search] → [Top-K Relevant Chunks]
      ↓
[GPT-4 / Claude] + [Prompt: "Cite section/page for every claim"]
      ↓
[Answer with citations]
```

## Running the Dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

Then open `http://localhost:8501` in your browser.

## Key RAG Concepts Demonstrated
- **Chunking strategy** – overlapping chunks to avoid losing context at boundaries
- **Citation enforcement** – system prompt forces the model to cite every claim
- **Structured extraction** – automatic extraction of Risks, Dates, and Stakeholders
- **Hallucination prevention** – model is instructed to say "not found in document" rather than guess
