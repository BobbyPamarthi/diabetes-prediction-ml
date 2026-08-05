import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, roc_curve, auc
)
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

import os
os.makedirs('D:/sugarrr/plots', exist_ok=True)

# --- Load data (local file instead of Google Drive) ---
data = pd.read_csv('D:/sugarrr/diabetes_prediction_dataset.csv')
print(data.head(3))
print('\nClass wise count')
print(data['diabetes'].value_counts())

# --- SMOTE ---
sm = SMOTE(random_state=42)
X = data.drop('diabetes', axis=1)
y = data['diabetes']
X_encoded = pd.get_dummies(X, drop_first=True)
X_res, y_res = sm.fit_resample(X_encoded, y)
print("\nAfter SMOTE:")
print(y_res.value_counts())

# --- Train/Test split + Scaling ---
X_train, X_test, y_train, y_test = train_test_split(
    X_res, y_res, test_size=0.2, random_state=42, stratify=y_res
)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- Helper function ---
def train_eval_model(model, X_train, X_test, y_train, y_test, model_name):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        y_score = model.predict_proba(X_test)[:, 1]
    else:
        y_score = model.decision_function(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_score)

    print(f"\n=== {model_name} ===")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1-score : {f1:.4f}")
    print(f"ROC-AUC  : {auc_score:.4f}")

    fpr, tpr, _ = roc_curve(y_test, y_score)
    plt.figure()
    plt.plot(fpr, tpr, label=f"{model_name} (AUC={auc_score:.3f})")
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC Curve - {model_name}")
    plt.legend(loc="lower right")
    plt.grid(True)
    safe_name = model_name.replace(" ", "_").replace("-", "_")
    plt.savefig(f'D:/sugarrr/plots/roc_{safe_name}.png', dpi=100, bbox_inches='tight')
    plt.close()
    print(f"  -> Saved plots/roc_{safe_name}.png")

# --- Train all models ---
print("\n" + "="*50)
print("TRAINING INDIVIDUAL MODELS")
print("="*50)

log_reg = LogisticRegression(max_iter=1000)
train_eval_model(log_reg, X_train_scaled, X_test_scaled, y_train, y_test, "Logistic Regression")

knn = KNeighborsClassifier(n_neighbors=5)
train_eval_model(knn, X_train_scaled, X_test_scaled, y_train, y_test, "K-Nearest Neighbors")

base_estimator = DecisionTreeClassifier(max_depth=1, random_state=42)
ab = AdaBoostClassifier(estimator=base_estimator, n_estimators=50, random_state=42)
train_eval_model(ab, X_train_scaled, X_test_scaled, y_train, y_test, "AdaBoost")

nb = GaussianNB()
train_eval_model(nb, X_train, X_test, y_train, y_test, "Naive Bayes")

dt = DecisionTreeClassifier(max_depth=18, random_state=42)
train_eval_model(dt, X_train, X_test, y_train, y_test, "Decision Tree")

rf = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=40)
train_eval_model(rf, X_train, X_test, y_train, y_test, "Random Forest")

xgb = XGBClassifier(
    n_estimators=200, learning_rate=0.05, max_depth=4,
    subsample=0.8, colsample_bytree=0.8,
    eval_metric='logloss', random_state=42
)
train_eval_model(xgb, X_train, X_test, y_train, y_test, "XGBoost")

# --- ANN ---
print("\n" + "="*50)
print("TRAINING ANN")
print("="*50)

ann_model = Sequential([
    Dense(32, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])
ann_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
ann_model.summary()

history = ann_model.fit(
    X_train_scaled, y_train,
    epochs=100, batch_size=16,
    validation_split=0.2, verbose=1
)
print("Training finished.")

print("\nTesting Accuracy:")
print(np.max(history.history['val_accuracy']))

best_val_acc_epoch = np.argmax(history.history['val_accuracy']) + 1
best_val_acc = np.max(history.history['val_accuracy'])
print(f"Best Validation Accuracy: {best_val_acc:.4f} at Epoch {best_val_acc_epoch}")

# Accuracy & Loss plots
sns.set_style("darkgrid")
plt.figure(figsize=(10, 5))
plt.plot(history.history['accuracy'], label='Train Accuracy', color='red', marker='o')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy', color='green', marker='o')
plt.xlabel('Epochs'); plt.ylabel('Accuracy'); plt.title('Accuracy')
plt.legend(); plt.ylim(0, 1)
plt.savefig('D:/sugarrr/plots/ann_accuracy.png', dpi=100, bbox_inches='tight'); plt.close()
print("  -> Saved plots/ann_accuracy.png")

plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Train Loss', color='red', marker='o')
plt.plot(history.history['val_loss'], label='Validation Loss', color='purple', marker='o')
plt.xlabel('Epochs'); plt.ylabel('Loss'); plt.title('Loss')
plt.legend(); plt.ylim(0, max(history.history['loss']) + 0.1)
plt.savefig('D:/sugarrr/plots/ann_loss.png', dpi=100, bbox_inches='tight'); plt.close()
print("  -> Saved plots/ann_loss.png")

# --- Ensemble ---
print("\n" + "="*50)
print("ENSEMBLE (RF + XGB + ANN)")
print("="*50)

rfc = RandomForestClassifier(n_estimators=200, max_depth=30, random_state=40)
rfc.fit(X_train, y_train)
xgbc = XGBClassifier(n_estimators=200, random_state=42)
xgbc.fit(X_train, y_train)

proba_rf = rfc.predict_proba(X_test)[:, 1]
proba_xgb = xgbc.predict_proba(X_test)[:, 1]
proba_ann = ann_model.predict(X_test_scaled).ravel()

avg_proba = (proba_rf + proba_xgb + proba_ann) / 3.0
y_pred_ens = (avg_proba >= 0.5).astype(int)

acc = accuracy_score(y_test, y_pred_ens)
prec = precision_score(y_test, y_pred_ens)
rec = recall_score(y_test, y_pred_ens)
f1 = f1_score(y_test, y_pred_ens)
auc_val = roc_auc_score(y_test, avg_proba)

print(f"\n=== Ensemble (RF + XGB + ANN) ===")
print(f"Accuracy : {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall   : {rec:.4f}")
print(f"F1-score : {f1:.4f}")
print(f"ROC-AUC  : {auc_val:.4f}")

# ROC Curve comparison
fpr_ens, tpr_ens, _ = roc_curve(y_test, avg_proba)
auc_ens = auc(fpr_ens, tpr_ens)

plt.figure(figsize=(8, 6))
plt.plot(fpr_ens, tpr_ens, label=f"Ensemble (AUC = {auc_ens:.3f})", linewidth=2.8)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison: RF + XGB + ANN Hybrid Ensemble")
plt.legend(); plt.grid(True)
plt.savefig('D:/sugarrr/plots/ensemble_roc.png', dpi=100, bbox_inches='tight'); plt.close()
print("  -> Saved plots/ensemble_roc.png")

print("\nDone!")
