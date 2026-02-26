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
    margin: 0;
    color: #00ff99;
    font-family: 'Courier New', monospace;
    overflow: hidden;
    background: none;
}


body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;

    background: url('https://th.bing.com/th/id/OIP.GN6pJxkDWaTA0ZGB42RY1AHaFj?w=148&h=180&c=7&r=0&o=7&dpr=1.1&pid=1.7&rm=3')
                center center / cover no-repeat;

    filter: brightness(50%) contrast(120%);
    z-index: -2;
}

/* MATRIX CANVAS */
canvas {
    position: fixed;
    top: 0;
    left: 0;
    z-index: -1;
}
/* FULL SCREEN MATRIX */
canvas {
    position:fixed;
    top:0;
    left:0;
    z-index:-1;
}

/* TITLE */
.title {
    text-align:center;
    font-size:100px;
    margin-top:60px;
    letter-spacing:12px;
    text-shadow:0 0 20px #00ff99;
}

/* CARD */
.card {
    width: 420px;
    margin: 40px auto;
    padding: 30px;
    background: rgba(0, 0, 0, 0.3); /* light glass, not solid */
    backdrop-filter: blur(8px);
    border: 1px solid #00ff99;
    box-shadow: 0 0 40px rgba(0,255,153,0.6);
    text-align: center;
}

.card:hover {
    box-shadow:0 0 40px rgba(0,255,153,0.7);
}

/* INPUTS */
input {
    width:90%;
    padding:12px;
    margin:12px 0;
    background:black;
    border:1px solid #00ff99;
    color:#00ff99;
    border-radius:0px;
    outline:none;
}

input:focus {
    box-shadow:0 0 10px #00ff99;
}

/* BUTTON */
button {
    padding:12px 30px;
    background:black;
    color:#00ff99;
    border:1px solid #00ff99;
    border-radius:0px;
    cursor:pointer;
    transition:0.3s;
}

button:hover {
    background:#00ff99;
    color:black;
}

.button {
    padding:12px 30px;
    border:1px solid #00ff99;
    color:#00ff99;
    text-decoration:none;
    display:inline-block;
    margin-top:20px;
    border-radius:0px;
}

.button:hover {
    background:#00ff99;
    color:black;
}

.progress {
    width:100%;
    height:20px;
    background:black;
    border:1px solid #00ff99;
    margin-top:15px;
}

.progress-bar {
    height:100%;
    background:#00ff99;
    width:0%;
    transition:width 1s ease-in-out;
    
 @keyframes screenFlicker {
    0% { opacity: 1; }
    50% { opacity: 0.97; }
    100% { opacity: 1; }
}

body {
    animation: screenFlicker 0.15s infinite;
}
}
</style>

<canvas id="matrix"></canvas>

<script>
var c = document.getElementById("matrix");
var ctx = c.getContext("2d");

c.height = window.innerHeight;
c.width = window.innerWidth;

let modeIndex = 0;
const modes = [
    "01",                                   // A - Binary
    "0123456789ABCDEF",                     // B - Hex
    "!@#$%^&*(){}[]<>?/|+-=",               // C - Symbols
    "01GRAYLOCK"                            // D - Brand mix
];

let letters = modes[modeIndex].split("");
let fontSize = 14;
let columns = c.width / fontSize;
let drops = [];

for (let x = 0; x < columns; x++)
    drops[x] = 1;

// Change mode every 10 seconds
setInterval(() => {
    modeIndex = (modeIndex + 1) % modes.length;
    letters = modes[modeIndex].split("");
}, 10000);

function draw() {
    ctx.fillStyle = "rgba(0,0,0,0.08)";
    ctx.fillRect(0,0,c.width,c.height);

    ctx.fillStyle = "#00ff99";
    ctx.font = fontSize + "px monospace";

    for (let i=0; i<drops.length; i++) {
        let text = letters[Math.floor(Math.random()*letters.length)];
        ctx.fillText(text, i*fontSize, drops[i]*fontSize);

        if (drops[i]*fontSize > c.height && Math.random() > 0.975)
            drops[i] = 0;

        drops[i]++;
    }
}

setInterval(draw,33);

function playBeep() {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = ctx.createOscillator();
    const gainNode = ctx.createGain();

    oscillator.type = "square";
    oscillator.frequency.setValueAtTime(800, ctx.currentTime);
    gainNode.gain.setValueAtTime(0.05, ctx.currentTime);

    oscillator.connect(gainNode);
    gainNode.connect(ctx.destination);

    oscillator.start();
    oscillator.stop(ctx.currentTime + 0.1);
}

// Random eerie beeps every 3-8 seconds
setInterval(() => {
    if (Math.random() > 0.5) {
        playBeep();
    }
}, Math.random() * 5000 + 3000);


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

    avg_claim = insurance_data["total_claim_amount"].mean()

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