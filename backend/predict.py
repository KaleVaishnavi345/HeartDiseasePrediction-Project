import pickle
import os
import pandas as pd

# ---------------------------------
# 1) BASE DIRECTORY
# ---------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "model_ml_2.pkl")
BEST_MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model_comparison.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler_1.pkl")

# ---------------------------------
# 2) LOAD MODEL AND SCALER
# ---------------------------------
with open(MODEL_PATH, "rb") as f:
    logistic_model = pickle.load(f)

with open(BEST_MODEL_PATH, "rb") as f:
    best_model = pickle.load(f)

with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)

# ---------------------------------
# 3) SAME COLUMN ORDER AS TRAINING
# ---------------------------------
columns = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal",
]

# ---------------------------------
# 4) PREDICTION FUNCTION
# ---------------------------------
def predict_heart(data, model_name="logistic_regression"):
    df = pd.DataFrame([data], columns=columns)

    # Keep backend logs concise for production/demo runs.

    logistic_input = scaler.transform(df)
    best_input = df

    if model_name == "best_model":
        selected_model = best_model
        model_input = best_input
        used_model_name = "Best Comparison Model"
        class_probabilities = selected_model.predict_proba(model_input)[0]
        prediction_class = int(selected_model.predict(model_input)[0])
    elif model_name == "ensemble":
        logistic_probabilities = logistic_model.predict_proba(logistic_input)[0]
        best_probabilities = best_model.predict_proba(best_input)[0]
        class_probabilities = (logistic_probabilities + best_probabilities) / 2
        prediction_class = int(class_probabilities.argmax())
        used_model_name = "Ensemble (Logistic + Best Model)"
    else:
        selected_model = logistic_model
        model_input = logistic_input
        used_model_name = "Logistic Regression"
        class_probabilities = selected_model.predict_proba(model_input)[0]
        prediction_class = int(selected_model.predict(model_input)[0])

    # Class mapping for this project dataset: target=0 is high risk, target=1 is low risk.
    high_risk_probability = float(class_probabilities[0])
    low_risk_probability = float(class_probabilities[1])

    if prediction_class == 0:
        confidence = round(high_risk_probability * 100, 2)
    else:
        confidence = round(low_risk_probability * 100, 2)

    return {
        "prediction_class": prediction_class,
        "confidence": confidence,
        "high_risk_probability": round(high_risk_probability * 100, 2),
        "low_risk_probability": round(low_risk_probability * 100, 2),
        "model_used": used_model_name,
    }
