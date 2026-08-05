"""Train and save the best model (Random Forest) + scaler for the prediction app."""
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib, os

SAVE_DIR = 'D:/sugarrr/saved_model'
os.makedirs(SAVE_DIR, exist_ok=True)

print("Loading data...")
data = pd.read_csv('D:/sugarrr/diabetes_prediction_dataset.csv')

X = data.drop('diabetes', axis=1)
y = data['diabetes']
X_enc = pd.get_dummies(X, drop_first=True)

feature_cols = list(X_enc.columns)
print(f"Features: {feature_cols}")

print("Applying SMOTE...")
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X_enc, y)

X_train, X_test, y_train, y_test = train_test_split(
    X_res, y_res, test_size=0.2, random_state=42, stratify=y_res
)

print("Training Random Forest...")
rf = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=40, n_jobs=-1)
rf.fit(X_train, y_train)

scaler = StandardScaler()
scaler.fit(X_train)

print("Saving model, scaler, and feature columns...")
joblib.dump(rf, f'{SAVE_DIR}/rf_model.pkl')
joblib.dump(scaler, f'{SAVE_DIR}/scaler.pkl')
joblib.dump(feature_cols, f'{SAVE_DIR}/feature_cols.pkl')

from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test, rf.predict(X_test))
print(f"Model accuracy: {acc:.4f}")
print("Done! Models saved to saved_model/")
