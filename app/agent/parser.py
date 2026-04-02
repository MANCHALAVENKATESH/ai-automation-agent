# app/agent/parser.py
import json
import re


def extract_json(text: str) -> str:
    """
    Extract JSON array from LLM response text.
    Handles all cases - single line, multi line, with/without markdown
    """
    if not text or not text.strip():
        print("❌ Empty response from LLM")
        return ""

    text = text.strip()

    # ── Case 1: Has ```json ... ``` block ──
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # ── Case 2: Has ``` ... ``` block ──
    match = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # ── Case 3: Find [ ... ] anywhere in text ──
    # Find first [ and last ]
    start = text.find("[")
    end = text.rfind("]")

    if start != -1 and end != -1 and end > start:
        return text[start:end + 1].strip()

    # ── Case 4: Return as is ──
    return text.strip()


def fix_json(text: str) -> str:
    """
    Fix common JSON mistakes from LLM.
    """
    if not text:
        return ""

    text = text.strip()

    # Fix missing closing bracket
    if text.startswith("[") and not text.endswith("]"):
        text += "]"

    # Fix trailing commas before ]
    # Example: [{"a": "b"},] → [{"a": "b"}]
    text = re.sub(r",\s*\]", "]", text)

    # Fix trailing commas before }
    # Example: {"a": "b",} → {"a": "b"}
    text = re.sub(r",\s*\}", "}", text)

    return text


def validate_step(step: dict) -> bool:
    """
    Check if a step has required fields.
    """
    if not isinstance(step, dict):
        return False

    action = step.get("action")
    if not action:
        return False

    # Check required fields per action type
    if action == "open_url":
        if not step.get("value"):
            print(f"⚠️ open_url missing 'value'")
            return False

    elif action == "type":
        if not step.get("selector"):
            print(f"⚠️ type missing 'selector'")
            return False
        if step.get("value") is None:
            print(f"⚠️ type missing 'value'")
            return False

    elif action == "click":
        if not step.get("selector"):
            print(f"⚠️ click missing 'selector'")
            return False

    elif action == "screenshot":
        # value is optional - defaults to screenshot.png
        pass

    elif action == "wait":
        # value is optional - defaults to 1000ms
        pass

    return True


def parse_steps(response_text: str) -> list:
    """
    Convert LLM response text into list of steps.

    Input:
    '[{"action": "open_url", "value": "https://google.com"}]'

    Output:
    [{"action": "open_url", "value": "https://google.com"}]
    """

    # ── Guard: empty response ──
    if not response_text or not response_text.strip():
        print("❌ Empty response from LLM")
        return []

    print(f"\n🔍 Raw LLM text:\n{response_text}")

    # ── Step 1: Extract JSON ──
    extracted = extract_json(response_text)
    print(f"\n🔍 Extracted JSON:\n{extracted}")

    if not extracted:
        print("❌ Could not extract JSON")
        return []

    # ── Step 2: Fix JSON ──
    fixed = fix_json(extracted)
    print(f"\n🔍 Fixed JSON:\n{fixed}")

    if not fixed:
        print("❌ JSON is empty after fixing")
        return []

    # ── Step 3: Parse JSON ──
    try:
        steps = json.loads(fixed)

        # Must be a list
        if not isinstance(steps, list):
            print("❌ JSON is not a list/array")
            return []

        # Must have items
        if len(steps) == 0:
            print("❌ Empty steps list")
            return []

        # ── Step 4: Validate each step ──
        valid_steps = []
        for i, step in enumerate(steps):
            if validate_step(step):
                valid_steps.append(step)
                print(f"✅ Step {i+1} valid: {step}")
            else:
                print(f"⚠️ Step {i+1} invalid - skipped: {step}")

        return valid_steps

    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print(f"   At position: {e.pos}")
        print(f"   Text was: {fixed}")
        return []