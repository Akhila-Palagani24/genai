import os
import json
import re
from flask import Flask, render_template, request, jsonify
from google import genai
import PyPDF2
from werkzeug.utils import secure_filename

# ==============================
# CONFIG
# ==============================
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Use your key here
client = genai.Client(api_key="AIzaSyDHe-07Vh_9e8rQEwEHvrXJFiWX7Yv75aw")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Extraction Error: {e}")
    return text

@app.route('/')
def home():
    # Make sure your file is named index1.html in the templates folder
    return render_template('index1.html')

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "Please upload a resume"}), 400

        resume_file = request.files["resume"]
        
        # Save and Extract
        filename = secure_filename(resume_file.filename)
        pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        resume_file.save(pdf_path)
        resume_text = extract_text_from_pdf(pdf_path)

        if not resume_text.strip():
            return jsonify({"error": "Could not read text from PDF. Ensure it is not an image."}), 400

        # Prompt for Audit
        prompt = f"""
        You are a professional Resume Auditor. Analyze this resume:
        {resume_text}
        
        Return ONLY a JSON object with this structure:
        {{
            "score": 85,
            "found": ["Python", "Flask"],
            "missing": ["Docker"],
            "strengths": ["Clear experience"],
            "weaknesses": ["Missing cloud skills"],
            "suggestions": "Add certification"
        }}
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        
        # --- ROBUST JSON EXTRACTION ---
        raw_text = response.text
        # This regex finds anything between { and } to avoid markdown errors
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        
        if json_match:
            clean_json = json_match.group(0)
            return jsonify(json.loads(clean_json))
        else:
            print(f"AI Response failed to provide JSON: {raw_text}")
            return jsonify({"error": "AI response format error"}), 500

    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)