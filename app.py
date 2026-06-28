import streamlit as st
from agent import run_agent

st.set_page_config(
    page_title="Prior Auth Agent | Cotiviti POC",
    page_icon="🏥",
    layout="wide",
)

st.markdown("""
<style>
footer { display:none; }
#MainMenu { display:none; }
header[data-testid="stHeader"] { display:none; }
[data-testid="stSidebarCollapsedControl"] { display:none !important; }
[data-testid="collapsedControl"] { display:none !important; }

/* Remove all default padding */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
.stApp { overflow: hidden; }

/* Full viewport wrapper */
.app-wrapper {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
}

/* Header */
.app-header {
    background: linear-gradient(90deg, #0f172a, #1e3a5f, #0f172a);
    padding: 12px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 2px solid #3b82f6;
    flex-shrink: 0;
}
.header-left { display: flex; align-items: center; gap: 14px; }
.header-icon {
    width: 40px; height: 40px; background: #3b82f6;
    border-radius: 10px; display: flex; align-items: center;
    justify-content: center; font-size: 20px;
}
.header-title { font-size: 17px; font-weight: 700; color: #f1f5f9; margin: 0; }
.header-sub { font-size: 11px; color: #94a3b8; margin: 2px 0 0; }
.header-badges { display: flex; gap: 8px; }
.badge { font-size: 11px; font-weight: 600; padding: 4px 12px; border-radius: 20px; }
.b-blue   { background:#1d4ed8; color:#bfdbfe; border:1px solid #3b82f6; }
.b-green  { background:#065f46; color:#6ee7b7; border:1px solid #10b981; }
.b-purple { background:#4c1d95; color:#c4b5fd; border:1px solid #7c3aed; }

/* Body row */
.body-row {
    display: flex;
    flex: 1;
    overflow: hidden;
}

/* Left panel — fixed, no scroll */
.left-panel {
    width: 360px;
    min-width: 360px;
    background: linear-gradient(180deg, #0f172a, #1e293b);
    padding: 20px 18px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border-right: 1px solid #1e3a5f;
    overflow: hidden;
}
.panel-label {
    font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: .08em;
    color: #64748b; margin: 8px 0 4px;
}

/* Right panel — scrollable */
.right-panel {
    flex: 1;
    overflow-y: auto;
    padding: 24px 28px;
    background: #f8fafc;
}

/* Step cards */
.step-card { border-radius: 12px; margin-bottom: 18px; overflow: hidden; box-shadow: 0 1px 6px rgba(0,0,0,0.07); }
.sh1 { background: linear-gradient(90deg,#1e3a5f,#1e40af); padding:12px 18px; display:flex; align-items:center; gap:12px; }
.sh2 { background: linear-gradient(90deg,#134e4a,#0f766e); padding:12px 18px; display:flex; align-items:center; gap:12px; }
.sh3 { background: linear-gradient(90deg,#3b0764,#6d28d9); padding:12px 18px; display:flex; align-items:center; gap:12px; }
.snum { width:26px; height:26px; border-radius:50%; background:rgba(255,255,255,0.2); color:white; font-size:12px; font-weight:700; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.stitle { font-size:14px; font-weight:600; color:#fff; }
.sbody { padding:16px 18px; font-size:13.5px; color:#1e293b; line-height:1.8; background:#fff; border:1px solid #e2e8f0; border-top:none; border-radius:0 0 12px 12px; }

/* Decision */
.dec-approved { border-radius:12px; padding:20px 22px; margin-bottom:16px; background:linear-gradient(135deg,#ecfdf5,#d1fae5); border:1.5px solid #6ee7b7; }
.dec-denied   { border-radius:12px; padding:20px 22px; margin-bottom:16px; background:linear-gradient(135deg,#fef2f2,#fee2e2); border:1.5px solid #fca5a5; }
.dec-pending  { border-radius:12px; padding:20px 22px; margin-bottom:16px; background:linear-gradient(135deg,#fffbeb,#fef3c7); border:1.5px solid #fcd34d; }
.dec-label { font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.07em; color:#6b7280; margin-bottom:8px; }
.dv-a { font-size:22px; font-weight:800; color:#065f46; margin-bottom:10px; }
.dv-d { font-size:22px; font-weight:800; color:#991b1b; margin-bottom:10px; }
.dv-p { font-size:22px; font-weight:800; color:#92400e; margin-bottom:10px; }
.db-a { font-size:13.5px; line-height:1.8; color:#064e3b; white-space:pre-wrap; }
.db-d { font-size:13.5px; line-height:1.8; color:#7f1d1d; white-space:pre-wrap; }
.db-p { font-size:13.5px; line-height:1.8; color:#78350f; white-space:pre-wrap; }

/* Streamlit widget overrides inside left panel */
[data-testid="stSidebar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

CASES = {
    "— paste your own —": "",
    "Case 1 — Approve (CGM for Diabetic Patient)": """Patient: 58-year-old female with a 10-year history of Type 2 diabetes and hypertension. Treating endocrinologist (board-certified) has documented medical necessity and submitted a formal order for a continuous glucose monitoring (CGM) device. Patient HbA1c is 9.2%, currently on insulin therapy twice daily. Previous fingerstick monitoring has been inconsistent due to the patient arthritis limiting manual dexterity. Patient has completed CGM education with a certified diabetes educator at the clinic. No prior CGM use. Endocrinologist notes poor glycemic control and recommends CGM to improve adherence and reduce hypoglycemic episodes. Patient has tried dietary modification and oral medications prior to insulin initiation. No active infections or contraindications noted.""",
    "Case 2 — Deny (MRI for Non-Specific Back Pain)": """Patient: 34-year-old male presenting with lower back pain of 2 weeks duration. No history of trauma, fever, or neurological symptoms such as numbness or weakness. Physician is requesting an MRI of the lumbar spine. Patient has not tried physical therapy, NSAIDs, or any conservative management. No prior imaging ordered. No red flag symptoms documented such as bowel or bladder dysfunction, saddle anesthesia, or unexplained weight loss. Pain is described as mild to moderate, with no radiation to the lower extremities. No history of malignancy or spinal infection suspected.""",
    "Case 3 — Pending (Biologic Therapy for RA)": """Patient: 61-year-old male presenting with recurrent unexplained syncope episodes occurring approximately once per month for the past 3 months. A board-certified cardiologist is requesting approval for an implantable loop recorder (ILR) to monitor for intermittent arrhythmias. Patient has undergone a standard 24-hour Holter monitor and a 30-day event monitor, both of which were inconclusive. Echocardiogram completed last month showed normal left ventricular function with no structural abnormalities. Patient has no history of prior cardiac procedures. Physician has documented medical necessity and submitted a formal order for ILR implantation. However, the results of the tilt table test ordered by the cardiologist to rule out vasovagal syncope have not yet been received and are expected within the next 5 business days. The cardiologist notes these results are required before proceeding.""",
}

# ── Render header ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="header-left">
        <div class="header-icon">🏥</div>
        <div>
            <p class="header-title">Clinical Prior Authorization Agent</p>
            <p class="header-sub">Agentic AI · Chain Reasoning · RAG Policy Grounding · LangGraph</p>
        </div>
    </div>
    <div class="header-badges">
        <span class="badge b-blue">LangGraph</span>
        <span class="badge b-green">Groq LLaMA3</span>
        <span class="badge b-purple">RAG</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Two native columns ────────────────────────────────────────────────────────
left, right = st.columns([1, 1.7], gap="small")

with left:
    st.markdown("""
    <style>
    [data-testid="column"]:first-child * { color: #e2e8f0 !important; }
    [data-testid="column"]:first-child textarea {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        color: #e2e8f0 !important;
    }
    [data-testid="column"]:first-child [data-baseweb="select"] * {
        background: #1e293b !important;
        color: #e2e8f0 !important;
        border-color: #334155 !important;
    }
    [data-testid="column"]:first-child button[kind="primary"] {
        background: #3b82f6 !important;
        border: none !important;
    }
    </style>
    <script>
    (function() {
        function fixLeftCol() {
            const cols = window.parent.document.querySelectorAll('[data-testid="column"]');
            if (cols.length >= 1) {
                const left = cols[0];
                left.style.position = 'sticky';
                left.style.top = '0';
                left.style.height = '100vh';
                left.style.overflowY = 'auto';
                left.style.background = 'linear-gradient(180deg, #0f172a, #1e293b)';
                left.style.padding = '20px 16px';
                left.style.borderRight = '1px solid #1e3a5f';
                left.style.flexShrink = '0';
                // Also make the parent a flex row with overflow hidden
                const parent = left.parentElement;
                if (parent) {
                    parent.style.display = 'flex';
                    parent.style.alignItems = 'flex-start';
                    parent.style.overflow = 'hidden';
                    parent.style.height = 'calc(100vh - 70px)';
                }
            }
        }
        setTimeout(fixLeftCol, 200);
        setTimeout(fixLeftCol, 600);
        setTimeout(fixLeftCol, 1200);
    })();
    </script>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#64748b;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;'>Sample Cases</p>", unsafe_allow_html=True)
    selected = st.selectbox("case", list(CASES.keys()), label_visibility="collapsed")

    st.markdown("<p style='color:#64748b;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin:10px 0 4px;'>Patient Case Summary</p>", unsafe_allow_html=True)
    case_text = st.text_area("txt", value=CASES[selected], height=360,
        placeholder="Enter patient age, diagnosis, requested treatment, clinical history...",
        label_visibility="collapsed")

    run_button = st.button("🔍 Run Prior Authorization Review", type="primary", use_container_width=True)

    st.markdown("<p style='color:#475569;font-size:11px;text-align:center;margin-top:16px;'>LangGraph · Groq LLaMA3 · RAG · Streamlit</p>", unsafe_allow_html=True)

with right:
    if run_button:
        if not case_text.strip():
            st.warning("Please enter or select a patient case first.")
        else:
            with st.spinner("Agent is reviewing the case..."):
                try:
                    result = run_agent(case_text)

                    st.markdown(f"""
                    <div class="step-card">
                        <div class="sh1"><div class="snum">1</div><span style="font-size:18px">🔬</span><div class="stitle">Extracted Clinical Facts</div></div>
                        <div class="sbody">{result['extracted_facts']}</div>
                    </div>""", unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="step-card">
                        <div class="sh2"><div class="snum">2</div><span style="font-size:18px">📋</span><div class="stitle">Retrieved Policy Document (RAG)</div></div>
                        <div class="sbody">{result['retrieved_policy']}</div>
                    </div>""", unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="step-card">
                        <div class="sh3"><div class="snum">3</div><span style="font-size:18px">⚖️</span><div class="stitle">Policy-Grounded Criteria Analysis</div></div>
                        <div class="sbody">{result['criteria_check']}</div>
                    </div>""", unsafe_allow_html=True)

                    decision_text = result["decision"]
                    if "APPROVED" in decision_text:
                        cls, dv, db, icon = "approved", "dv-a", "db-a", "✅ APPROVED"
                    elif "DENIED" in decision_text:
                        cls, dv, db, icon = "denied", "dv-d", "db-d", "❌ DENIED"
                    else:
                        cls, dv, db, icon = "pending", "dv-p", "db-p", "⏳ PENDING — MORE INFO NEEDED"

                    st.markdown(f"""
                    <div class="dec-{cls}">
                        <div class="dec-label">⚡ Final Decision</div>
                        <div class="{dv}">{icon}</div>
                        <div class="{db}">{decision_text}</div>
                    </div>""", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")
    else:
        st.markdown("""
        <div style="text-align:center;color:#94a3b8;padding:120px 20px;">
            <div style="font-size:52px;margin-bottom:16px;">🔍</div>
            <div style="font-size:16px;font-weight:600;color:#475569;margin-bottom:8px;">Ready to review</div>
            <div style="font-size:14px;color:#94a3b8;">Select a sample case on the left<br>and click <b>Run Prior Authorization Review</b>.</div>
        </div>""", unsafe_allow_html=True)