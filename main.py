from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files like images
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <html>
    <head>
        <title>GREYLOCK Fraud Detector</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
            body {
                margin: 0;
                background-color: #0d0d0d;
                color: #00ff00;
                font-family: 'Courier New', Courier, monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 30px;
            }
            .banner {
                position: relative;
                width: 100%;
                max-width: 900px;
                padding: 40px 20px;
                background: linear-gradient(135deg, #001100, #004400);
                border-radius: 15px;
                box-shadow: 0 0 15px #00ff00aa;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 20px;
                overflow: hidden;
                user-select: none;
            }
            .banner h1 {
                font-family: 'Orbitron', sans-serif;
                font-size: 3.5rem;
                margin: 0;
                letter-spacing: 5px;
                color: #00ff00;
                text-shadow: 0 0 10px #00ff00bb;
                white-space: nowrap;
                z-index: 2;
            }
            .banner img.lock-icon {
                width: 80px;
                height: 80px;
                filter: drop-shadow(0 0 6px #00ff00cc);
                z-index: 2;
            }
            .binary-bg {
                position: absolute;
                top: 0;
                left: 100%;
                width: 300%;
                height: 100%;
                font-size: 2rem;
                color: #00880088;
                font-family: monospace;
                white-space: nowrap;
                line-height: 80px;
                animation: scrollBinary 20s linear infinite;
                user-select: none;
                z-index: 1;
            }
            @keyframes scrollBinary {
                0% { transform: translateX(0); }
                100% { transform: translateX(-66.66%); }
            }
            form {
                margin-top: 40px;
                background-color: #111;
                padding: 25px 30px;
                border-radius: 12px;
                width: 350px;
                box-shadow: 0 0 15px #00ff00aa;
                color: #00ff00;
                font-size: 1.1rem;
            }
            label {
                display: block;
                margin-top: 15px;
            }
            input[type="text"] {
                width: 100%;
                padding: 8px 10px;
                margin-top: 6px;
                border: none;
                border-radius: 6px;
                background-color: #0a0a0a;
                color: #0f0;
                font-family: monospace;
                font-size: 1rem;
                box-sizing: border-box;
            }
            input[type="submit"] {
                margin-top: 25px;
                width: 100%;
                padding: 12px;
                font-size: 1.3rem;
                font-weight: 700;
                background-color: #00cc00;
                color: #000;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            input[type="submit"]:hover {
                background-color: #009900;
            }
            a {
                color: #00ff00;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
            .result-container {
                margin-top: 40px;
                background-color: #111;
                padding: 25px 30px;
                border-radius: 12px;
                width: 400px;
                box-shadow: 0 0 15px #00ff00aa;
                color: #00ff00;
                font-size: 1.2rem;
                font-family: monospace;
            }
            .result-container h2 {
                margin-top: 0;
                text-align: center;
                font-family: 'Orbitron', sans-serif;
                font-size: 2rem;
            }
        </style>
    </head>
    <body>
        <div class="banner">
            <img src="/static/lock.png" alt="Lock Icon" class="lock-icon" />
            <h1>GREYLOCK Fraud Detector</h1>
            <div class="binary-bg">
                01001100 01101111 01100011 01101011 01100101 01100100 00100000 01000110 01110010 01100001 01110101 01100100 00100000 01000100 01100101 01110100 01100101 01100011 01110100 01101001 01101111 01101110 &nbsp;
                01001100 01101111 01100011 01101011 01100101 01100100 00100000 01000110 01110010 01100001 01110101 01100100 00100000 01000100 01100101 01110100 01100101 01100011 01110100 01101001 01101111 01101110 &nbsp;
                01001100 01101111 01100011 01101011 01100101 01100100 00100000 01000110 01110010 01100001 01110101 01100100 00100000 01000100 01100101 01110100 01100101 01100011 01110100 01101001 01101111 01101110 &nbsp;
            </div>
        </div>

        <form action="/predict" method="post">
            <label>Transaction Amount:
                <input type="text" name="amount" required />
            </label>
            <label>Feature V1:
                <input type="text" name="v1" required />
            </label>
            <label>Feature V2:
                <input type="text" name="v2" required />
            </label>
            <input type="submit" value="Check Fraud" />
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/predict", response_class=HTMLResponse)
async def predict(amount: str = Form(...), v1: str = Form(...), v2: str = Form(...)):
    # Dummy prediction logic — replace with your model later
    fraud_prob = 0.85
    result_text = "🚨 Fraud Detected!" if fraud_prob > 0.5 else "✅ Legitimate Transaction"
    
    html_content = f"""
    <html>
    <head>
        <title>Prediction Result - GREYLOCK</title>
        <style>
            body {{
                background-color: #0d0d0d;
                color: #00ff00;
                font-family: 'Courier New', Courier, monospace;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                padding: 20px;
            }}
            .result-container {{
                background-color: #111;
                padding: 30px 40px;
                border-radius: 15px;
                box-shadow: 0 0 20px #00ff00aa;
                max-width: 400px;
                width: 100%;
                text-align: center;
            }}
            h2 {{
                font-family: 'Orbitron', sans-serif;
                font-size: 2.2rem;
                margin-bottom: 25px;
            }}
            p {{
                font-size: 1.2rem;
                margin: 10px 0;
            }}
            a {{
                color: #00ff00;
                font-weight: bold;
                text-decoration: none;
                display: inline-block;
                margin-top: 25px;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="result-container">
            <h2>Prediction Result</h2>
            <p><strong>Transaction Amount:</strong> {amount}</p>
            <p><strong>Feature V1:</strong> {v1}</p>
            <p><strong>Feature V2:</strong> {v2}</p>
            <h3>{result_text}</h3>
            <a href="/">&#8592; Check Another Transaction</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)