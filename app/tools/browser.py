# ============================================
# BROWSER - Playwright browser management
# ============================================
from playwright.sync_api import sync_playwright
from app.config import HEADLESS

# Global variables
_playwright = None
_browser = None
_context = None
page = None


def init_browser():
    """
    Start browser if not already started.
    Called automatically when needed.
    """
    global _playwright, _browser, _context, page

    if page is not None:
        return page  # Already running

    print("🌐 Starting browser...")

    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch(headless=HEADLESS)
    _context = _browser.new_context()
    page = _context.new_page()

    print("✅ Browser ready!")
    return page


def close_browser():
    """
    Close browser and cleanup.
    Called at end of each task.
    """
    global _playwright, _browser, _context, page

    try:
        if _browser:
            _browser.close()
            print("🔒 Browser closed")
        if _playwright:
            _playwright.stop()
    except Exception as e:
        print(f"⚠️ Browser close error: {e}")
    finally:
        _playwright = None
        _browser = None
        _context = None
        page = None