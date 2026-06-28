# 🏥 Clinical Prior Authorization Agent
**Cotiviti Internship Assessment — Generative AI / Agentic AI**  
**Sushmitha Urs | Northeastern University | M.S. Analytics & Artificial Intelligence**

---

## Overview
An agentic AI system that automates clinical prior authorization decisions using LangGraph, RAG policy retrieval, and Groq LLM inference. Given a free-text patient case summary, the agent reasons through it step by step — retrieving the exact payer policy document, evaluating each coverage criterion against that policy, and producing an APPROVED / DENIED / PENDING decision with full written justification.

---

## Agent Architecture — 4-Node LangGraph Pipeline
## Agent Architecture — 4-Node LangGraph Pipeline

```
Patient Case Input
       │
       ▼
[Node 1] Extract Clinical Facts
   NLP reader — pulls age, diagnosis, treatment, history, documentation status
       │
       ▼
[Node 2] Retrieve Relevant Policy (RAG)
   Keyword-based retrieval — fetches the correct payer policy document
   (Medicare LCD L33822 / AIM Lumbar Spine Guidelines / BCBS MED-00048 / CMS Cardiac ILR)
       │
       ▼
[Node 3] Policy-Grounded Criteria Analysis
   LLM Reasoner — evaluates each coverage criterion, cites specific policy clauses
   Outputs: MET / NOT MET / INSUFFICIENT INFORMATION per criterion
       │
       ▼
[Node 4] Generate Final Decision
   Decision Engine — APPROVED / DENIED / PENDING + justification + next steps
```
---

## Tech Stack
| Tool | Role |
|------|------|
| **LangGraph** | 4-node agentic graph orchestration |
| **Groq LLM** | Fast LLM inference at each node |
| **RAG Retriever** | Keyword-based payer policy document retrieval |
| **Streamlit** | Interactive web frontend |
| **Python + dotenv** | Environment management |

---

## Policies Included (RAG Knowledge Base)
- **Medicare LCD L33822** — Continuous Glucose Monitoring (CGM) Devices
- **AIM Lumbar Spine MRI Guidelines** — Advanced Imaging
- **BCBS Medical Policy MED-00048** — Biologic DMARDs for Rheumatoid Arthritis
- **CMS Cardiac ILR Policy** — Implantable Loop Recorders

---

## Test Cases & Results
| Case | Condition | Requested | Decision |
|------|-----------|-----------|----------|
| 1 | Type 2 Diabetes, HbA1c 9.2%, on insulin | CGM Device | ✅ APPROVED |
| 2 | Non-specific back pain, 2 weeks, no treatment tried | Lumbar MRI | ❌ DENIED |
| 3 | Syncope, Holter inconclusive, tilt test pending | ILR Implant | ⏳ PENDING |

---

## Setup & Run

**1. Clone the repo**
```bash
git clone https://github.com/sushmithaurs/cotiviti-prior-auth-agent.git
cd cotiviti-prior-auth-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create `.env` file**
'''bash
GROQ_API_KEY=your_groq_api_key_here'
'''

**4. Run the app**
```bash
streamlit run app.py
```

---

## Topic
**Topic 2 — Clinical Decision Making and Pattern Recognition in Health Care**  
Agentic Generative AI · Chain Reasoning · RAG Policy Grounding · LangGraph · TPO (Treatment, Payment & Operations)

---

## Deliverables
- `agent.py` — LangGraph 4-node agentic pipeline
- `app.py` — Streamlit frontend
- `policies.py` — RAG policy document store
- `requirements.txt` — Dependencies
- `Cotiviti_Report.docx` — Written report (APA format)
- `Cotiviti_Presentation.pptx` — Slide deck
- `demo.mp4` — Video presentation and live POC demo
  ## Video Demo
[Watch the demo here]-https://drive.google.com/file/d/1oNLDiCbAzQLkufVPIqZdEMD3nZzKP1rp/view?usp=sharing
