from flask import Flask, send_from_directory, render_template_string
import os, base64

app = Flask(__name__)
PLOTS_DIR = 'D:/sugarrr/plots'

MODELS = [
    {"name": "Logistic Regression", "accuracy": 0.9146, "precision": 0.9153, "recall": 0.9138, "f1": 0.9145, "roc_auc": 0.9766, "plot": "roc_Logistic_Regression.png"},
    {"name": "K-Nearest Neighbors", "accuracy": 0.9459, "precision": 0.9329, "recall": 0.9610, "f1": 0.9467, "roc_auc": 0.9831, "plot": "roc_K_Nearest_Neighbors.png"},
    {"name": "AdaBoost",            "accuracy": 0.9259, "precision": 0.9136, "recall": 0.9409, "f1": 0.9270, "roc_auc": 0.9855, "plot": "roc_AdaBoost.png"},
    {"name": "Naive Bayes",         "accuracy": 0.8355, "precision": 0.7741, "recall": 0.9474, "f1": 0.8520, "roc_auc": 0.9305, "plot": "roc_Naive_Bayes.png"},
    {"name": "Decision Tree",       "accuracy": 0.9557, "precision": 0.9585, "recall": 0.9526, "f1": 0.9555, "roc_auc": 0.9831, "plot": "roc_Decision_Tree.png"},
    {"name": "Random Forest",       "accuracy": 0.9667, "precision": 0.9670, "recall": 0.9663, "f1": 0.9667, "roc_auc": 0.9961, "plot": "roc_Random_Forest.png"},
    {"name": "XGBoost",             "accuracy": 0.9653, "precision": 0.9819, "recall": 0.9481, "f1": 0.9647, "roc_auc": 0.9955, "plot": "roc_XGBoost.png"},
    {"name": "ANN",                 "accuracy": 0.9439, "precision": None,   "recall": None,   "f1": None,   "roc_auc": None,   "plot": None},
    {"name": "Ensemble (RF+XGB+ANN)","accuracy": 0.9767,"precision": 0.9825, "recall": 0.9707, "f1": 0.9766, "roc_auc": 0.9975, "plot": "ensemble_roc.png"},
]

