# main.py ← ROOT FOLDER
import warnings
import os
import sys

warnings.filterwarnings("ignore")

# ── Load .env file FIRST before anything else ──
from dotenv import load_dotenv
load_dotenv()  # ← Reads .env file automatically

# ── Verify token loaded ──
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    print(f"✅ HF Token loaded: {hf_token[:8]}...")
else:
    print("⚠️ HF Token not found in .env")

# ── Suppress other warnings ──
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

# ── Add ROOT to Python path ──
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.agent.agent import run_agent


if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AI Browser Automation Agent")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("  1. Run a task")
        print("  2. View task history")
        print("  3. View success stats")
        print("  4. Exit")

        choice = input("\nChoice (1-4): ").strip()

        if choice == "1":
            user_input = input("\nEnter your task: ").strip()
            if user_input:
                run_agent(user_input)
            else:
                print("❌ Please enter a task")

        elif choice == "2":
            from app.database.json_db import get_task_history
            history = get_task_history(limit=5)
            if history:
                print("\n📋 Last 5 Tasks:")
                for i, task in enumerate(history, 1):
                    print(
                        f"  {i}. [{task['status']}] "
                        f"{task['task']} - "
                        f"{task['timestamp']}"
                    )
            else:
                print("  No history yet")

        elif choice == "3":
            from app.database.json_db import get_success_rate
            stats = get_success_rate()
            print(f"\n📊 Stats:")
            print(f"   Total Runs   : {stats.get('total_runs', 0)}")
            print(f"   Successful   : {stats.get('successful_runs', 0)}")
            print(f"   Success Rate : {stats.get('success_rate', '0%')}")

        elif choice == "4":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice")