"""
LLM and Group Prompt Loading Service
Handles ChatGroq initialization and dynamic group prompt discovery.
"""

import os
import sys
import importlib
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env
load_dotenv()

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
VALID_GROUPS = [f"{i:02d}" for i in range(1, 9)]  # ['01', '02', ..., '08']


def get_api_key() -> Optional[str]:
    """Retrieve the Groq API key from environment variables."""
    key = os.getenv("GROQ_API_KEY", "").strip()
    return key if key else None


def get_llm(model_name: Optional[str] = None, temperature: float = 0.3) -> ChatGroq:
    """
    Initialize and return a ChatGroq client.
    Raises ValueError if the API key is not configured.
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "Groq API key is not configured.\n"
            "Please create a .env file and add your GROQ_API_KEY."
        )
    
    model = model_name or os.getenv("GROQ_MODEL", DEFAULT_MODEL)
    return ChatGroq(
        model=model,
        groq_api_key=api_key,
        temperature=temperature,
    )


def load_group_prompt(group_id: str) -> Dict[str, Any]:
    """
    Dynamically loads the prompt file for a specified group.
    Supports live reloads so edits in group_XX_prompt.py take effect immediately.
    """
    # Normalize group id (e.g. '1' -> '01')
    try:
        clean_id = f"{int(group_id):02d}"
    except (ValueError, TypeError):
        clean_id = "01"

    if clean_id not in VALID_GROUPS:
        clean_id = "01"

    module_name = f"student_task.prompts.group_{clean_id}_prompt"
    prompt_file_rel = f"student_task/prompts/group_{clean_id}_prompt.py"

    default_system_prompt = (
        "You are a helpful AI assistant.\n"
        "Answer the user's question clearly and helpfully."
    )
    default_version = "1.0"

    try:
        # Check if already imported to force reload latest student edits
        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)

        system_prompt = getattr(module, "SYSTEM_PROMPT", default_system_prompt)
        prompt_version = str(getattr(module, "PROMPT_VERSION", default_version))

        return {
            "group_id": clean_id,
            "system_prompt": system_prompt.strip(),
            "prompt_version": prompt_version,
            "prompt_file": prompt_file_rel,
            "error": None,
        }
    except Exception as e:
        return {
            "group_id": clean_id,
            "system_prompt": default_system_prompt,
            "prompt_version": default_version,
            "prompt_file": prompt_file_rel,
            "error": f"Could not load prompt for group {clean_id}: {str(e)}",
        }
