# ============================================
# JSON DATABASE - TinyDB
# Stores task logs and history
# ============================================
import os
import json
from datetime import datetime
from tinydb import TinyDB, Query
from app.config import DB_PATH

# Create directory if not exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connect to JSON database
db = TinyDB(DB_PATH)

# Tables (like sheets in Excel)
tasks_table = db.table("tasks")  # All task runs
errors_table = db.table("errors")  # All errors
TaskQuery = Query()


def log_task(user_input: str, steps: list, results: list):
    """
    Save a task run to database.

    Creates record like:
    {
        "task": "Search Python on Google",
        "steps": [...],
        "results": [true, true, false],
        "success_count": 2,
        "total_steps": 3,
        "status": "partial",
        "timestamp": "2024-01-15 10:30:00"
    }
    """
    try:
        # Calculate success rate
        success_count = sum(results)
        total = len(results)

        if total == 0:
            status = "no_steps"
        elif success_count == total:
            status = "success"
        elif success_count == 0:
            status = "failed"
        else:
            status = "partial"

        record = {
            "task": user_input,
            "steps": steps,
            "results": results,
            "success_count": success_count,
            "total_steps": total,
            "success_rate": f"{(success_count / total * 100):.0f}%" if total > 0 else "0%",
            "status": status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        task_id = tasks_table.insert(record)
        print(f"✅ Task logged to DB (id: {task_id})")
        return task_id

    except Exception as e:
        print(f"❌ Failed to log task: {e}")
        return None


def log_error(step: dict, error: str):
    """
    Save an error to database.
    """
    try:
        errors_table.insert({
            "step": step,
            "error": error,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        print(f"❌ Failed to log error: {e}")


def get_task_history(limit: int = 10) -> list:
    """
    Get recent task history.
    Returns last N tasks.
    """
    try:
        all_tasks = tasks_table.all()
        return all_tasks[-limit:] if all_tasks else []
    except Exception as e:
        print(f"❌ Failed to get history: {e}")
        return []


def get_success_rate() -> dict:
    """
    Get overall statistics.

    Returns:
    {
        "total_runs": 10,
        "successful_runs": 8,
        "success_rate": "80%"
    }
    """
    try:
        all_tasks = tasks_table.all()

        if not all_tasks:
            return {
                "total_runs": 0,
                "successful_runs": 0,
                "success_rate": "0%"
            }

        total = len(all_tasks)
        success = sum(1 for t in all_tasks if t.get("status") == "success")

        return {
            "total_runs": total,
            "successful_runs": success,
            "failed_runs": total - success,
            "success_rate": f"{(success / total * 100):.0f}%"
        }

    except Exception as e:
        print(f"❌ Failed to get stats: {e}")
        return {}


def search_tasks(keyword: str) -> list:
    """
    Search tasks by keyword.

    Example: search_tasks("google")
    Returns all tasks containing "google"
    """
    try:
        return tasks_table.search(
            TaskQuery.task.test(
                lambda x: keyword.lower() in x.lower()
            )
        )
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return []