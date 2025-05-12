import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import os
import secrets
from flask_bootstrap import Bootstrap

import json
import csv

from services.openrouter_service import OpenRouterService

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

Bootstrap(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

openrouter_controller = OpenRouterService()

CONFIG_FILE = "prompt.json"

@app.route('/')
def home():
    prompt = ""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            prompt_data = json.load(f)
            prompt = prompt_data.get("pdf_extraction_prompt", "")
            model = prompt_data.get("pdf_extraction_model", "")

    return render_template('home.html', current_prompt=prompt, current_model=model)

@app.route("/update-prompt", methods=["POST"])
def update_prompt():
    prompt = request.form.get("prompt")

    if not prompt:
        return jsonify({"error": "Missing 'prompt' in request"}), 400

    try:
        prompt_data = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                prompt_data = json.load(f)

        if prompt_data["pdf_extraction_prompt"] == prompt:
            return redirect(url_for('home'))
        else:    
            prompt_data["pdf_extraction_prompt"] = prompt

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(prompt_data, f, indent=4)

            flash("Prompt updated successfully")
            return redirect(url_for('home'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update-model", methods=["POST"])
def update_model():
    model = request.form.get("model")

    try:
        config_data = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config_data = json.load(f)

        if config_data["pdf_extraction_model"] == model:
            return redirect(url_for('home'))
        else:    
            config_data["pdf_extraction_model"] = model

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4)

            flash("Model updated successfully")
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
    prompt_data = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            prompt_data = json.load(f)

    prompt = prompt_data["pdf_extraction_prompt"]
    model = prompt_data["pdf_extraction_model"]
    summary = openrouter_controller.pdf_extraction_request_structured_output(message=prompt, model=model, pdf_path=filepath)
    print(f"We cooking at path: {filepath}!")
    json_data = summary["choices"][0]["message"]["content"]
    print(type(json_data))
    json_data = json.loads(json_data)
    print(json_data.keys())
    convert_questionnaire_json_to_csv(json_data=json_data)

def convert_questionnaire_json_to_csv(json_data: dict, output_path: str = "weguide_formatted.csv"):
    """
    Converteert een vragenlijst in JSON (WeGuide-formaat) naar een CSV-bestand
    conform de vereisten van het WeGuide-importsysteem.
    """

    # Define header fields as per the CSV import structure
    questionnaire_header_fields = [
        "id", "external_id", "calculation_type", "route_to_after_completion",
        "title", "subtitle", "description", "celebrate", "celebrate_text", "confetti",
        "default_language", "show_question", "disable_progress_bar",
        "instructions_header", "instructions_back_button", "instructions_next_button",
        "survey_id", "new", "allow_instructions", "supported_languages"
    ]

    questionnaire_metadata_fields = [
        "questionnaire_instructions", "calculated_variables",
        "data_points", "question_groups"
    ]

    question_fields = [
        "id", "external_id", "type", "minimum", "maximum", "default_value", "step",
        "minimum_length", "maximum_length", "mandatory", "confirm_skip", "scoring",
        "footer", "info_text", "description", "save_answer", "short_name",
        "binah_question_id", "no_value", "title", "subtitle", "minimum_label",
        "title_hidden", "maximum_label", "placeholder", "orientation", "data_label",
        "allow_verify", "allow_verify_text", "decimal_places", "overlay", "camera",
        "allow_instructions", "allow_recording_instructions", "recording_instructions",
        "restrict_video_length", "max_video_time", "conditional_logic",
        "question_group_id", "show_as_dropdown", "restricted", "routing_logic"
    ]

    option_fields = [
        "id", "index", "question_id", "score", "text", "external_id"
    ]

    with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Header section
        # writer.writerow(["# Questionnaire Header"])
        for field in questionnaire_header_fields:
            value = json_data.get(field, "")
            print(f"Value: {value}")
            if isinstance(value, (list, dict)):
                value = json.dumps(value)
            writer.writerow([field, value])

        # Metadata section
        for field in questionnaire_metadata_fields:
            value = json_data.get(field, "")
            print(f"Value: {value}")
            if isinstance(value, (list, dict)):
                value = json.dumps(value)
            writer.writerow([field, value])

        # Questions header
        writer.writerow([])
        # writer.writerow(["# Questions"])
        writer.writerow(question_fields)

        for question in json_data.get("questions", []):
            row = [question.get(field, "") for field in question_fields]
            writer.writerow(row)

            # Options per question
            if "options" in question and isinstance(question["options"], list):
                writer.writerow([""] + option_fields)
                for opt in question["options"]:
                    opt_row = [""] + [opt.get(f, "") for f in option_fields]
                    writer.writerow(opt_row)

    print(f"WeGuide CSV geëxporteerd naar: {output_path}")


if __name__ == '__main__':
    app.run(debug=True)