# ============================================
# UTILS - Helper functions
# ============================================
import os
import json
from datetime import datetime


def make_dirs():
    """Create all required directories."""
    dirs = ["./data", "./data/chroma_db", "./screenshots"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✅ Directories ready")


def timestamped_name(prefix: str, ext: str) -> str:
    """
    Create filename with timestamp.
    Example: screenshot_20240115_103000.png
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}.{ext}"


def pretty_print_steps(steps: list):
    """Print steps in readable format."""
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {json.dumps(step, indent=2)}")


def save_json(data: dict, filename: str):
    """Save dict to JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def load_json(filename: str) -> dict:
    """Load dict from JSON file."""
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)