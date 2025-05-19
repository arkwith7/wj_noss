from flask import Flask, request, render_template
import os
import subprocess
import sys

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'input'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Run the extract_pdf function in a subprocess and capture its output
        process = subprocess.Popen(
            [sys.executable, '-c', f'from main_test import extract_pdf; extract_pdf("{file.filename}")'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        # Combine stdout and stderr for output
        output = stdout + stderr

        return render_template('upload.html', output=output)  # Pass output to the template
    return 'Invalid file type'

if __name__ == '__main__':
    app.run(debug=True)
