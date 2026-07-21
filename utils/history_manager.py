import pandas as pd
from datetime import datetime
import os
import json


HISTORY_FILE = "data/prediction_history.csv"


def save_prediction(
    disease,
    symptoms,
    confidence=None,
    risk=None,
    top_predictions=None
):
    """
    Save AI prediction history.

    Stores:
    - Disease
    - Symptoms
    - Confidence
    - Risk Level
    - Top Predictions
    """


    os.makedirs(
        "history",
        exist_ok=True
    )



    columns = [
        "Date",
        "Time",
        "Disease",
        "Symptoms",
        "Confidence",
        "Risk Level",
        "Top Predictions"
    ]



    # Create file if missing

    if not os.path.exists(HISTORY_FILE):

        pd.DataFrame(
            columns=columns
        ).to_csv(
            HISTORY_FILE,
            index=False
        )



    # Convert top predictions to text

    if top_predictions:

        top_prediction_text = json.dumps(
            top_predictions
        )

    else:

        top_prediction_text = ""



    new_row = pd.DataFrame([{

        "Date":
            datetime.now().strftime("%d-%m-%Y"),

        "Time":
            datetime.now().strftime("%I:%M %p"),

        "Disease":
            disease,

        "Symptoms":
            ", ".join(symptoms),

        "Confidence":
            confidence if confidence else 0,

        "Risk Level":
            risk if risk else "Unknown",

        "Top Predictions":
            top_prediction_text

    }])



    history = pd.read_csv(
        HISTORY_FILE
    )


    history = pd.concat(
        [
            history,
            new_row
        ],
        ignore_index=True
    )


    history.to_csv(
        HISTORY_FILE,
        index=False
    )



def load_history():

    if os.path.exists(HISTORY_FILE):

        return pd.read_csv(
            HISTORY_FILE
        )


    return pd.DataFrame(
        columns=[
            "Date",
            "Time",
            "Disease",
            "Symptoms",
            "Confidence",
            "Risk Level",
            "Top Predictions"
        ]
    )