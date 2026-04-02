# ============================================
# LANGCHAIN - Updated for newer versions
# ============================================
from langchain_ollama import OllamaLLM          # ← NEW import
from langchain_core.prompts import PromptTemplate  # ← NEW import
from langchain_core.output_parsers import StrOutputParser  # ← NEW
from app.config import MODEL

# ---- Step 1: Connect to Ollama ----
llm = OllamaLLM(
    model=MODEL,
    temperature=0.1
)

# ---- Step 2: Prompt Template ----
prompt_template = PromptTemplate(
    input_variables=["user_input", "context", "history"],
    template="""
You are an AI browser automation agent.

PAST EXPERIENCE (use this to help):
{context}

RECENT ACTIONS TAKEN:
{history}

SUPPORTED ACTIONS (ONLY use these):
- open_url   : {{"action": "open_url", "value": "https://..."}}
- type       : {{"action": "type", "selector": "css_selector", "value": "text"}}
- click      : {{"action": "click", "selector": "css_selector"}}
- wait       : {{"action": "wait", "value": 2000}}
- screenshot : {{"action": "screenshot", "value": "filename.png"}}

STRICT RULES:
- Return ONLY valid JSON array
- NO explanation
- NO markdown
- ALWAYS close array with ]

Task: {user_input}

JSON Output:
"""
)

# ---- Step 3: Create Chain (New Way) ----
# Old way: LLMChain(llm=llm, prompt=prompt)   ❌ Deprecated
# New way: prompt | llm | parser               ✅ Current
output_parser = StrOutputParser()
chain = prompt_template | llm | output_parser


def ask_llm(user_input: str, context: str = "", history: str = "") -> str:
    """
    Send task to LLM and get steps back.
    """
    print("🤖 Sending to LLM...")

    try:
        response = chain.invoke({
            "user_input": user_input,
            "context": context if context else "No past experience yet",
            "history": history if history else "No recent actions"
        })
        return response

    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return ""