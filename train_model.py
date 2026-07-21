import os
import joblib
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

from utils.preprocessing import preprocess_data

TRAIN_PATH = "data/raw/Training.csv"
TEST_PATH = "data/raw/Testing.csv"

print("Loading datasets...")

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

X_train, X_test, y_train, y_test, encoder = preprocess_data(train_df, test_df)

models = {
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "Naive Bayes": GaussianNB(),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}

results = {}

best_model = None
best_accuracy = 0

print("\nTraining Models...\n")

for name, model in models.items():
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    results[name] = accuracy

    print(f"{name:<20} Accuracy : {accuracy:.4f}")

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model

os.makedirs("models", exist_ok=True)

joblib.dump(best_model, "models/best_model.pkl")
joblib.dump(encoder, "models/label_encoder.pkl")

print("\n=================================")
print("Best Model Saved Successfully!")
print("=================================")
print(f"Best Accuracy : {best_accuracy:.4f}")