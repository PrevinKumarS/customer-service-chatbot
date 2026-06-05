## Plan: AI Bank Customer Service Chatbot

TL;DR - Define a Python Streamlit chatbot project that routes banking intents, triages complaints, and demonstrates prompt engineering, few-shot learning, chain-of-thought reasoning, structured JSON outputs, and guardrails. Clarify provider, knowledgebase format, intent categories, and evaluation expectations before implementation.

---

### 1. Clarification Phase
Ask one question at a time before making assumptions:
- Do you want a specific LLM provider/API (OpenAI, Azure, local model, etc.)?
- Should the knowledgebase be loaded from local JSON files directly or incorporated indirectly through prompt context?
- Which banking intent categories must be covered beyond standard examples? (e.g., account inquiry, transaction dispute, fraud report)
- Do you want the evaluation report as a single file, and should it include exact query responses or just summary metrics?

---

### 2. Project Structure
Create a simple project layout:
- `app.py` — Streamlit UI and app orchestration
- `chatbot.py` — prompt engineering, model calls, KB loading, and reasoning flow
- `guards.py` — input guardrails, PII/off-topic/prompt injection checks
- `schema.py` — Pydantic structured response models and validation
- `knowledgebase/` — folder with multiple JSON files for AI Bank customer service and complaint resolution data
- `requirements.txt` — Python dependencies
- `Readme.txt` — setup and run instructions
- `evaluation_report.txt` — 20-query test report and findings

---

### 3. Prompt Engineering & Few-Shot Learning
Implement:
- A system prompt that defines the assistant role, response style, output formatting, and safety guardrails
- Few-shot examples for at least 3 banking intents in the prompt
- Instructions to use chain-of-thought reasoning for complex queries so the model reasons internally before answering
- Explicit decline behavior for out-of-scope questions

---

### 4. Knowledgebase
Build `knowledgebase/` with JSON files covering:
- account types and services
- complaint resolution steps
- escalation policies
- customer service contact and process
The app should load these files and include relevant KB content in the prompt or retrieval flow.

---

### 5. Structured JSON Output
Implement:
- A Pydantic schema for internal structured output, e.g. `intent`, `confidence`, `action`, `resolution`, `escalation_required`, `notes`
- Validation of the model’s structured response with Pydantic
- Human-readable response display in the chatbot while preserving validated JSON internally

---

### 6. Guardrails
Implement input filtering:
- PII detection for emails, phone numbers, account numbers
- Off-topic detection for non-banking or irrelevant queries
- Prompt injection defense to reject malicious prompt-like content
If triggered, respond politely with a decline message.

---

### 7. Streamlit UI
Build a simple UI with:
- Header and assistant description
- User input text box and submit button
- Chat history display
- Optional debug panel for the validated JSON output
- Sidebar or note section describing scope and safety behavior

---

### 8. Dependencies & Documentation
Create:
- `requirements.txt` with Streamlit, Pydantic, and chosen LLM client library
- `Readme.txt` with:
  - Python version
  - virtual environment creation
  - dependency install
  - running `streamlit run app.py`
  - API key placement and configuration

---

### 9. Evaluation Report
Prepare `evaluation_report.txt` with:
- 20 test queries
- classification of results by category
- accuracy assessment
- formatting validation
- guardrail effectiveness
- notes on any failures or edge cases

---

### Verification
1. Confirm Streamlit app launches successfully.
2. Validate at least 3 banking intents and see both friendly response and structured JSON.
3. Test guardrails with PII, off-topic, and injection inputs.
4. Check dependency install and README instructions.
5. Verify the evaluation report documents 20 queries and outcomes.

---

### Notes
- This plan intentionally avoids assumptions and includes a step to ask clarification questions first.
- If you want, I can now ask the first clarification question about the LLM provider.
