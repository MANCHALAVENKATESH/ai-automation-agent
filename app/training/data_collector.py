# app/training/data_collector.py
# ============================================
# COLLECTS GOOD TASK DATA FOR FINE TUNING
# ============================================
import warnings
warnings.filterwarnings("ignore")

import os
import json
from datetime import datetime
from app.database.json_db import tasks_table

# Directory to save training data
TRAINING_DIR = "./data/training"
os.makedirs(TRAINING_DIR, exist_ok=True)


def collect_training_data():
    """
    Get all SUCCESSFUL tasks from JSON DB
    and convert to training format.

    Training Format:
    {
        "prompt": "User asked: Search Python on Google",
        "response": '[{"action": "open_url", ...}]'
    }
    """
    print("📦 Collecting training data...")

    # Get only successful tasks
    all_tasks = tasks_table.all()
    good_tasks = [
        t for t in all_tasks
        if t.get("status") == "success"
    ]

    print(f"✅ Found {len(good_tasks)} successful tasks")

    if not good_tasks:
        print("❌ No successful tasks yet!")
        print("   Run some tasks first, then collect data")
        return []

    # Convert to training format
    training_data = []

    for task in good_tasks:
        training_item = {
            "prompt": build_training_prompt(task["task"]),
            "response": json.dumps(task["steps"])
        }
        training_data.append(training_item)
        print(f"  ✅ Added: {task['task'][:50]}...")

    return training_data


def build_training_prompt(user_input: str) -> str:
    """
    Build the prompt format for training.
    Must match EXACTLY what agent uses.
    """
    return f"""You are an AI browser automation agent.

SUPPORTED ACTIONS:
- open_url   : {{"action": "open_url", "value": "https://..."}}
- type       : {{"action": "type", "selector": "css_selector", "value": "text"}}
- click      : {{"action": "click", "selector": "css_selector"}}
- wait       : {{"action": "wait", "value": 2000}}
- screenshot : {{"action": "screenshot", "value": "filename.png"}}

RULES:
- Return ONLY valid JSON array
- NO explanation
- NO markdown

Task: {user_input}

JSON Output:"""


def save_training_file():
    """
    Save training data to JSONL file.
    JSONL = one JSON object per line
    (Format required for fine tuning)
    """
    training_data = collect_training_data()

    if not training_data:
        return None

    # Save as JSONL file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{TRAINING_DIR}/training_{timestamp}.jsonl"

    with open(filename, "w") as f:
        for item in training_data:
            f.write(json.dumps(item) + "\n")

    print(f"\n✅ Training data saved to: {filename}")
    print(f"   Total examples: {len(training_data)}")
    return filename


def save_ollama_training_file():
    """
    Save in Ollama fine tuning format.
    """
    training_data = collect_training_data()

    if not training_data:
        return None

    # Ollama format
    ollama_data = []
    for item in training_data:
        ollama_data.append({
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI browser automation agent. Return ONLY valid JSON arrays of steps."
                },
                {
                    "role": "user",
                    "content": item["prompt"]
                },
                {
                    "role": "assistant",
                    "content": item["response"]
                }
            ]
        })

    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{TRAINING_DIR}/ollama_training_{timestamp}.jsonl"

    with open(filename, "w") as f:
        for item in ollama_data:
            f.write(json.dumps(item) + "\n")

    print(f"\n✅ Ollama training data saved: {filename}")
    print(f"   Total examples: {len(ollama_data)}")
    return filename