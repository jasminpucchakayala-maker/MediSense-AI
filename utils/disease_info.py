import pandas as pd

df = pd.read_csv("data/external/disease_info.csv")

DISEASE_INFO = {}

for _, row in df.iterrows():
    DISEASE_INFO[row["Disease"]] = {
        "description": row["Description"],
        "precautions": row["Precautions"].split("|"),
        "diet": row["Diet"].split("|"),
        "doctor": row["Doctor_Advice"]
    }