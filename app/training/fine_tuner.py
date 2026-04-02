# app/training/fine_tuner.py
# ============================================
# FINE TUNES LLAMA3 USING OLLAMA
# ============================================
import warnings
warnings.filterwarnings("ignore")

import os
import json
import subprocess
from app.config import MODEL


def create_modelfile(
    training_file: str,
    model_name: str = "automation-agent"
) -> str:
    """
    Create Ollama Modelfile for fine tuning.

    Modelfile = Instructions for Ollama
    to create your custom model
    """
    modelfile_content = f"""# Custom fine-tuned model for browser automation

# Base model to start from
FROM {MODEL}

# Model behavior settings
PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER num_ctx 4096

# System prompt - always included
SYSTEM \"\"\"
You are an expert AI browser automation agent.
You have been specifically trained to generate 
browser automation steps.

RULES:
- ALWAYS return valid JSON array
- NEVER add explanations
- NEVER use markdown
- Use ONLY supported actions

SUPPORTED ACTIONS:
- open_url   : {{"action": "open_url", "value": "https://..."}}
- type       : {{"action": "type", "selector": "css", "value": "text"}}
- click      : {{"action": "click", "selector": "css"}}
- wait       : {{"action": "wait", "value": 2000}}
- screenshot : {{"action": "screenshot", "value": "file.png"}}
\"\"\"

# Training data file
# ADAPTER {training_file}
"""

    # Save Modelfile
    modelfile_path = "./data/training/Modelfile"
    os.makedirs(os.path.dirname(modelfile_path), exist_ok=True)

    with open(modelfile_path, "w") as f:
        f.write(modelfile_content)

    print(f"✅ Modelfile created: {modelfile_path}")
    return modelfile_path


def create_custom_model(
    modelfile_path: str,
    model_name: str = "automation-agent"
):
    """
    Create custom Ollama model from Modelfile.

    This runs: ollama create automation-agent -f Modelfile
    """
    print(f"\n🔨 Creating custom model: {model_name}")
    print("This may take a few minutes...")

    try:
        result = subprocess.run(
            ["ollama", "create", model_name, "-f", modelfile_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )

        if result.returncode == 0:
            print(f"✅ Model '{model_name}' created successfully!")
            print(result.stdout)
        else:
            print(f"❌ Failed to create model")
            print(f"   Error: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("❌ Timeout - model creation took too long")
    except FileNotFoundError:
        print("❌ Ollama not found - is it installed?")
    except Exception as e:
        print(f"❌ Error: {e}")


def list_ollama_models():
    """Show all available Ollama models."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )
        print("\n📋 Available Ollama Models:")
        print(result.stdout)
    except Exception as e:
        print(f"❌ Error: {e}")


def test_fine_tuned_model(model_name: str = "automation-agent"):
    """
    Test the fine tuned model.
    """
    print(f"\n🧪 Testing model: {model_name}")

    try:
        from langchain_ollama import OllamaLLM

        # Load fine tuned model
        fine_tuned_llm = OllamaLLM(
            model=model_name,
            temperature=0.1
        )

        # Test prompt
        test_prompt = "Go to google.com and search for Python"

        print(f"📝 Test prompt: {test_prompt}")
        response = fine_tuned_llm.invoke(test_prompt)
        print(f"🤖 Response:\n{response}")

        # Validate response
        try:
            steps = json.loads(response)
            print(f"✅ Valid JSON with {len(steps)} steps!")
        except:
            print("⚠️ Response is not valid JSON")

    except Exception as e:
        print(f"❌ Test failed: {e}")