import joblib
import pandas as pd
import numpy as np

# Load model
model = joblib.load("models/best_model.pkl")
encoder = joblib.load("models/label_encoder.pkl")


def predict_disease(selected_symptoms, all_symptoms):
    """
    Predict disease from selected symptoms.
    Returns:
    - Disease prediction
    - Confidence score (float)
    - Top 3 predictions with probabilities (float)
    """

    # Create input vector
    input_data = [0] * len(all_symptoms)

    for symptom in selected_symptoms:
        if symptom in all_symptoms:
            index = all_symptoms.index(symptom)
            input_data[index] = 1

    # Convert to dataframe
    input_df = pd.DataFrame(
        [input_data],
        columns=all_symptoms
    )

    # Prediction
    prediction = model.predict(input_df)
    disease = encoder.inverse_transform(prediction)[0]

    # Probability calculation
    probabilities = model.predict_proba(input_df)[0]

    # Get top 3 predictions
    top_indices = probabilities.argsort()[-3:][::-1]

    top_predictions = []

    for index in top_indices:
        disease_name = encoder.inverse_transform([index])[0]
        # Force float conversion to prevent json serialization issues with numpy float64
        probability = float(round(probabilities[index] * 100, 2))

        top_predictions.append(
            {
                "disease": disease_name,
                "probability": probability
            }
        )

    # Confidence of main prediction (force float conversion)
    confidence = float(round(max(probabilities) * 100, 2))

    return {
        "disease": disease,
        "confidence": confidence,
        "top_predictions": top_predictions
    }