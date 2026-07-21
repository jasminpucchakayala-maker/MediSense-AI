import pandas as pd
from sklearn.preprocessing import LabelEncoder


def preprocess_data(train_df, test_df):
    """
    Preprocess training and testing datasets.

    Returns:
        X_train, X_test, y_train, y_test, label_encoder
    """

    # Remove unwanted columns if present
    train_df = train_df.loc[:, ~train_df.columns.str.contains("^Unnamed")]
    test_df = test_df.loc[:, ~test_df.columns.str.contains("^Unnamed")]

    # Features
    X_train = train_df.drop("prognosis", axis=1)
    X_test = test_df.drop("prognosis", axis=1)

    # Target
    y_train = train_df["prognosis"]
    y_test = test_df["prognosis"]

    # Encode labels
    encoder = LabelEncoder()

    y_train = encoder.fit_transform(y_train)
    y_test = encoder.transform(y_test)

    return X_train, X_test, y_train, y_test, encoder