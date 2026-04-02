# app/memory/vector_store.py
import warnings
import os
import sys
import json
import uuid
from datetime import datetime
import logging

warnings.filterwarnings("ignore")

# ── Load .env ──
from dotenv import load_dotenv
load_dotenv()

# ── Suppress warnings ──
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

# ── Add ROOT to path ──
ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import chromadb
from sentence_transformers import SentenceTransformer
from app.config import CHROMA_PATH, TOP_K_RESULTS

# Create directory
os.makedirs(CHROMA_PATH, exist_ok=True)

print("📦 Loading Vector DB...")

# ── Connect ChromaDB ──
client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="agent_memory",
    metadata={"hnsw:space": "cosine"}
)

# ── Load Embedding Model with HF Token ──
print("📦 Loading embedding model...")

hf_token = os.getenv("HF_TOKEN")
if hf_token:
    print(f"✅ Using HF Token: {hf_token[:8]}...")
else:
    print("⚠️ No HF Token found")

embedder = SentenceTransformer(
    "all-MiniLM-L6-v2",
    use_auth_token=hf_token,
    tokenizer_kwargs={"clean_up_tokenization_spaces": True}
)

print("✅ Vector DB ready!")


def save_task(user_input: str, steps: list, success: bool):
    """Save completed task to Vector DB."""
    try:
        doc_id = str(uuid.uuid4())
        steps_text = json.dumps(steps)

        collection.add(
            documents=[user_input],
            metadatas=[{
                "steps": steps_text,
                "success": str(success),
                "timestamp": datetime.now().isoformat()
            }],
            ids=[doc_id]
        )
        print(f"✅ Saved to Vector DB (id: {doc_id[:8]}...)")

    except Exception as e:
        print(f"❌ Failed to save: {e}")


def find_similar_tasks(
    user_input: str,
    only_successful: bool = True
) -> list:
    """Find similar past tasks."""
    try:
        count = collection.count()
        if count == 0:
            return []

        n_results = min(TOP_K_RESULTS, count)
        where_filter = {"success": "True"} if only_successful else None

        results = collection.query(
            query_texts=[user_input],
            n_results=n_results,
            where=where_filter
        )

        similar_tasks = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                similar_tasks.append({
                    "task": doc,
                    "steps": results["metadatas"][0][i].get("steps", "[]"),
                    "timestamp": results["metadatas"][0][i].get("timestamp", "")
                })

        return similar_tasks

    except Exception as e:
        print(f"❌ Search error: {e}")
        return []


def get_memory_count() -> int:
    """Get total memories stored."""
    try:
        return collection.count()
    except:
        return 0


def delete_all_memories():
    """Clear all memories."""
    try:
        client.delete_collection("agent_memory")
        print("🗑️ All memories deleted")
    except Exception as e:
        print(f"❌ Error: {e}")