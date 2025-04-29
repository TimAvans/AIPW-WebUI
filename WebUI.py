from flask import Flask, render_template, request, redirect, url_for, flash
import os
import secrets
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

Bootstrap(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/page1')
def page1():
    return render_template('page1.html')

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
    print(f"We cooking at path: {filepath}!")

if __name__ == '__main__':
    app.run(debug=True)