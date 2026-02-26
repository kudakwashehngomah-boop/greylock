from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np
import joblib
import os

app = FastAPI()

# ==========================
# LOAD MODEL + DATASETS
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "fraud_model.pkl")
CREDIT_PATH = os.path.join(BASE_DIR, "model", "creditcard.csv")
INSURANCE_PATH = os.path.join(BASE_DIR, "model", "insurance.csv")

model = joblib.load(MODEL_PATH)
credit_data = pd.read_csv(CREDIT_PATH)

# Safe insurance loading
if os.path.exists(INSURANCE_PATH):
    insurance_data = pd.read_csv(INSURANCE_PATH)
else:
    insurance_data = pd.DataFrame({
        "ClaimAmount":[5000,20000,40000],
        "NumClaims":[1,2,5],
        "FraudReported":[0,0,1]
    })

# ==========================
# GLOBAL STYLE + MATRIX JS
# ==========================
STYLE = """
<style>
body {
    margin:0;
    background: radial-gradient(circle at center, #050505 0%, #000000 70%);
    color:#00ffcc;
    font-family: 'Courier New', monospace;
    overflow:hidden;
}

/* MATRIX */
canvas {
    position:fixed;
    top:0;
    left:0;
    z-index:-1;
}

/* GLITCH TITLE */
.title {
    text-align:center;
    font-size:120px;
    margin-top:80px;
    letter-spacing:15px;
    animation:flicker 2s infinite alternate;
}

@keyframes flicker {
    from { text-shadow:0 0 10px #00ffcc; }
    to { text-shadow:0 0 40px #00ffcc; }
}

/* GLASS CARD */
.card {
    width:420px;
    margin:40px auto;
    padding:30px;
    background:rgba(0,255,204,0.05);
    border:1px solid rgba(0,255,204,0.3);
    border-radius:20px;
    backdrop-filter: blur(10px);
    box-shadow:0 0 40px rgba(0,255,204,0.2);
    text-align:center;
    transition:0.4s;
}

.card:hover {
    transform:scale(1.05);
}

input {
    width:90%;
    padding:12px;
    margin:10px 0;
    background:#111;
    border:1px solid #00ffcc;
    color:#00ffcc;
    border-radius:8px;
}

button {
    padding:12px 30px;
    background:#00ffcc;
    color:black;
    border:none;
    border-radius:8px;
    font-weight:bold;
    cursor:pointer;
    transition:0.3s;
}

button:hover {
    background:white;
    transform:scale(1.1);
}

.button {
    padding:12px 30px;
    border:2px solid #00ffcc;
    color:#00ffcc;
    text-decoration:none;
    display:inline-block;
    margin-top:20px;
    border-radius:10px;
    transition:0.3s;
}

.button:hover {
    background:#00ffcc;
    color:black;
}

.progress {
    width:100%;
    height:25px;
    background:#111;
    border-radius:20px;
    margin-top:15px;
    overflow:hidden;
}

.progress-bar {
    height:100%;
    background:linear-gradient(90deg,#00ffcc,#00ff66);
    width:0%;
    transition:width 1s ease-in-out;
}
</style>

<canvas id="matrix"></canvas>
<script>
var c = document.getElementById("matrix");
var ctx = c.getContext("2d");
c.height = window.innerHeight;
c.width = window.innerWidth;
var letters = "01";
letters = letters.split("");
var fontSize = 14;
var columns = c.width/fontSize;
var drops = [];
for(var x = 0; x < columns; x++)
    drops[x] = 1;
function draw() {
    ctx.fillStyle = "rgba(0,0,0,0.05)";
    ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle = "#00ffcc";
    ctx.font = fontSize + "px monospace";
    for(var i=0; i<drops.length; i++) {
        var text = letters[Math.floor(Math.random()*letters.length)];
        ctx.fillText(text,i*fontSize,drops[i]*fontSize);
        if(drops[i]*fontSize > c.height && Math.random() > 0.975)
            drops[i] = 0;
        drops[i]++;
    }
}
setInterval(draw,33);
</script>
"""

# ==========================
# HOME
# ==========================
@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(f"""
    {STYLE}
    <div class="title">GRAYLOCK</div>
    <div class="card">
        <h2>AI FRAUD INTELLIGENCE SYSTEM</h2>
        <a href="/credit" class="button">Credit Fraud Scanner</a><br>
        <a href="/insurance" class="button">Insurance Fraud Scanner</a>
    </div>
    """)

# ==========================
# CREDIT PAGE
# ==========================
@app.get("/credit", response_class=HTMLResponse)
async def credit_page():
    return HTMLResponse(f"""
    {STYLE}
    <div class="card">
        <h2>Credit Fraud Detection</h2>
        <form action="/credit-predict" method="post">
            <input name="amount" placeholder="Transaction Amount" required>
            <input name="v1" placeholder="Feature V1" required>
            <input name="v2" placeholder="Feature V2" required>
            <button type="submit">Scan Transaction</button>
        </form>
        <a href="/" class="button">Back</a>
    </div>
    """)

@app.post("/credit-predict", response_class=HTMLResponse)
async def credit_predict(amount: float = Form(...),
                         v1: float = Form(...),
                         v2: float = Form(...)):

    features = np.array([[amount, v1, v2]])
    fraud_prob = model.predict_proba(features)[0][1]
    percentage = int(fraud_prob * 100)

    small_tx_count = len(credit_data[credit_data["Amount"] < 50])

    if amount < 50 and small_tx_count > 100:
        result = "🧨 SALAMI SLICING FRAUD DETECTED"
    elif fraud_prob > 0.75:
        result = "🚨 HIGH RISK FRAUD"
    elif fraud_prob > 0.5:
        result = "⚠️ SUSPICIOUS TRANSACTION"
    else:
        result = "✅ LEGITIMATE TRANSACTION"

    return HTMLResponse(f"""
    {STYLE}
    <div class="card">
        <h2>AI SCAN RESULT</h2>
        <h3>{result}</h3>
        <p>Fraud Probability: {percentage}%</p>
        <div class="progress">
            <div class="progress-bar" style="width:{percentage}%"></div>
        </div>
        <a href="/credit" class="button">Back</a>
    </div>
    """)

# ==========================
# INSURANCE PAGE
# ==========================
@app.get("/insurance", response_class=HTMLResponse)
async def insurance_page():
    return HTMLResponse(f"""
    {STYLE}
    <div class="card">
        <h2>Insurance Fraud Detection</h2>
        <form action="/insurance-predict" method="post">
            <input name="claim" placeholder="Claim Amount" required>
            <input name="numclaims" placeholder="Number of Claims" required>
            <button type="submit">Scan Claim</button>
        </form>
        <a href="/" class="button">Back</a>
    </div>
    """)

@app.post("/insurance-predict", response_class=HTMLResponse)
async def insurance_predict(claim: float = Form(...),
                            numclaims: int = Form(...)):

    avg_claim = insurance_data["ClaimAmount"].mean()

    if claim > avg_claim * 2 and numclaims > 3:
        result = "🚨 INSURANCE FRAUD DETECTED"
    else:
        result = "✅ CLAIM NORMAL"

    return HTMLResponse(f"""
    {STYLE}
    <div class="card">
        <h2>AI SCAN RESULT</h2>
        <h3>{result}</h3>
        <a href="/insurance" class="button">Back</a>
    </div>
    """)