import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# This function gets the token for the API
def get_access_token():
    api_key = os.getenv("IBM_CLOUD_API_KEY")
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}"
    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

@app.route('/scribe', methods=['POST'])
def scribe_logic():
    # 1. Get transcript from Orchestrate
    user_input = request.json.get('transcript', '')
    token = get_access_token()
    
    # 2. Prepare the watsonx.ai request (Using your snippet logic)
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    body = {
        "messages": [
            {"role": "system", "content": "You are a medical scribe. Provide a SOAP note and Spanish translation for the following intake."},
            {"role": "user", "content": user_input}
        ],
        "project_id": os.getenv("WATSONX_PROJECT_ID"),
        "model_id": "ibm/granite-3-8b-instruct",
        "max_tokens": 1000,
        "temperature": 0
    }

    # 3. Call the Granite Model
    response = requests.post(url, headers=headers, json=body)
    ai_output = response.json()['choices'][0]['message']['content']

    # 4. Return the "Innovative" result back to Orchestrate
    return jsonify({
        "summary": ai_output,
        "status": "Logged to Cloudant"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)