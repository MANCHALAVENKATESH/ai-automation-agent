# ============================================
# ACTIONS - Execute each browser step
# ============================================
from app.tools.browser import init_browser

SUPPORTED_ACTIONS = {
    "open_url",
    "type",
    "click",
    "wait",
    "screenshot"
}


def execute_step(step: dict) -> bool:
    """
    Execute a single step.
    Returns True if success, False if failed.

    Example steps:
    {"action": "open_url", "value": "https://google.com"}
    {"action": "type", "selector": "#search", "value": "Python"}
    {"action": "click", "selector": "#submit"}
    """
    page = init_browser()
    action = step.get("action")

    if not action:
        print("⚠️ Step has no action")
        return False

    if action not in SUPPORTED_ACTIONS:
        print(f"⚠️ Unknown action: {action}")
        print(f"   Supported: {SUPPORTED_ACTIONS}")
        return False

    try:
        # ---- OPEN URL ----
        if action == "open_url":
            url = step.get("value")
            if not url:
                raise ValueError("Missing 'value' (url)")
            print(f"🌐 Opening: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # ---- TYPE TEXT ----
        elif action == "type":
            selector = step.get("selector")
            value = step.get("value", "")
            if not selector:
                raise ValueError("Missing 'selector'")
            print(f"⌨️ Typing '{value}' into '{selector}'")
            page.fill(selector, value, timeout=10000)

        # ---- CLICK ----
        elif action == "click":
            selector = step.get("selector")
            if not selector:
                raise ValueError("Missing 'selector'")
            print(f"🖱️ Clicking: {selector}")
            page.click(selector, timeout=10000)

        # ---- WAIT ----
        elif action == "wait":
            ms = int(step.get("value", 1000))
            print(f"⏳ Waiting {ms}ms")
            page.wait_for_timeout(ms)

        # ---- SCREENSHOT ----
        elif action == "screenshot":
            filename = step.get("value", "screenshot.png")
            print(f"📸 Screenshot -> {filename}")
            page.screenshot(path=filename)

        return True  # Success

    except Exception as e:
        print(f"❌ Action '{action}' failed!")
        print(f"   Step: {step}")
        print(f"   Error: {e}")
        return False  # Failed