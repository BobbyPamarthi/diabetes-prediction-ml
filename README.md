# 🩺 Diabetes Prediction using Machine Learning

A comparative study of **9 classification algorithms** on a 100,000-record diabetes dataset, with an ensemble model achieving **97.67% accuracy**. Includes two interactive Flask web apps — a results dashboard and a live patient prediction form.

---

## 📊 Results Summary

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 91.46% | 0.9153 | 0.9138 | 0.9145 | 0.9766 |
| K-Nearest Neighbors | 94.59% | 0.9329 | 0.9610 | 0.9467 | 0.9831 |
| AdaBoost | 92.59% | 0.9136 | 0.9409 | 0.9270 | 0.9855 |
| Naive Bayes | 83.55% | 0.7741 | 0.9474 | 0.8520 | 0.9305 |
| Decision Tree | 95.57% | 0.9585 | 0.9526 | 0.9555 | 0.9831 |
| Random Forest | 96.67% | 0.9670 | 0.9663 | 0.9667 | 0.9961 |
| XGBoost | 96.53% | 0.9819 | 0.9481 | 0.9647 | 0.9955 |
| ANN (100 epochs) | 94.39% | — | — | — | — |
| **Ensemble (RF+XGB+ANN)** | **97.67%** | **0.9825** | **0.9707** | **0.9766** | **0.9975** |

---

## 🗂️ Project Structure

```
diabetes-prediction-ml/
│
├── diabetes_prediction_dataset.csv   # Dataset — 100,000 patient records
├── run_diabetes.py                   # Train all 9 models & save plots
├── save_models.py                    # Save best model (RF) to disk
├── app.py                            # Flask dashboard — port 5000
├── predict_app.py                    # Flask prediction form — port 5001
├── start.py                          # Launch both apps simultaneously
├── generate_doc.py                   # Generate Word project report
├── final_code_diabetes_d2.ipynb      # Jupyter notebook
├── Diabetes_Prediction_Project_Report.docx
└── plots/
    ├── roc_Logistic_Regression.png
    ├── roc_K_Nearest_Neighbors.png
    ├── roc_AdaBoost.png
    ├── roc_Naive_Bayes.png
    ├── roc_Decision_Tree.png
    ├── roc_Random_Forest.png
    ├── roc_XGBoost.png
    ├── ensemble_roc.png
    ├── ann_accuracy.png
    └── ann_loss.png
```

---

## 📋 Dataset

- **File:** `diabetes_prediction_dataset.csv`
- **Records:** 100,000 patients
- **Class distribution:** 91,500 non-diabetic / 8,500 diabetic (imbalanced → fixed with SMOTE)

| Feature | Type | Description |
|---|---|---|
| `gender` | Categorical | Female / Male / Other |
| `age` | Numeric | Age in years |
| `hypertension` | Binary | 0 = No, 1 = Yes |
| `heart_disease` | Binary | 0 = No, 1 = Yes |
| `smoking_history` | Categorical | never / current / former / ever / not current / No Info |
| `bmi` | Numeric | Body Mass Index |
| `HbA1c_level` | Numeric | Glycated haemoglobin (%) |
| `blood_glucose_level` | Numeric | Blood glucose (mg/dL) |
| `diabetes` | Binary | **Target** — 0 = No, 1 = Yes |

---

## ⚙️ Preprocessing

1. **One-hot encoding** — `gender` and `smoking_history` → 13 total features after encoding
2. **SMOTE** — balances classes from 91,500:8,500 → 91,500:91,500
3. **Train/Test split** — 80% / 20%, stratified, `random_state=42`
4. **StandardScaler** — applied to Logistic Regression, KNN, AdaBoost, and ANN

---

## 🤖 Models & Hyperparameters

| Model | Key Parameters |
|---|---|
| Logistic Regression | `max_iter=1000` |
| K-Nearest Neighbors | `n_neighbors=5` |
| AdaBoost | `n_estimators=50`, base: `DecisionTree(max_depth=1)` |
| Naive Bayes | Default |
| Decision Tree | `max_depth=18` |
| Random Forest | `n_estimators=200, max_depth=20` |
| XGBoost | `n_estimators=200, lr=0.05, max_depth=4, subsample=0.8` |
| ANN | `Dense(32,relu) → Dense(16,relu) → Dense(1,sigmoid)`, Adam, 100 epochs |
| **Ensemble** | Soft-vote average of RF + XGB + ANN probabilities |

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install pandas numpy scikit-learn imbalanced-learn xgboost tensorflow matplotlib seaborn flask joblib python-docx
```

### 2. First-time setup
```bash
# Train all 9 models and generate plots
python run_diabetes.py

# Save the Random Forest model to disk
python save_models.py
```

### 3. Launch both web apps
```bash
python start.py
```

This opens two browser tabs automatically:

| App | URL | Description |
|---|---|---|
| Dashboard | http://127.0.0.1:5000 | All model metrics, charts, ROC curves |
| Patient Form | http://127.0.0.1:5001 | Enter patient data → get prediction |

---

## 🌐 Web Applications

### Dashboard (Port 5000)
- Accuracy summary cards for all 9 models
- Interactive bar charts — Accuracy, F1-Score, ROC-AUC
- Full metrics comparison table
- ROC curve plots for every model
- ANN training accuracy & loss curves

### Patient Prediction Form (Port 5001)
- Input: Gender, Age, BMI, HbA1c, Blood Glucose, Hypertension, Heart Disease, Smoking
- Powered by the saved Random Forest model (96.67% accuracy)
- Returns risk probability (0–100%) with color-coded result
- Personalised health recommendations

---

## 📈 ROC Curves

All ROC curves are saved in the `plots/` folder and displayed in the dashboard.

---

## 📄 Project Report

A full Word document report (`Diabetes_Prediction_Project_Report.docx`) is included, covering dataset description, preprocessing steps, model architectures, results, and conclusions.

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.x-orange?logo=scikit-learn)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?logo=tensorflow)
![XGBoost](https://img.shields.io/badge/XGBoost-1.x-green)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
