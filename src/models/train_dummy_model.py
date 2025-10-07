# train_dummy_model.py
from pathlib import Path
from sklearn.linear_model import LinearRegression
import joblib
import numpy as np

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Create models folder if it doesn't exist
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Path to save the model
MODEL_PATH = MODELS_DIR / "model.pkl"

# Dummy training data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Train a simple linear regression model
model = LinearRegression()
model.fit(X, y)

# Save the trained model
joblib.dump(model, MODEL_PATH)

print(f"✅ Model trained and saved at {MODEL_PATH}")
