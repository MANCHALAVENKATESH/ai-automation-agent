# ============================================
# API - Flask web API
# ============================================
from flask import Flask, request, jsonify
from app.agent.agent import run_agent
from app.database.json_db import (
    get_task_history,
    get_success_rate,
    search_tasks
)

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    """Check if API is running."""
    return jsonify({
        "status": "ok",
        "message": "Agent API is running"
    })


@app.route("/run", methods=["POST"])
def run():
    """
    Run a task.

    POST /run
    Body: {"task": "Search Python on Google"}
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data sent"}), 400

    task = data.get("task", "").strip()

    if not task:
        return jsonify({"error": "No task provided"}), 400

    try:
        run_agent(task)
        return jsonify({
            "status": "success",
            "task": task,
            "message": "Task completed"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route("/history", methods=["GET"])
def history():
    """Get recent task history."""
    limit = request.args.get("limit", 10, type=int)
    tasks = get_task_history(limit=limit)
    return jsonify({
        "status": "ok",
        "count": len(tasks),
        "tasks": tasks
    })


@app.route("/stats", methods=["GET"])
def stats():
    """Get success statistics."""
    return jsonify(get_success_rate())


@app.route("/search", methods=["GET"])
def search():
    """
    Search past tasks.
    GET /search?q=google
    """
    keyword = request.args.get("q", "")
    if not keyword:
        return jsonify({"error": "No search keyword"}), 400

    results = search_tasks(keyword)
    return jsonify({
        "keyword": keyword,
        "count": len(results),
        "results": results
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)