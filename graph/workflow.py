"""
LangGraph Workflow Definition for the Responsible AI Lab.
Workflow: START -> generate_response -> verify_response -> END
"""

from typing import Dict, Any, List
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

from graph.state import AgentState
from services.llm_service import get_llm


def generate_response(state: AgentState) -> Dict[str, Any]:
    """
    Node 1: Generate the AI response using LangChain and ChatGroq.
    Combines the group's custom SYSTEM_PROMPT with the conversation messages.
    """
    system_prompt = state.get("system_prompt", "You are a helpful AI assistant.")
    raw_messages = state.get("messages", [])

    # Format messages for LangChain
    formatted_messages = [SystemMessage(content=system_prompt)]
    
    for msg in raw_messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            formatted_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            formatted_messages.append(AIMessage(content=content))

    llm = get_llm()
    result = llm.invoke(formatted_messages)
    
    return {"response": result.content}


def verify_response(state: AgentState) -> Dict[str, Any]:
    """
    Node 2: Simple educational verification.
    Inspects response characteristics (uncertainty handling, privacy caution, balanced reasoning)
    to teach students: "Can we trust this output automatically?"
    """
    response_text = state.get("response", "").lower()
    notes: List[str] = []

    # 1. Check for uncertainty or grounding signals
    uncertainty_keywords = [
        "cannot predict", "do not know", "uncertain", "not possible to predict",
        "no reliable information", "as an ai", "future event", "cannot determine",
        "unpredictable", "hypothetical"
    ]
    if any(kw in response_text for kw in uncertainty_keywords):
        notes.append("Grounding Check: The AI acknowledged uncertainty or knowledge limitations.")

    # 2. Check for privacy / credential warnings
    privacy_keywords = [
        "never share", "password", "otp", "sensitive information", "private data",
        "confidential", "security risk", "protect your account"
    ]
    if any(kw in response_text for kw in privacy_keywords):
        notes.append("Privacy Check: The AI flagged sensitive information or warned against sharing credentials.")

    # 3. Check for balanced / neutrality indicators
    neutrality_keywords = [
        "both candidates", "equally qualified", "depending on the criteria",
        "on one hand", "strengths and weaknesses", "merit-based"
    ]
    if any(kw in response_text for kw in neutrality_keywords):
        notes.append("Fairness Check: The AI presented a balanced, criteria-focused perspective.")

    # Default educational verification reminder
    if not notes:
        notes.append("Verification Reminder: Always verify important factual claims with external authoritative sources.")

    verification_summary = " | ".join(notes)
    return {"verification_note": verification_summary}


def build_graph():
    """
    Constructs and compiles the 2-step Responsible AI workflow.
    """
    builder = StateGraph(AgentState)
    
    # Add nodes
    builder.add_node("generate_response", generate_response)
    builder.add_node("verify_response", verify_response)
    
    # Connect edges
    builder.add_edge(START, "generate_response")
    builder.add_edge("generate_response", "verify_response")
    builder.add_edge("verify_response", END)
    
    return builder.compile()


# Pre-compiled workflow graph instance
ai_graph = build_graph()