def img_b64(filename):
    path = os.path.join(PLOTS_DIR, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Diabetes Prediction Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; }
  header { background: linear-gradient(135deg, #1e40af, #7c3aed); padding: 28px 40px; }
  header h1 { font-size: 2rem; font-weight: 700; }
  header p  { opacity: .75; margin-top: 6px; }
  .section { padding: 36px 40px; }
  .section h2 { font-size: 1.3rem; font-weight: 600; margin-bottom: 24px; border-left: 4px solid #6366f1; padding-left: 12px; }
  /* Cards */
  .cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 16px; margin-bottom: 40px; }
  .card { background: #1e293b; border-radius: 12px; padding: 18px; text-align: center; border: 1px solid #334155; transition: transform .2s; }
  .card:hover { transform: translateY(-4px); border-color: #6366f1; }
  .card .model-name { font-size: .8rem; color: #94a3b8; margin-bottom: 10px; }
  .card .big-num { font-size: 2rem; font-weight: 700; color: #a5b4fc; }
  .card .label { font-size: .7rem; color: #64748b; margin-top: 2px; }
  .card.best { border-color: #22c55e; }
  .card.best .big-num { color: #4ade80; }
  /* Charts */
  .chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
  .chart-box { background: #1e293b; border-radius: 12px; padding: 24px; border: 1px solid #334155; }
  .chart-box h3 { font-size: 1rem; margin-bottom: 16px; color: #94a3b8; }
  /* ROC plots */
  .roc-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }
  .roc-card { background: #1e293b; border-radius: 12px; padding: 16px; border: 1px solid #334155; }
  .roc-card h3 { font-size: .85rem; color: #94a3b8; margin-bottom: 12px; text-align: center; }
  .roc-card img { width: 100%; border-radius: 8px; }
  /* Table */
  table { width: 100%; border-collapse: collapse; }
  th { background: #1e293b; padding: 12px 16px; text-align: left; font-size: .8rem; color: #64748b; text-transform: uppercase; letter-spacing: .05em; }
  td { padding: 12px 16px; border-bottom: 1px solid #1e293b; font-size: .9rem; }
  tr:hover td { background: #1e293b; }
  .badge { display:inline-block; padding:2px 8px; border-radius:999px; font-size:.75rem; font-weight:600; }
  .badge-green { background:#14532d; color:#4ade80; }
  .badge-blue  { background:#1e3a5f; color:#60a5fa; }
  .badge-gray  { background:#1e293b; color:#64748b; }
  @media(max-width:700px){ .chart-grid{grid-template-columns:1fr;} }
</style>
</head>
<body>
<header>
  <h1>🩺 Diabetes Prediction — ML Dashboard</h1>
  <p>Dataset: 100,000 records &nbsp;|&nbsp; SMOTE balanced &nbsp;|&nbsp; 9 Models compared</p>
</header>

<!-- ACCURACY CARDS -->
<div class="section">
  <h2>Model Accuracy Overview</h2>
  <div class="cards">
    {% for m in models %}
    <div class="card {{ 'best' if m.accuracy == best_acc else '' }}">
      <div class="model-name">{{ m.name }}</div>
      <div class="big-num">{{ "%.1f"|format(m.accuracy*100) if m.accuracy else "—" }}%</div>
      <div class="label">Accuracy{% if m.accuracy == best_acc %} 🏆{% endif %}</div>
    </div>
    {% endfor %}
  </div>

  <!-- BAR CHARTS -->
  <div class="chart-grid">
    <div class="chart-box">
      <h3>Accuracy &amp; F1-Score</h3>
      <canvas id="barAcc"></canvas>
    </div>
    <div class="chart-box">
      <h3>ROC-AUC Score</h3>
      <canvas id="barAuc"></canvas>
    </div>
  </div>
</div>

<!-- METRICS TABLE -->
<div class="section">
  <h2>Full Metrics Table</h2>
  <table>
    <thead>
      <tr><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>ROC-AUC</th></tr>
    </thead>
    <tbody>
      {% for m in models %}
      <tr>
        <td>{{ m.name }}</td>
        <td>{% if m.accuracy %}<span class="badge {{ 'badge-green' if m.accuracy >= 0.96 else 'badge-blue' }}">{{ "%.4f"|format(m.accuracy) }}</span>{% else %}—{% endif %}</td>
        <td>{{ "%.4f"|format(m.precision) if m.precision else "—" }}</td>
        <td>{{ "%.4f"|format(m.recall) if m.recall else "—" }}</td>
        <td>{{ "%.4f"|format(m.f1) if m.f1 else "—" }}</td>
        <td>{{ "%.4f"|format(m.roc_auc) if m.roc_auc else "—" }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>

<!-- ROC CURVE PLOTS -->
<div class="section">
  <h2>ROC Curve Plots</h2>
  <div class="roc-grid">
    {% for m in models %}
    {% if m.plot and m.img %}
    <div class="roc-card">
      <h3>{{ m.name }}</h3>
      <img src="data:image/png;base64,{{ m.img }}" alt="{{ m.name }} ROC">
    </div>
    {% endif %}
    {% endfor %}
  </div>
</div>

<!-- ANN TRAINING PLOTS -->
{% if ann_acc_img or ann_loss_img %}
<div class="section">
  <h2>ANN Training Curves</h2>
  <div class="chart-grid">
    {% if ann_acc_img %}
    <div class="roc-card">
      <h3>Accuracy over Epochs</h3>
      <img src="data:image/png;base64,{{ ann_acc_img }}" alt="ANN Accuracy">
    </div>
    {% endif %}
    {% if ann_loss_img %}
    <div class="roc-card">
      <h3>Loss over Epochs</h3>
      <img src="data:image/png;base64,{{ ann_loss_img }}" alt="ANN Loss">
    </div>
    {% endif %}
  </div>
</div>
{% endif %}

<script>
const labels = {{ chart_labels | tojson }};
const accData = {{ chart_acc | tojson }};
const f1Data  = {{ chart_f1  | tojson }};
const aucData = {{ chart_auc | tojson }};

const colors = [
  '#6366f1','#22d3ee','#f59e0b','#ec4899','#10b981','#3b82f6','#a855f7','#f97316','#14b8a6'
];

new Chart(document.getElementById('barAcc'), {
  type: 'bar',
  data: {
    labels,
    datasets: [
      { label: 'Accuracy', data: accData, backgroundColor: colors.map(c => c + 'cc'), borderColor: colors, borderWidth: 1.5, borderRadius: 5 },
      { label: 'F1-Score', data: f1Data,  backgroundColor: colors.map(c => c + '55'), borderColor: colors, borderWidth: 1.5, borderRadius: 5 }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend: { labels: { color: '#94a3b8' } } },
    scales: {
      x: { ticks: { color: '#64748b', font: { size: 10 } }, grid: { color: '#1e293b' } },
      y: { min: 0.75, max: 1.0, ticks: { color: '#64748b' }, grid: { color: '#334155' } }
    }
  }
});

new Chart(document.getElementById('barAuc'), {
  type: 'bar',
  data: {
    labels,
    datasets: [
      { label: 'ROC-AUC', data: aucData, backgroundColor: colors.map(c => c + 'bb'), borderColor: colors, borderWidth: 1.5, borderRadius: 5 }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend: { labels: { color: '#94a3b8' } } },
    scales: {
      x: { ticks: { color: '#64748b', font: { size: 10 } }, grid: { color: '#1e293b' } },
      y: { min: 0.88, max: 1.0, ticks: { color: '#64748b' }, grid: { color: '#334155' } }
    }
  }
});
</script>
</body>
</html>
"""

@app.route('/')
def index():
    best_acc = max((m['accuracy'] for m in MODELS if m['accuracy']), default=0)
    for m in MODELS:
        if m['plot']:
            m['img'] = img_b64(m['plot'])
        else:
            m['img'] = None

    chart_labels = [m['name'] for m in MODELS if m['accuracy']]
    chart_acc    = [round(m['accuracy'], 4) for m in MODELS if m['accuracy']]
    chart_f1     = [round(m['f1'], 4) if m['f1'] else None for m in MODELS if m['accuracy']]
    chart_auc    = [round(m['roc_auc'], 4) if m['roc_auc'] else None for m in MODELS if m['accuracy']]

    ann_acc_img  = img_b64('ann_accuracy.png')
    ann_loss_img = img_b64('ann_loss.png')

    return render_template_string(
        HTML,
        models=MODELS,
        best_acc=best_acc,
        chart_labels=chart_labels,
        chart_acc=chart_acc,
        chart_f1=chart_f1,
        chart_auc=chart_auc,
        ann_acc_img=ann_acc_img,
        ann_loss_img=ann_loss_img,
    )

if __name__ == '__main__':
    app.run(debug=False, port=5000)
