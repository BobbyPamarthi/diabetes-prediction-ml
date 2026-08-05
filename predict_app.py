from flask import Flask, request, render_template_string
import joblib, pandas as pd, os

app = Flask(__name__)

MODEL_DIR = 'D:/sugarrr/saved_model'
rf      = joblib.load(f'{MODEL_DIR}/rf_model.pkl')
scaler  = joblib.load(f'{MODEL_DIR}/scaler.pkl')
FEATURE_COLS = joblib.load(f'{MODEL_DIR}/feature_cols.pkl')

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Diabetes Risk Predictor</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 32px 16px; }
  .container { width: 100%; max-width: 620px; }
  h1 { font-size: 1.7rem; font-weight: 700; text-align: center; margin-bottom: 6px; }
  .sub { text-align: center; color: #64748b; font-size: .9rem; margin-bottom: 32px; }
  .card { background: #1e293b; border-radius: 16px; padding: 32px; border: 1px solid #334155; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .field { display: flex; flex-direction: column; gap: 6px; }
  .field.full { grid-column: 1 / -1; }
  label { font-size: .8rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; }
  input, select {
    background: #0f172a; border: 1px solid #334155; color: #e2e8f0;
    border-radius: 8px; padding: 10px 14px; font-size: .95rem; width: 100%;
    transition: border-color .2s;
  }
  input:focus, select:focus { outline: none; border-color: #6366f1; }
  input[type=range] { padding: 6px 0; background: none; border: none; cursor: pointer; }
  .range-val { font-size: .85rem; color: #a5b4fc; font-weight: 600; margin-top: 2px; }
  .hint { font-size: .72rem; color: #475569; margin-top: 2px; }
  .divider { grid-column: 1 / -1; border: none; border-top: 1px solid #334155; margin: 4px 0; }
  button {
    width: 100%; margin-top: 24px; padding: 14px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff; font-size: 1rem; font-weight: 700; border: none;
    border-radius: 10px; cursor: pointer; transition: opacity .2s;
  }
  button:hover { opacity: .9; }

  /* Result */
  .result { margin-top: 24px; border-radius: 12px; padding: 24px; text-align: center; display: none; }
  .result.positive { background: #450a0a; border: 1px solid #dc2626; }
  .result.negative { background: #052e16; border: 1px solid #16a34a; }
  .result .icon { font-size: 2.5rem; margin-bottom: 8px; }
  .result .verdict { font-size: 1.4rem; font-weight: 700; margin-bottom: 6px; }
  .result.positive .verdict { color: #f87171; }
  .result.negative .verdict { color: #4ade80; }
  .result .prob { font-size: .9rem; color: #94a3b8; }
  .bar-wrap { background: #0f172a; border-radius: 999px; height: 10px; margin: 14px 0 6px; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 999px; transition: width .6s ease; }
  .result.positive .bar-fill { background: #dc2626; }
  .result.negative .bar-fill { background: #16a34a; }
  .bar-labels { display: flex; justify-content: space-between; font-size: .72rem; color: #475569; }
  .tips { margin-top: 16px; text-align: left; font-size: .82rem; color: #94a3b8; line-height: 1.7; }

  @media(max-width:500px){ .grid{grid-template-columns:1fr;} }
</style>
</head>
<body>
<div class="container">
  <h1>🩺 Diabetes Risk Predictor</h1>
  <p class="sub">Powered by Random Forest (96.67% accuracy) &nbsp;|&nbsp; Enter patient details below</p>

  <div class="card">
    <form id="form">
      <div class="grid">

        <div class="field">
          <label>Gender</label>
          <select name="gender">
            <option value="Female">Female</option>
            <option value="Male">Male</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div class="field">
          <label>Age</label>
          <input type="number" name="age" min="1" max="120" value="45" required>
          <span class="hint">Years (1 – 120)</span>
        </div>

        <div class="field">
          <label>BMI</label>
          <input type="number" name="bmi" step="0.1" min="10" max="70" value="27.5" required>
          <span class="hint">Body Mass Index (10 – 70)</span>
        </div>

        <div class="field">
          <label>HbA1c Level</label>
          <input type="number" name="hba1c" step="0.1" min="3" max="15" value="5.5" required>
          <span class="hint">% (normal &lt; 5.7)</span>
        </div>

        <div class="field full">
          <label>Blood Glucose Level</label>
          <input type="range" name="glucose" min="70" max="300" value="140" oninput="document.getElementById('glu_val').textContent=this.value">
          <div class="range-val">Value: <span id="glu_val">140</span> mg/dL</div>
          <div class="hint">Normal fasting: 70–99 &nbsp;|&nbsp; Pre-diabetic: 100–125 &nbsp;|&nbsp; Diabetic: 126+</div>
        </div>

        <hr class="divider">

        <div class="field">
          <label>Hypertension</label>
          <select name="hypertension">
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>

        <div class="field">
          <label>Heart Disease</label>
          <select name="heart_disease">
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>

        <div class="field full">
          <label>Smoking History</label>
          <select name="smoking">
            <option value="never">Never</option>
            <option value="No Info">No Info</option>
            <option value="current">Current Smoker</option>
            <option value="former">Former Smoker</option>
            <option value="ever">Ever Smoked</option>
            <option value="not current">Not Current</option>
          </select>
        </div>

      </div>
      <button type="submit">Predict Diabetes Risk</button>
    </form>

    <div class="result" id="result">
      <div class="icon" id="r_icon"></div>
      <div class="verdict" id="r_verdict"></div>
      <div class="prob" id="r_prob"></div>
      <div class="bar-wrap"><div class="bar-fill" id="r_bar" style="width:0%"></div></div>
      <div class="bar-labels"><span>0% Risk</span><span>100% Risk</span></div>
      <div class="tips" id="r_tips"></div>
    </div>
  </div>
</div>

<script>
document.getElementById('form').addEventListener('submit', async e => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const data = Object.fromEntries(fd.entries());
  data.glucose = document.querySelector('[name=glucose]').value;

  const res = await fetch('/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
  const json = await res.json();

  const el = document.getElementById('result');
  el.className = 'result ' + (json.diabetic ? 'positive' : 'negative');
  el.style.display = 'block';
  document.getElementById('r_icon').textContent  = json.diabetic ? '⚠️' : '✅';
  document.getElementById('r_verdict').textContent = json.diabetic ? 'High Diabetes Risk' : 'Low Diabetes Risk';
  document.getElementById('r_prob').textContent = `Probability: ${(json.probability * 100).toFixed(1)}%`;
  document.getElementById('r_bar').style.width = (json.probability * 100).toFixed(1) + '%';
  document.getElementById('r_tips').innerHTML = json.tips;
  el.scrollIntoView({behavior:'smooth', block:'nearest'});
});
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/predict', methods=['POST'])
def predict():
    d = request.get_json()

    gender        = d.get('gender', 'Female')
    age           = float(d.get('age', 45))
    hypertension  = int(d.get('hypertension', 0))
    heart_disease = int(d.get('heart_disease', 0))
    smoking       = d.get('smoking', 'never')
    bmi           = float(d.get('bmi', 27.5))
    hba1c         = float(d.get('hba1c', 5.5))
    glucose       = float(d.get('glucose', 140))

    row = {col: False for col in FEATURE_COLS}
    row['age']                = age
    row['hypertension']       = hypertension
    row['heart_disease']      = heart_disease
    row['bmi']                = bmi
    row['HbA1c_level']        = hba1c
    row['blood_glucose_level']= glucose

    if gender == 'Male'  and 'gender_Male'  in row: row['gender_Male']  = True
    if gender == 'Other' and 'gender_Other' in row: row['gender_Other'] = True

    smoke_col = f'smoking_history_{smoking}'
    if smoke_col in row:
        row[smoke_col] = True

    df = pd.DataFrame([row])[FEATURE_COLS]
    prob = float(rf.predict_proba(df)[0][1])
    diabetic = prob >= 0.5

    tips_pos = """
      <b>Recommended actions:</b><br>
      • Consult a healthcare provider immediately<br>
      • Monitor blood glucose regularly<br>
      • Adopt a low-sugar, high-fiber diet<br>
      • Increase physical activity (150 min/week)<br>
      • Check HbA1c every 3 months
    """
    tips_neg = """
      <b>Stay healthy:</b><br>
      • Maintain a balanced diet<br>
      • Exercise regularly<br>
      • Monitor weight and BMI<br>
      • Annual health checkup recommended
    """

    return {'diabetic': diabetic, 'probability': round(prob, 4), 'tips': tips_pos if diabetic else tips_neg}

if __name__ == '__main__':
    app.run(debug=False, port=5001)
