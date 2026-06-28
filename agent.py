import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from policies import retrieve_policy

load_dotenv()

# ── State 
class AuthState(TypedDict):
    patient_case: str
    extracted_facts: str
    retrieved_policy: str
    criteria_check: str
    decision: str

# ── LLM 
def get_llm():
    return ChatGroq(
        model="qwen/qwen3-32b",
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0,
        model_kwargs={"thinking": {"type": "disabled"}},
    )

# ── Node 1: Extract clinical facts 
def extract_facts(state: AuthState) -> AuthState:
    llm = get_llm()
    prompt = f"""Extract key facts from this patient case. Be concise — bullet points only, no explanation.
Include: age, diagnosis, requested treatment, clinical history, physician documentation status, patient education status, comorbidities.
If the case says physician documented medical necessity — list it. If patient completed education — list it.

Patient Case:
{state['patient_case']}"""
    response = llm.invoke(prompt)
    return {**state, "extracted_facts": response.content}

# ── Node 2: Retrieve relevant policy (RAG) 
def retrieve_relevant_policy(state: AuthState) -> AuthState:
    policy_text = retrieve_policy(state["extracted_facts"])
    return {**state, "retrieved_policy": policy_text}

# ── Node 3: Check against retrieved policy criteria 
def check_criteria(state: AuthState) -> AuthState:
    llm = get_llm()
    prompt = f"""You are a prior authorization specialist. Evaluate each policy criterion below against the clinical facts.
For each criterion write ONE line: "Criterion X: MET / NOT MET / INSUFFICIENT INFORMATION — [one sentence reason]"
Cite the policy clause. Be brief and direct. No preamble.

POLICY:
{state['retrieved_policy']}

CLINICAL FACTS:
{state['extracted_facts']}"""
    response = llm.invoke(prompt)
    return {**state, "criteria_check": response.content}

# ── Node 4: Generate final decision 
def generate_decision(state: AuthState) -> AuthState:
    llm = get_llm()
    prompt = f"""You are a senior prior authorization reviewer. Make a final decision. Be concise.

Criteria Analysis:
{state['criteria_check']}

Respond in this exact format only — no extra text:

DECISION: [APPROVED / DENIED / PENDING - MORE INFO NEEDED]

JUSTIFICATION:
[2-3 sentences max. Reference the policy and key criteria.]

RECOMMENDED NEXT STEPS:
[2-3 bullet points max]"""
    response = llm.invoke(prompt)
    return {**state, "decision": response.content}

# ── Build the graph 
def build_agent():
    graph = StateGraph(AuthState)
    graph.add_node("extract_facts", extract_facts)
    graph.add_node("retrieve_policy", retrieve_relevant_policy)
    graph.add_node("check_criteria", check_criteria)
    graph.add_node("generate_decision", generate_decision)
    graph.set_entry_point("extract_facts")
    graph.add_edge("extract_facts", "retrieve_policy")
    graph.add_edge("retrieve_policy", "check_criteria")
    graph.add_edge("check_criteria", "generate_decision")
    graph.add_edge("generate_decision", END)
    return graph.compile()

# ── Run 
def run_agent(patient_case: str) -> dict:
    agent = build_agent()
    result = agent.invoke({"patient_case": patient_case})
    return {
        "extracted_facts": result["extracted_facts"],
        "retrieved_policy": result["retrieved_policy"],
        "criteria_check": result["criteria_check"],
        "decision": result["decision"],
    }