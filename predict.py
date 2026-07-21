import joblib
import pandas as pd

# Load model
model = joblib.load("models/best_model.pkl")
encoder = joblib.load("models/label_encoder.pkl")


def predict_disease(selected_symptoms, all_symptoms):
    """
    Predict disease from selected symptoms.
    """

    input_data = [0] * len(all_symptoms)

    for symptom in selected_symptoms:
        if symptom in all_symptoms:
            index = all_symptoms.index(symptom)
            input_data[index] = 1

    input_df = pd.DataFrame([input_data], columns=all_symptoms)

    prediction = model.predict(input_df)

    disease = encoder.inverse_transform(prediction)

    return disease[0]