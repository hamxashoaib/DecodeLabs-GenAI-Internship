"""
Task 3 – The Knowledge Analyst: RAG Pipeline
DecodeLabs Generative AI Internship | Batch 2026

This script implements a Retrieval-Augmented Generation (RAG) pipeline for
document intelligence. It loads a document, chunks it, embeds it into a FAISS
vector store, then retrieves relevant chunks to answer user questions — with
every answer forced to cite the source section.
"""

import os
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# DEPENDENCIES  (pip install langchain langchain-openai faiss-cpu pypdf2)
# ---------------------------------------------------------------------------
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain.schema import Document
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
except ImportError:
    print("Install dependencies: pip install langchain langchain-openai faiss-cpu pypdf2")
    exit(1)

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
CHUNK_SIZE = 500          # characters per chunk
CHUNK_OVERLAP = 80        # overlap between chunks to preserve context
TOP_K_RESULTS = 4         # number of chunks to retrieve per query
MODEL_NAME = "gpt-4o"


# ---------------------------------------------------------------------------
# CITATION-ENFORCING PROMPT TEMPLATE
# ---------------------------------------------------------------------------
RAG_PROMPT_TEMPLATE = """
You are a precise legal and technical document analyst.
Your task is to answer the user's question using ONLY the context provided below.

STRICT RULES:
1. Every factual claim in your answer MUST include a citation in the format: [Section X.X] or [Page N].
2. If the answer is not found in the context, respond with: "This information is not found in the provided document."
3. Never guess, hallucinate, or use outside knowledge.
4. Be concise and professional.

CONTEXT FROM DOCUMENT:
{context}

QUESTION: {question}

ANSWER (with citations):
"""

CITATION_PROMPT = PromptTemplate(
    template=RAG_PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)


# ---------------------------------------------------------------------------
# STEP 1: LOAD DOCUMENT
# ---------------------------------------------------------------------------
def load_document(file_path: str) -> str:
    """Load a .txt or .pdf document and return raw text."""
    path = Path(file_path)

    if path.suffix == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    elif path.suffix == ".pdf":
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            text = ""
            for i, page in enumerate(reader.pages):
                text += f"\n[Page {i+1}]\n{page.extract_text()}"
            return text
        except ImportError:
            print("Install PyPDF2: pip install pypdf2")
            return ""

    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")


# ---------------------------------------------------------------------------
# STEP 2: CHUNK THE DOCUMENT
# ---------------------------------------------------------------------------
def chunk_document(raw_text: str) -> list[Document]:
    """Split document into overlapping chunks for better retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_text(raw_text)
    # Wrap in LangChain Document objects with metadata
    documents = [
        Document(page_content=chunk, metadata={"chunk_id": i, "source": "uploaded_document"})
        for i, chunk in enumerate(chunks)
    ]
    print(f"[RAG] Document split into {len(documents)} chunks.")
    return documents


# ---------------------------------------------------------------------------
# STEP 3: BUILD VECTOR STORE
# ---------------------------------------------------------------------------
def build_vector_store(documents: list[Document]) -> FAISS:
    """Embed chunks and store in FAISS for similarity search."""
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = FAISS.from_documents(documents, embeddings)
    print("[RAG] Vector store built successfully.")
    return vector_store


# ---------------------------------------------------------------------------
# STEP 4: CREATE QA CHAIN
# ---------------------------------------------------------------------------
def build_qa_chain(vector_store: FAISS) -> RetrievalQA:
    """Build a RetrievalQA chain that enforces citations."""
    llm = ChatOpenAI(
        model_name=MODEL_NAME,
        temperature=0,              # deterministic for factual tasks
        openai_api_key=OPENAI_API_KEY
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": TOP_K_RESULTS})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": CITATION_PROMPT}
    )
    return qa_chain


# ---------------------------------------------------------------------------
# STEP 5: STRUCTURED EXTRACTION (Risks, Dates, Stakeholders)
# ---------------------------------------------------------------------------
def extract_structured_info(qa_chain: RetrievalQA) -> dict:
    """Automatically extract Risks, Dates, and Stakeholders from the document."""
    queries = {
        "risks": "List all risks mentioned in this document. Cite the section for each.",
        "dates": "List all dates and deadlines mentioned in this document with their context. Cite sections.",
        "stakeholders": "Who are the key stakeholders or parties mentioned in this document? Cite sections."
    }

    results = {}
    for category, query in queries.items():
        print(f"[RAG] Extracting: {category}...")
        response = qa_chain.invoke({"query": query})
        results[category] = response.get("result", "Extraction failed.")

    return results


# ---------------------------------------------------------------------------
# MAIN – INTERACTIVE Q&A LOOP
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("  DecodeLabs RAG Pipeline – Document Intelligence")
    print("=" * 60)

    # Load document
    doc_path = "sample_document.txt"
    if not Path(doc_path).exists():
        print(f"[ERROR] Document not found: {doc_path}")
        return

    raw_text = load_document(doc_path)
    documents = chunk_document(raw_text)
    vector_store = build_vector_store(documents)
    qa_chain = build_qa_chain(vector_store)

    print("\n[AUTO EXTRACTION] Extracting key information from document...\n")
    structured = extract_structured_info(qa_chain)

    print("\n📋 STRUCTURED EXTRACTION RESULTS")
    print("-" * 40)
    for key, value in structured.items():
        print(f"\n🔹 {key.upper()}:\n{value}")

    # Save extraction results
    with open("extraction_results.json", "w") as f:
        json.dump(structured, f, indent=2)
    print("\n[INFO] Extraction results saved to extraction_results.json")

    # Interactive Q&A
    print("\n\n💬 INTERACTIVE Q&A MODE (type 'exit' to quit)")
    print("-" * 40)
    while True:
        question = input("\nAsk a question about the document: ").strip()
        if question.lower() in ("exit", "quit", "q"):
            print("Exiting RAG pipeline. Goodbye!")
            break
        if not question:
            continue

        response = qa_chain.invoke({"query": question})
        print(f"\n🤖 Answer:\n{response.get('result', 'No answer generated.')}")


if __name__ == "__main__":
    main()
