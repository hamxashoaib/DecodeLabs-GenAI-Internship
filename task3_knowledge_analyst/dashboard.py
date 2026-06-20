"""
Task 3 – The Knowledge Analyst: Streamlit Summary Dashboard
DecodeLabs Generative AI Internship | Batch 2026

Run with: streamlit run dashboard.py
"""

import os
import json
import streamlit as st
from pathlib import Path

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Document Intelligence Dashboard",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Document Intelligence Dashboard")
st.caption("Powered by RAG – Retrieval-Augmented Generation | DecodeLabs Internship Task 3")

# ---------------------------------------------------------------------------
# SIDEBAR – SETTINGS
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    model_choice = st.selectbox("LLM Model", ["gpt-4o", "gpt-3.5-turbo", "gpt-4"])
    top_k = st.slider("Chunks to retrieve (Top-K)", 2, 8, 4)
    st.divider()
    st.info("Upload a PDF or TXT document to get started.")

# ---------------------------------------------------------------------------
# IMPORTS (lazy — only after key is entered)
# ---------------------------------------------------------------------------
def load_rag_modules():
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_community.vectorstores import FAISS
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        from langchain.schema import Document
        from langchain.chains import RetrievalQA
        from langchain.prompts import PromptTemplate
        return True, (RecursiveCharacterTextSplitter, FAISS, OpenAIEmbeddings,
                      ChatOpenAI, Document, RetrievalQA, PromptTemplate)
    except ImportError:
        return False, None

# ---------------------------------------------------------------------------
# DOCUMENT UPLOAD
# ---------------------------------------------------------------------------
st.subheader("1️⃣ Upload Your Document")
uploaded_file = st.file_uploader(
    "Upload a legal or technical document (PDF or TXT)",
    type=["pdf", "txt"]
)

use_sample = st.checkbox("Use the included sample contract instead")

# ---------------------------------------------------------------------------
# RAG PROMPT
# ---------------------------------------------------------------------------
RAG_PROMPT = """
You are a precise legal and technical document analyst.
Answer the question using ONLY the context below.
Every claim MUST include a citation: [Section X.X] or [Page N].
If not found, say: "Not found in the document."

CONTEXT:
{context}

QUESTION: {question}

ANSWER (with citations):
"""

# ---------------------------------------------------------------------------
# BUILD PIPELINE
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Building vector store...")
def build_pipeline(text_content: str, _api_key: str, _model: str, _k: int):
    ok, modules = load_rag_modules()
    if not ok:
        return None
    (RecursiveCharacterTextSplitter, FAISS, OpenAIEmbeddings,
     ChatOpenAI, Document, RetrievalQA, PromptTemplate) = modules

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.split_text(text_content)
    docs = [Document(page_content=c, metadata={"chunk_id": i}) for i, c in enumerate(chunks)]

    embeddings = OpenAIEmbeddings(openai_api_key=_api_key)
    vector_store = FAISS.from_documents(docs, embeddings)

    llm = ChatOpenAI(model_name=_model, temperature=0, openai_api_key=_api_key)
    prompt = PromptTemplate(template=RAG_PROMPT, input_variables=["context", "question"])
    retriever = vector_store.as_retriever(search_kwargs={"k": _k})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain

# ---------------------------------------------------------------------------
# MAIN FLOW
# ---------------------------------------------------------------------------
doc_text = None

if use_sample:
    sample_path = Path("sample_document.txt")
    if sample_path.exists():
        doc_text = sample_path.read_text(encoding="utf-8")
        st.success("Sample contract loaded successfully.")
    else:
        st.warning("sample_document.txt not found in current directory.")

elif uploaded_file:
    if uploaded_file.type == "text/plain":
        doc_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        try:
            from PyPDF2 import PdfReader
            import io
            reader = PdfReader(io.BytesIO(uploaded_file.read()))
            doc_text = ""
            for i, page in enumerate(reader.pages):
                doc_text += f"\n[Page {i+1}]\n{page.extract_text()}"
        except ImportError:
            st.error("Install PyPDF2: pip install pypdf2")
    if doc_text:
        st.success(f"Document loaded. ({len(doc_text)} characters)")

# ---------------------------------------------------------------------------
# DASHBOARD TABS
# ---------------------------------------------------------------------------
if doc_text:
    st.divider()
    tab1, tab2, tab3 = st.tabs(["📊 Summary Dashboard", "💬 Q&A Chat", "📄 Raw Document"])

    with tab3:
        st.subheader("Raw Document Text")
        st.text_area("Content", doc_text, height=400)

    if not api_key:
        st.warning("Enter your OpenAI API key in the sidebar to enable AI features.")
    else:
        qa_chain = build_pipeline(doc_text, api_key, model_choice, top_k)

        if qa_chain:
            with tab1:
                st.subheader("2️⃣ Automated Extraction")
                col1, col2, col3 = st.columns(3)

                extractions = {
                    "⚠️ Risks": "List all risks in this document with citations [Section X.X].",
                    "📅 Dates & Deadlines": "List all dates and deadlines in this document with citations.",
                    "👥 Stakeholders": "Who are all the key parties and stakeholders? Include citations."
                }
                cols = [col1, col2, col3]

                for (label, query), col in zip(extractions.items(), cols):
                    with col:
                        st.markdown(f"**{label}**")
                        with st.spinner(f"Extracting {label}..."):
                            try:
                                result = qa_chain.invoke({"query": query})
                                st.write(result.get("result", "Failed to extract."))
                            except Exception as e:
                                st.error(f"Error: {e}")

            with tab2:
                st.subheader("3️⃣ Ask Anything About the Document")
                st.caption("Every answer will include citations to the document sections.")

                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []

                # Display history
                for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"]):
                        st.write(msg["content"])

                question = st.chat_input("Ask a question about the document...")
                if question:
                    st.session_state.chat_history.append({"role": "user", "content": question})
                    with st.chat_message("user"):
                        st.write(question)

                    with st.chat_message("assistant"):
                        with st.spinner("Searching document..."):
                            try:
                                response = qa_chain.invoke({"query": question})
                                answer = response.get("result", "No answer generated.")
                                st.write(answer)
                                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                            except Exception as e:
                                st.error(f"Error: {e}")
        else:
            st.error("Failed to load RAG modules. Run: pip install langchain langchain-openai faiss-cpu")

else:
    st.info("Upload a document or enable the sample document to get started.")
