# app/training/data_preparer.py
# ============================================
# PREPARES AND CLEANS TRAINING DATA
# ============================================
import warnings
warnings.filterwarnings("ignore")

import json
import os


def load_jsonl(filepath: str) -> list:
    """Load JSONL file into list."""
    data = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def validate_training_data(filepath: str) -> dict:
    """
    Check training data quality.
    Returns report of good/bad examples.
    """
    print(f"🔍 Validating: {filepath}")
    data = load_jsonl(filepath)

    good = 0
    bad = 0
    issues = []

    for i, item in enumerate(data):
        # Check has messages
        if "messages" not in item:
            bad += 1
            issues.append(f"Item {i}: Missing 'messages'")
            continue

        messages = item["messages"]

        # Check has 3 messages (system, user, assistant)
        if len(messages) != 3:
            bad += 1
            issues.append(f"Item {i}: Wrong message count {len(messages)}")
            continue

        # Check assistant response is valid JSON
        assistant_msg = messages[2].get("content", "")
        try:
            steps = json.loads(assistant_msg)
            if isinstance(steps, list) and len(steps) > 0:
                good += 1
            else:
                bad += 1
                issues.append(f"Item {i}: Empty steps list")
        except json.JSONDecodeError:
            bad += 1
            issues.append(f"Item {i}: Invalid JSON in response")

    report = {
        "total": len(data),
        "good": good,
        "bad": bad,
        "quality": f"{(good/len(data)*100):.0f}%" if data else "0%",
        "issues": issues
    }

    print(f"\n📊 Validation Report:")
    print(f"   Total   : {report['total']}")
    print(f"   Good    : {report['good']}")
    print(f"   Bad     : {report['bad']}")
    print(f"   Quality : {report['quality']}")

    if issues:
        print(f"\n⚠️ Issues found:")
        for issue in issues[:5]:
            print(f"   - {issue}")

    return report


def clean_training_data(filepath: str) -> str:
    """
    Remove bad examples from training data.
    Returns path to cleaned file.
    """
    print(f"🧹 Cleaning: {filepath}")
    data = load_jsonl(filepath)

    clean_data = []
    removed = 0

    for item in data:
        try:
            messages = item.get("messages", [])
            if len(messages) == 3:
                assistant_msg = messages[2].get("content", "")
                steps = json.loads(assistant_msg)
                if isinstance(steps, list) and len(steps) > 0:
                    clean_data.append(item)
                else:
                    removed += 1
        except:
            removed += 1

    # Save cleaned data
    clean_path = filepath.replace(".jsonl", "_clean.jsonl")
    with open(clean_path, "w") as f:
        for item in clean_data:
            f.write(json.dumps(item) + "\n")

    print(f"✅ Cleaned file saved: {clean_path}")
    print(f"   Kept    : {len(clean_data)}")
    print(f"   Removed : {removed}")

    return clean_path


def show_training_examples(filepath: str, count: int = 3):
    """
    Show sample training examples.
    """
    data = load_jsonl(filepath)

    print(f"\n📝 Sample Training Examples ({min(count, len(data))}):")
    print("=" * 50)

    for i, item in enumerate(data[:count]):
        messages = item.get("messages", [])
        print(f"\nExample {i+1}:")
        print(f"  User   : {messages[1]['content'][-100:]}...")
        print(f"  Agent  : {messages[2]['content']}")
        print("-" * 50)