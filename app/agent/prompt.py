# ============================================
# PROMPT BUILDER
# ============================================
# Note: Main prompting now done in llm.py via LangChain
# This file kept for any extra prompt utilities

def build_prompt(user_input: str, context: str = "", history: str = "") -> str:
    """
    Simple prompt builder (backup - main one is in llm.py)
    """
    return f"""
You are an AI browser automation agent.

PAST EXPERIENCE:
{context if context else "None"}

RECENT ACTIONS:
{history if history else "None"}

SUPPORTED ACTIONS:
- open_url   : {{"action": "open_url", "value": "https://..."}}
- type       : {{"action": "type", "selector": "css_selector", "value": "text"}}
- click      : {{"action": "click", "selector": "css_selector"}}
- wait       : {{"action": "wait", "value": 2000}}
- screenshot : {{"action": "screenshot", "value": "filename.png"}}

RULES:
- Return ONLY valid JSON array
- No explanation, No markdown

Task: {user_input}

JSON Output:
"""