from flask import Flask, request, jsonify
import requests
import re
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "Dark OSINT Proxy running on Render 🚀"
    })

@app.route('/lookup', methods=['GET'])
def lookup():
    phone = request.args.get('mobile', '').strip()

    # Validate phone number (10 digits)
    if not re.fullmatch(r'\d{10}', phone):
        return jsonify({"error": "Please provide a valid 10-digit phone number"}), 400

    upstream_url = f"https://seller-ki-mkc.taitanx.workers.dev/?mobile={phone}"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; DarkOSINTProxy/1.0)",
            "Accept": "application/json"
        }

        # Request to upstream
        resp = requests.get(upstream_url, headers=headers, timeout=15, verify=True)

        # Forward the response as-is
        return (resp.text, resp.status_code, {"Content-Type": "application/json"})

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to connect to upstream API",
            "details": str(e)
        }), 502


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
