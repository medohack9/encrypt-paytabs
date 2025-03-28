from flask import Flask, request
import subprocess

app = Flask(__name__)

def run_js_script(card_number, expiry_month, expiry_year, cvv, key, csrf):
    js_code = f'''
    const CryptoJS = require("crypto-js");
    let t = {{
        "clientKey": "{key}",
        "currency": "EGP",
        "payment": {{
            "method": "card",
            "cardNumber": "{card_number}",
            "expiryMonth": "{expiry_month}",
            "expiryYear": "{expiry_year}",
            "cvv": "{cvv}"
        }},
        "device": {{
            "screenWidth": 1366,
            "screenHeight": 768,
            "colorDepth": 24,
            "timezoneOffset": -120
        }},
        "extra": {{
            "method": "CC"
        }}
    }};
    
    t = JSON.stringify(t);
    
    let a = {{
        k: "{key}",
        v: CryptoJS.AES.encrypt(t, "{csrf}").toString()
    }};
    
    console.log(JSON.stringify(a));
    '''
    
    with open("encrypt.js", "w") as f:
        f.write(js_code)
    
    result = subprocess.run(["node", "encrypt.js"], capture_output=True, text=True)
    return result.stdout.strip()

@app.route("/encrypt", methods=["GET"])
def encrypt():
    card_number = request.args.get("cc")
    expiry_month = request.args.get("mes")
    expiry_year = request.args.get("ano")
    cvv = request.args.get("cvv")
    key = request.args.get("key")
    csrf = request.args.get("csrf")
    
    if not all([card_number, expiry_month, expiry_year, cvv, key, csrf]):
        return "Missing required parameters", 400
    
    return run_js_script(card_number, expiry_month, expiry_year, cvv, key, csrf)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
    app.run(debug=True)
