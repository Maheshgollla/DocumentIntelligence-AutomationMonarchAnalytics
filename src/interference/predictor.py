import os
import sys
import logging
import joblib

# ✅ Dynamically add the project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ✅ Now imports will always work
from src.preprocessing.normalizer import normalize_text_value

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ✅ Correct path for model
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "model.pkl")

# Load model
try:
    model = joblib.load(MODEL_PATH)
    logging.info(f"✅ ML model loaded successfully from {MODEL_PATH}")
except Exception as e:
    logging.error(f"❌ Failed to load model from {MODEL_PATH}: {e}")
    model = None

# Example text
texts = ["Invoice date: October 2, 2025", "Amount: $1200"]
normalized_output = [normalize_text_value(t) for t in texts]

# Predict if model loaded
if model:
    try:
        predictions = model.predict([[90]])  # dummy example
        ml_prediction = float(predictions[0])
    except Exception as e:
        logging.error(f"❌ Inference failed: {e}")
        ml_prediction = "Error during inference"
else:
    ml_prediction = "N/A (model not loaded)"

# Final result
final_result = {
    "ml_prediction": ml_prediction,
    "normalized_output": normalized_output
}

logging.info(f"✅ Final merged result: {final_result}")
