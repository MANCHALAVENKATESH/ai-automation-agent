# app/config.py
import os

# Ollama Settings
OLLAMA_URL = "http://localhost:11434/api/generate"

# ============================================
# MODEL SETTINGS
# ============================================
# Change this to use fine tuned model
# after you have trained it!

USE_FINE_TUNED = False  # ← Set True after fine tuning

if USE_FINE_TUNED:
    MODEL = "automation-agent"  # ← Your fine tuned model
else:
    MODEL = "llama3"            # ← Default model

# Browser Settings
HEADLESS = False

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "agent_db.json")
CHROMA_PATH = os.path.join(DATA_DIR, "chroma_db")
TRAINING_DIR = os.path.join(DATA_DIR, "training")

# Memory Settings
MAX_HISTORY = 5
TOP_K_RESULTS = 3

# Create directories
for d in [DATA_DIR, CHROMA_PATH, TRAINING_DIR]:
    os.makedirs(d, exist_ok=True)