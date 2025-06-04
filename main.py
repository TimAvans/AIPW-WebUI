import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import os
import secrets
from flask_bootstrap import Bootstrap
import json
import pandas as pd

from models.schemas import LLMConfig
from services.openrouter_service import OpenRouterService
from services.discriminator_service import Discriminator
from services.generator_service import Generator

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

Bootstrap(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

OPENROUTER_SERVICE = OpenRouterService()

CONFIG_FILE = "prompt.json"
FEEDBACK_LIMIT = 3

DISCRIMINATOR = Discriminator(openrouter_service=OPENROUTER_SERVICE)
GENERATOR = Generator(openrouter_service=OPENROUTER_SERVICE)

@app.route('/')
def home():
    prompt_model = get_config_data()

    return render_template('home.html', config=prompt_model)

@app.route("/update-prompt", methods=["POST"])
def update_prompt():
    try:
    
        new_config_data = {
            "generator_prompt": request.form.get("generator_prompt"),
            "generator_model": request.form.get("generator_model"),
            "discriminator_prompt": request.form.get("discriminator_prompt"),
            "discriminator_model": request.form.get("discriminator_model"),
        }
        updated_config = LLMConfig(**new_config_data)

        current_config = get_config_data()

        if current_config is updated_config:
            flash("No changes made")
            return redirect(url_for('home'))
        else:        
            update_config_data(updated_config)

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
        
        generator_discriminator(file_path)
        
        # post_process_csv(file_path)
        flash('File successfully uploaded and processed.')
        return redirect(url_for('home'))
    else:
        flash('Only PDF files are allowed!')
        return redirect(url_for('home'))

def post_process_csv(filepath):
    df = pd.read_csv(filepath, dtype=str, keep_default_na=False)

    df_cleaned = df.applymap(lambda x: x.replace('""', '"').strip('"') if isinstance(x, str) else x)
    print("Turnign into csv")
    df_cleaned.to_csv("cleaned_file.csv", index=False)

def generator_discriminator(filepath):
    feedback_prompt = "<feedback>In case the discriminator has feedback on the request it will be provided here.</feedback>"
    accepted = False
    feedback_counter = 0

    while not accepted and feedback_counter < FEEDBACK_LIMIT:
        csv_string = GENERATOR.generate(filepath=filepath, feedback_prompt=feedback_prompt)
        feedback = DISCRIMINATOR.discriminate(filepath=filepath, questionnaire_data=csv_string)
        # print(f"Feedback: {feedback}")
        accepted = feedback["accepted"]
        feedback_prompt = feedback["feedback"]
        # print(f"Feedback: {feedback_prompt}")
        print(f"Accepted: {accepted}")
        feedback_counter += 1

def get_config_data():
    prompt_data = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            prompt_data = json.load(f)
            prompt_model = LLMConfig(**prompt_data)
    return prompt_model

def update_config_data(prompt_model):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(prompt_model.model_dump(), f, indent=4)


if __name__ == '__main__':
    app.run(debug=True)