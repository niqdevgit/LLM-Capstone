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

K2XML_DIR = "/k2xml"
XML_FILE_PATH = os.path.join(K2XML_DIR, "input.xml")

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

    generated_text = response.json()

    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
                        <root>
                            <data>{generated_text}</data>
                        </root>"""

    os.makedirs(K2XML_DIR, exist_ok=True)

    with open(XML_FILE_PATH, "w", encoding="utf-8") as xml_file:
        xml_file.write(xml_content)


    def run_k2xml():
        print('first')
        process = subprocess.run(["timeout", "5s", "mono", "/app/k2xml/K2XML_Converter.exe"], capture_output=True, text=True)
        print('subprosess')
        print(process.stdout)
        return process.stdout

    print('before func call')
    k2result = run_k2xml()
    if "Data at the root level is invalid" not in k2result:
        k2xml_status = False
    else:
        k2xml_status = True

    hf_response = response.json()

    # Create a new response object including k2xml status
    final_response = {
        "generated_text": hf_response[0].get("generated_text", ""),
        "k2xml": k2xml_status
    }

    return jsonify(final_response), 200

    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")