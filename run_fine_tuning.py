# run_fine_tuning.py
# ============================================
# RUN THIS TO FINE TUNE YOUR MODEL
# ============================================
import warnings
warnings.filterwarnings("ignore")

from app.training.data_collector import save_ollama_training_file
from app.training.data_preparer import (
    validate_training_data,
    clean_training_data,
    show_training_examples
)
from app.training.fine_tuner import (
    create_modelfile,
    create_custom_model,
    list_ollama_models,
    test_fine_tuned_model
)


def run_pipeline():
    print("=" * 60)
    print("🧠 FINE TUNING PIPELINE")
    print("=" * 60)

    # ── STEP 1: Collect Data ──
    print("\n📦 STEP 1: Collecting Training Data...")
    training_file = save_ollama_training_file()

    if not training_file:
        print("❌ No training data!")
        print("   Run at least 10 successful tasks first")
        print("   Then run this script again")
        return

    # ── STEP 2: Validate Data ──
    print("\n🔍 STEP 2: Validating Training Data...")
    report = validate_training_data(training_file)

    if report["good"] < 5:
        print(f"❌ Not enough good data ({report['good']} examples)")
        print("   Need at least 5 good examples")
        print("   Run more tasks and try again")
        return

    # ── STEP 3: Clean Data ──
    print("\n🧹 STEP 3: Cleaning Training Data...")
    clean_file = clean_training_data(training_file)

    # ── STEP 4: Show Examples ──
    print("\n📝 STEP 4: Sample Training Data:")
    show_training_examples(clean_file, count=2)

    # ── STEP 5: Create Modelfile ──
    print("\n📄 STEP 5: Creating Modelfile...")
    modelfile = create_modelfile(
        training_file=clean_file,
        model_name="automation-agent"
    )

    # ── STEP 6: Create Model ──
    print("\n🔨 STEP 6: Creating Fine Tuned Model...")
    create_custom_model(
        modelfile_path=modelfile,
        model_name="automation-agent"
    )

    # ── STEP 7: List Models ──
    print("\n📋 STEP 7: Available Models:")
    list_ollama_models()

    # ── STEP 8: Test Model ──
    print("\n🧪 STEP 8: Testing Fine Tuned Model...")
    test_fine_tuned_model("automation-agent")

    # ── STEP 9: Update Config ──
    print("\n" + "=" * 60)
    print("✅ FINE TUNING COMPLETE!")
    print("=" * 60)
    print("\nTo use your fine tuned model:")
    print("  Open app/config.py")
    print("  Change: USE_FINE_TUNED = False")
    print("  To    : USE_FINE_TUNED = True")
    print("\nThen run: python main.py")


if __name__ == "__main__":
    run_pipeline()