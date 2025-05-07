import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import os
import secrets
from flask_bootstrap import Bootstrap

from services.openrouter_service import OpenRouterService
from prompt import PDF_EXTRACTION_PROMPT

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

Bootstrap(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

openrouter_controller = OpenRouterService()

PROMPT_FILE = "prompt.json"

@app.route('/')
def home():
    prompt = ""
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            prompt_data = json.load(f)
            prompt = prompt_data.get("pdf_extraction_prompt", "")

    return render_template('home.html', current_prompt=prompt)

@app.route("/update-prompt", methods=["POST"])
def update_prompt():
    prompt = request.form.get("prompt")

    if not prompt:
        return jsonify({"error": "Missing 'prompt' in request"}), 400

    try:
        prompt_data = {}
        if os.path.exists(PROMPT_FILE):
            with open(PROMPT_FILE, "r", encoding="utf-8") as f:
                prompt_data = json.load(f)

        if prompt_data["pdf_extraction_prompt"] == prompt:
            return redirect(url_for('home'))
        else:    
            prompt_data["pdf_extraction_prompt"] = prompt

            with open(PROMPT_FILE, "w", encoding="utf-8") as f:
                json.dump(prompt_data, f, indent=4)

            flash("Prompt updated successfully")
            return redirect(url_for('home'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        flash('No file part')
        return redirect(url_for('home'))

    file = request.files['pdf_file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('home'))

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        convert_pdf_to_csv(file_path)
        
        flash('File successfully uploaded and processed.')
        return redirect(url_for('home'))
    else:
        flash('Only PDF files are allowed!')
        return redirect(url_for('home'))
    
def convert_pdf_to_csv(filepath):
    summary = openrouter_controller.pdf_extraction_request(message=PDF_EXTRACTION_PROMPT, pdf_path=filepath)
    print(f"We cooking at path: {filepath}!")
    print(summary)

if __name__ == '__main__':
    app.run(debug=True)