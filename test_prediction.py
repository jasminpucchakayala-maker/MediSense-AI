import pandas as pd

from utils.predictor import predict_disease

train = pd.read_csv("data/raw/Training.csv")

train = train.loc[:, ~train.columns.str.contains("^Unnamed")]

all_symptoms = list(train.columns[:-1])

symptoms = [
    "itching",
    "skin_rash",
    "nodal_skin_eruptions"
]

prediction = predict_disease(
    symptoms,
    all_symptoms
)

print("=" * 50)
print("Predicted Disease")
print("=" * 50)

print(prediction)