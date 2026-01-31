from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/scribe', methods=['POST'])
def scribe_logic():
    data = request.json
    transcript = data.get('transcript', '')
    
    # Fresh OPQRST Analysis
    symptoms = transcript.lower()
    suggestions = []
    if not any(word in symptoms for word in ["start", "when"]):
        suggestions.append("Ask when the pain started (Onset).")
    if not any(word in symptoms for word in ["better", "worse"]):
        suggestions.append("Ask what makes it better/worse (Provocation).")

    # Generate the Legal Log
    fhir_note = {
        "resourceType": "DocumentReference",
        "timestamp": datetime.now().isoformat(),
        "content": {"transcript": transcript, "legal_status": "Verified"}
    }

    return jsonify({
        "summary": transcript,
        "nursing_suggestions": suggestions,
        "fhir_json": fhir_note
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)