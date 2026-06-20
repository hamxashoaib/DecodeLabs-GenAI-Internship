# 🤖 Generative AI 
Industrial Training Mission Kit/br
**DecodeLabs | Batch 2026**

This repository contains my completed project submissions for the **Generative AI Industrial Training** program by DecodeLabs. Four out of five tasks have been implemented, covering prompt engineering, document intelligence (RAG), multimodal pipelines, and AI safety auditing.

---

## 📁 Repository Structure

```
DecodeLabs-GenAI-Internship/
│
├── task1_system_prompt_architect/
│   ├── system_prompt.md          # Full system prompt with persona + constraints
│   ├── few_shot_examples.md      # Few-shot prompting examples
│   └── README.md
│
├── task3_knowledge_analyst/
│   ├── rag_pipeline.py           # RAG simulation pipeline
│   ├── dashboard.py              # Streamlit summary dashboard
│   ├── sample_document.txt       # Sample legal/technical document
│   └── README.md
│
├── task4_multimodal_content_engine/
│   ├── pipeline.py               # Full multimodal pipeline
│   ├── transcribe.py             # Whisper transcription module
│   ├── viral_extractor.py        # GPT-based viral segment detector
│   ├── caption_generator.py      # Social media caption generator
│   ├── sample_output.json        # Example pipeline output
│   └── README.md
│
├── task5_ai_safety_audit/
│   ├── red_team_report.md        # Full red teaming findings report
│   ├── safety_framework.md       # Proposed guardrails & safety framework
│   ├── bias_test_results.md      # Gender/racial bias test documentation
│   └── README.md
│
└── README.md                     # This file
```

---

## ✅ Tasks Completed

| Task | Title | Status |
|------|-------|--------|
| Task 1 | The System Prompt Architect | ✅ Complete |
| Task 2 | The Creative Visionary | ⏭️ Skipped |
| Task 3 | The Knowledge Analyst (RAG) | ✅ Complete |
| Task 4 | The Multimodal Content Engine | ✅ Complete |
| Task 5 | The AI Safety & Bias Audit | ✅ Complete |

---

## 🛠️ Tech Stack

| Tool / Library | Purpose |
|----------------|---------|
| Python 3.10+ | Core language |
| OpenAI / Anthropic API | LLM backbone |
| Whisper (openai-whisper) | Speech-to-text transcription |
| Streamlit | RAG dashboard UI |
| LangChain | RAG pipeline orchestration |
| FAISS | Vector similarity search |
| PyPDF2 | PDF document parsing |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/hamxashoaib/DecodeLabs-GenAI-Internship.git
cd DecodeLabs-GenAI-Internship

```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
# Add your OpenAI API key to .env
```

### 4. Run individual tasks
```bash
# Task 3 – RAG Dashboard
streamlit run task3_knowledge_analyst/dashboard.py

# Task 4 – Multimodal Pipeline
python task4_multimodal_content_engine/pipeline.py

# Task 5 – Safety Audit Report
# See task5_ai_safety_audit/red_team_report.md
```

---

## 👤 Author

**Hamza Shoaib**/
 Artificial Intelligence/n
 The Islamia University of Bahawalpur (IUB)/n
Batch (May 5 - Jun 5) | DecodeLabs Generative AI Internship

---

## 📄 License
MIT License – feel free to fork and build on top of this work.
