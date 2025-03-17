from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all CORS

# Load API key from environment variable (for security)
HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL_URL = "https://api-inference.huggingface.co/models/niklassuvitie/gpt2-medium-ipxact"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def validate_with_kactus2(xml_content):
    """
    Validates the generated IP-XACT component using Kactus2.
    Assumes kactus2-cli is installed and available in PATH.
    """
    try:
        with open("generated_component.xml", "w") as f:
            f.write(xml_content)
        
        # Run Kactus2 validation
        result = subprocess.run(["kactus2-cli", "validate", "generated_component.xml"],
                                capture_output=True, text=True)
        
        if result.returncode == 0:
            return True, "Component is valid"
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("description", "")
    print(prompt)
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    response = requests.post(HF_MODEL_URL, headers=headers, json={"inputs": prompt})
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to generate response", "details": response.text}), 500
    
    #generated_component = response.json()
    #xml_content = generated_component.get("generated_xml", "")
    
    #if not xml_content:
    #    return jsonify({"error": "Model did not return a valid XML component"}), 500
    
    #is_valid, validation_message = validate_with_kactus2(xml_content)
    
    #if not is_valid:
    #    return jsonify({"error": "Generated component is invalid", "details": validation_message}), 400
    
    #return jsonify({"component": xml_content, "validation": validation_message})
    return jsonify(response.json()), 200

    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")