# ============================================
# RAG - Retrieval Augmented Generation
# Gets context from memory to help LLM
# ============================================
from app.memory.vector_store import find_similar_tasks, get_memory_count


def get_context_from_memory(user_input: str) -> str:
    """
    RAG Pipeline:
    1. RETRIEVE - Find similar past tasks
    2. FORMAT   - Format them as context text
    3. RETURN   - Give context to LLM

    Example output:
    "Similar tasks I have done before:
     1. Task: 'Search Python on Google'
        Steps: [open_url, type, click]
     2. Task: 'Search Java on Google'
        Steps: [open_url, type, click]"
    """

    # Check if we have any memories
    total_memories = get_memory_count()
    print(f"🧠 Total memories in DB: {total_memories}")

    if total_memories == 0:
        return ""

    # RETRIEVE - Find similar tasks
    similar_tasks = find_similar_tasks(user_input)

    if not similar_tasks:
        print("ℹ️ No similar tasks found in memory")
        return ""

    print(f"✅ Found {len(similar_tasks)} similar past tasks")

    # FORMAT - Build context string
    context_lines = ["Similar tasks I have done before (use these as reference):"]

    for i, task in enumerate(similar_tasks, 1):
        context_lines.append(
            f"\n{i}. Previous Task: '{task['task']}'"
            f"\n   Steps Used: {task['steps']}"
        )

    return "\n".join(context_lines)