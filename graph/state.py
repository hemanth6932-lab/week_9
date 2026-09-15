"""
Agent State Definition for LangGraph Workflow.
"""

from typing import TypedDict, List, Dict, Optional, Any


class AgentState(TypedDict):
    """
    Represents the state of the Responsible AI Assistant graph.
    """
    messages: List[Dict[str, str]]
    group_id: str
    system_prompt: str
    prompt_version: str
    response: str
    verification_note: Optional[str]
