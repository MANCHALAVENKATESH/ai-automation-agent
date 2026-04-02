# app/agent/agent.py
import warnings
warnings.filterwarnings("ignore")

from app.agent.llm import ask_llm
from app.agent.parser import parse_steps
from app.tools.actions import execute_step
from app.tools.browser import close_browser
from app.memory.vector_store import save_task
from app.memory.rag import get_context_from_memory
from app.database.json_db import log_task, log_error

# Stores recent actions in memory during session
_session_history = []


def run_agent(user_input: str):
    """
    Main agent pipeline.
    """
    # ── Clean the input first ──
    user_input = user_input.strip()  # ← Fixes duplicate task name bug

    print("\n" + "="*50)
    print(f"🎯 Task: {user_input}")
    print("="*50)

    # ============================================
    # STEP 1: RAG - Get context from memory
    # ============================================
    print("\n📚 Step 1: Checking memory for similar tasks...")
    context = get_context_from_memory(user_input)

    if context:
        print(f"✅ Found relevant past experience!")
    else:
        print("ℹ️ No similar past tasks found - starting fresh")

    # ============================================
    # STEP 2: LangChain - Send to LLM
    # ============================================
    print("\n🤖 Step 2: Generating steps with LLM...")

    history_text = "\n".join(_session_history[-5:]) if _session_history else ""

    raw_result = ask_llm(
        user_input=user_input,
        context=context,
        history=history_text
    )

    if not raw_result:
        print("❌ LLM returned empty response")
        return

    # ============================================
    # STEP 3: Parse steps
    # ============================================
    print("\n🔍 Step 3: Parsing steps...")
    steps = parse_steps(raw_result)

    if not steps:
        print("❌ No valid steps found")
        return

    print(f"\n✅ Found {len(steps)} valid steps:")
    for i, step in enumerate(steps, 1):
        print(f"   {i}. {step}")

    # ============================================
    # STEP 4: Execute steps
    # ============================================
    print("\n▶️ Step 4: Executing steps...")
    results = []

    for i, step in enumerate(steps, 1):
        print(f"\n--- Step {i}/{len(steps)} ---")
        success = execute_step(step)
        results.append(success)

        status = "✅ Success" if success else "❌ Failed"
        _session_history.append(
            f"Task: {user_input} | Step {i}: {step} | {status}"
        )

        if not success:
            log_error(step, "Step execution failed")

    # ============================================
    # STEP 5: Save to Vector DB
    # ============================================
    print("\n💾 Step 5: Saving to memory...")
    all_success = all(results)
    save_task(user_input, steps, all_success)

    # ============================================
    # STEP 6: Save to JSON DB
    # ============================================
    log_task(user_input, steps, results)

    # ============================================
    # STEP 7: Summary
    # ============================================
    passed = sum(results)
    total = len(results)

    print("\n" + "="*50)
    print("📊 TASK COMPLETE")
    print("="*50)
    print(f"✅ Steps passed : {passed}/{total}")
    print(f"🧠 Saved memory : Yes")
    print(f"📝 Logged to DB : Yes")

    close_browser()