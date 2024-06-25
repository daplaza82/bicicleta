from flask import Flask, request, jsonify, render_template
import urllib.request
import json
import os
import ssl
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

app = Flask(__name__)

def allowSelfSignedHttps(allowed):
    # Bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)  # This line is needed if you use self-signed certificate in your scoring service.

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from request
    user_data = request.json

    # Prepare the data for the Azure ML endpoint
    data = {"Inputs": {"data": [user_data]}, "GlobalParameters": 1.0}
    body = str.encode(json.dumps(data))

    url = 'http://2f1592b3-57aa-4905-8783-5dfa709b497f.centralus.azurecontainer.io/score'
    api_key = 'D7rJmF2GTCwnWmC39JJGDnxAyig5vDPd'  # Replace this with the API key for the web service

    if not api_key:
        return jsonify({"error": "A key should be provided to invoke the endpoint"}), 400

    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return result, 200
    except urllib.error.HTTPError as error:
        error_message = f"The request failed with status code: {error.code}\n"
        error_message += f"Headers: {error.info()}\n"
        error_message += error.read().decode("utf8", 'ignore')
        return jsonify({"error": error_message}), error.code

@app.route('/health')
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
