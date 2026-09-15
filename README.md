# 🤖 Responsible AI Student Lab

> **A beginner-friendly Responsible AI lab project for 2nd/3rd-year B.Tech students.**  
> Built with **Python**, **Streamlit**, **LangChain**, **LangGraph**, and **Groq**.

Students do **not** need to build this AI system from scratch. The application is ready to run immediately. Students focus on experimenting with system prompts, testing AI limitations (hallucination, bias, privacy), verifying factual accuracy, and documenting responsible AI principles.

---

## 🏗️ Architecture

```text
                STREAMLIT UI
                     │
                     ▼
              User Question
                     │
                     ▼
                 LangGraph
                     │
                     ▼
       System Prompt (group_XX_prompt.py)
                     │
                     ▼
             LangChain + Groq LLM
                     │
                     ▼
                AI Response
                     │
                     ▼
        Simple Verification Inspection
                     │
                     ▼
              Response to UI
```

---

## 📁 Repository Structure

```text
Week_9/
├── app.py                     # Streamlit frontend UI
├── requirements.txt           # Project dependencies
├── .env.example               # Example environment variables template
├── .env                       # Local API key configuration (gitignored)
├── .gitignore                 # Git ignore rules
├── README.md                  # Main project guide
│
├── services/
│   ├── __init__.py
│   └── llm_service.py         # Groq client & dynamic prompt loader
│
├── graph/
│   ├── __init__.py
│   ├── state.py               # LangGraph AgentState definition
│   └── workflow.py            # LangGraph workflow (generation + verification)
│
└── student_task/
    ├── README.md              # Detailed student guide & 9 lab tasks
    ├── TEACHER_CHECKLIST.md   # Instructor grading & evaluation checklist
    │
    ├── prompts/               # Group-specific prompt files (Groups 01 to 08)
    │   ├── group_01_prompt.py
    │   ├── group_02_prompt.py
    │   ├── group_03_prompt.py
    │   ├── group_04_prompt.py
    │   ├── group_05_prompt.py
    │   ├── group_06_prompt.py
    │   ├── group_07_prompt.py
    │   └── group_08_prompt.py
    │
    └── submissions/           # Group submission reports
        ├── group_01/RESPONSIBLE_AI.md
        ├── group_02/RESPONSIBLE_AI.md
        ├── group_03/RESPONSIBLE_AI.md
        ├── group_04/RESPONSIBLE_AI.md
        ├── group_05/RESPONSIBLE_AI.md
        ├── group_06/RESPONSIBLE_AI.md
        ├── group_07/RESPONSIBLE_AI.md
        └── group_08/RESPONSIBLE_AI.md
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python **3.10** or higher installed.
- Git installed.

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell / Command Prompt):**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the example file to `.env`:
```bash
cp .env.example .env
```
Open `.env` and set your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```
*(Get your free Groq API key from [console.groq.com](https://console.groq.com/keys)).*

---

## 🚀 Running the Application

### Option A: Launch with CLI Group Flag (Recommended)
Run the application specifying your assigned group number (`01` through `08`):
```bash
streamlit run app.py -- --group 01
```

### Option B: Launch and Select Group via UI
Run without arguments and select your group from the sidebar dropdown:
```bash
streamlit run app.py
```

---

## 🧑‍🎓 Student Instructions

1. **Locate your assigned files**:
   - Prompt file: `student_task/prompts/group_XX_prompt.py`
   - Lab report: `student_task/submissions/group_XX/RESPONSIBLE_AI.md`
2. **Read the student guide**: Open [`student_task/README.md`](student_task/README.md) for full instructions on the 9 tasks:
   - **Task 1**: Prompt Improvement (Role, Goal, Audience, Instructions, Constraints)
   - **Task 2**: Hallucination Testing
   - **Task 3**: Bias Testing
   - **Task 4**: Privacy & Sensitive Data Safeguards
   - **Task 5**: Fact Verification with External Sources
   - **Task 6**: Copyright & Academic Integrity
   - **Task 7**: AI Regulations (India, EU, US)
   - **Task 8**: Jobs, Automation & Upskilling
   - **Task 9**: Emerging AI Technologies
   - **Task 10**: Formulate 3 Responsible AI Rules
3. **Commit your work**:
   ```bash
   git add student_task/prompts/group_XX_prompt.py student_task/submissions/group_XX/RESPONSIBLE_AI.md
   git commit -m "Group XX Responsible AI Lab Submission"
   git push origin main
   ```
   *Do NOT modify `app.py`, `graph/`, `services/`, or `.env`.*

---

## 👨‍🏫 Teacher Instructions

1. Direct students to [`student_task/README.md`](student_task/README.md).
2. Assign student teams to Groups `01` through `08`.
3. Evaluate student submissions using the standardized criteria in [`student_task/TEACHER_CHECKLIST.md`](student_task/TEACHER_CHECKLIST.md).
4. Verify each group's improved prompt by switching to their group in the Streamlit UI or running:
   ```bash
   streamlit run app.py -- --group XX
   ```

---

## 🔒 Security & Privacy Rules

- **Never commit `.env` or API keys** to GitHub.
- `.gitignore` is pre-configured to ignore `.env`, virtual environments, and caches.
- The UI never exposes API keys or internal secrets to students.
