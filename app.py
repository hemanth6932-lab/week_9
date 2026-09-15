"""
Responsible AI Assistant - Student Lab Application
Streamlit Frontend for B.Tech Responsible AI Lab.
"""

import sys
import argparse
import streamlit as st
from services.llm_service import load_group_prompt, get_api_key, VALID_GROUPS
from graph.workflow import ai_graph

# Page configuration
st.set_page_config(
    page_title="Responsible AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom styling for a clean, professional, beginner-friendly UI
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 1rem;
    }
    .badge-container {
        display: flex;
        gap: 0.6rem;
        margin-bottom: 1.2rem;
    }
    .status-badge {
        background-color: #E2E8F0;
        color: #0F172A;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .status-badge-accent {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .verification-box {
        background-color: #F8FAFC;
        border-left: 3px solid #3B82F6;
        padding: 0.6rem 0.8rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.85rem;
        color: #334155;
        margin-top: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def parse_cli_group() -> str:
    """Parses --group argument from CLI if provided (e.g. streamlit run app.py -- --group 01)."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--group", "-g", type=str, default=None)
    try:
        # sys.argv contains args passed after '--'
        args, _ = parser.parse_known_args(sys.argv[1:])
        if args.group:
            clean = f"{int(args.group):02d}"
            if clean in VALID_GROUPS:
                return clean
    except Exception:
        pass
    return "01"


# Initialize Session State
if "selected_group" not in st.session_state:
    st.session_state.selected_group = parse_cli_group()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "verification_notes" not in st.session_state:
    st.session_state.verification_notes = {}


# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Group & Lab Settings")

    # Group Selection
    group_idx = VALID_GROUPS.index(st.session_state.selected_group) if st.session_state.selected_group in VALID_GROUPS else 0
    selected = st.selectbox(
        "Select Your Group:",
        options=VALID_GROUPS,
        index=group_idx,
        format_func=lambda x: f"Group {x}",
        help="Select the group number assigned to your team.",
    )
    
    # If group changed, update session state
    if selected != st.session_state.selected_group:
        st.session_state.selected_group = selected
        st.rerun()

    # Load active prompt details
    prompt_data = load_group_prompt(st.session_state.selected_group)

    st.markdown(f"**Assigned File:** `{prompt_data['prompt_file']}`")
    st.markdown(f"**Prompt Version:** `{prompt_data['prompt_version']}`")

    if st.button("🔄 Reload Group Prompt", use_container_width=True):
        st.success(f"Prompt reloaded for Group {st.session_state.selected_group}!")
        st.rerun()

    st.divider()

    # Clear Chat Button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.verification_notes = {}
        st.rerun()

    st.divider()

    # Lab Tasks Overview
    st.subheader("📋 Lab Tasks Overview")
    st.markdown(
        """
        1. **Prompt Improvement** (Role, Goal, Audience, Rules)
        2. **Hallucination Test** (Future/unanswerable facts)
        3. **Bias Test** (Fairness & candidate evaluation)
        4. **Privacy Test** (Handling sensitive credentials)
        5. **Fact Verification** (External source check)
        6. **Copyright & Ethics** (Rewriting & plagiarism)
        7. **AI Regulation** (India, EU, US governance)
        8. **Jobs & Upskilling** (Automation vs human skills)
        9. **Emerging AI** (Multimodal, Agents, RAG)
        10. **3 Responsible AI Rules**
        """
    )

    st.divider()

    # Collapsible Learning Guide
    with st.expander("📘 What are we learning?"):
        st.markdown(
            """
            - **Prompting**: How instructions, constraints, and roles change AI behaviour.
            - **Hallucination**: AI can generate convincing but factually incorrect statements.
            - **Bias**: AI can produce unfair, skewed, or stereotyped outcomes if unguided.
            - **Privacy**: Never share passwords, OTPs, or confidential information with AI.
            - **Verification**: Always cross-check critical AI claims against reliable sources.
            - **Copyright**: Rephrasing content does not automatically confer originality.
            """
        )


# --- MAIN AREA ---

# Header & Subtitle
st.markdown('<div class="main-header">🤖 Responsible AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Prompt Improvement Challenge</div>', unsafe_allow_html=True)

# Status Badges
st.markdown(
    f"""
    <div class="badge-container">
        <span class="status-badge">👥 Group: {st.session_state.selected_group}</span>
        <span class="status-badge-accent">🏷️ Prompt Version: {prompt_data['prompt_version']}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Expandable Prompt Information (educational, no secret exposure)
with st.expander("▼ Prompt Information"):
    st.markdown(
        f"""
        You are currently using the prompt assigned to **Group {st.session_state.selected_group}**.

        Students can modify their system prompt in:  
        `{prompt_data['prompt_file']}`

        *After editing your prompt file, click **Reload Group Prompt** in the sidebar to test your improvements!*
        """
    )

# Check API Key availability
api_key = get_api_key()
if not api_key:
    st.warning(
        "⚠️ **Groq API key is not configured.**\n\n"
        "Please create a `.env` file in the project root directory and add your `GROQ_API_KEY`.\n\n"
        "Example:\n```env\nGROQ_API_KEY=your_api_key_here\n```"
    )

# Display Chat History
for idx, message in enumerate(st.session_state.messages):
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(content)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(content)
            # Show verification note if recorded
            if idx in st.session_state.verification_notes:
                st.markdown(
                    f'<div class="verification-box">🔍 <b>Inspection:</b> {st.session_state.verification_notes[idx]}</div>',
                    unsafe_allow_html=True,
                )

# Chat Input & AI Graph Invocation
if prompt := st.chat_input("Ask your question..."):
    if not api_key:
        st.error("Please configure your GROQ_API_KEY in the `.env` file to start chatting.")
    else:
        # Append and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Prepare state for LangGraph workflow
        current_state = {
            "messages": st.session_state.messages,
            "group_id": st.session_state.selected_group,
            "system_prompt": prompt_data["system_prompt"],
            "prompt_version": prompt_data["prompt_version"],
            "response": "",
            "verification_note": None,
        }

        # Invoke workflow with spinner
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                try:
                    result = ai_graph.invoke(current_state)
                    ai_reply = result.get("response", "No response generated.")
                    verif_note = result.get("verification_note")

                    st.markdown(ai_reply)
                    if verif_note:
                        st.markdown(
                            f'<div class="verification-box">🔍 <b>Inspection:</b> {verif_note}</div>',
                            unsafe_allow_html=True,
                        )

                    # Save to chat history
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                    msg_idx = len(st.session_state.messages) - 1
                    if verif_note:
                        st.session_state.verification_notes[msg_idx] = verif_note

                except Exception as e:
                    error_msg = str(e)
                    # Friendly error handling without exposing credentials
                    if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                        st.error("Authentication failed. Please verify that your GROQ_API_KEY in `.env` is valid.")
                    elif "rate_limit" in error_msg.lower() or "429" in error_msg:
                        st.error("Rate limit reached. Please wait a few moments before sending another message.")
                    else:
                        st.error(f"An error occurred while generating the response: {error_msg}")
