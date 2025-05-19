from flask import Flask, request, render_template, Response, jsonify, send_from_directory
import os
import subprocess
import sys
import threading
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'input'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variable to store the process
process = None

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global process
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

        return 'File uploaded successfully'

    return 'Invalid file type'

@app.route('/stream')
def stream():
    def generate():
        global process
        if process:
            while True:
                # Check if the process is still running
                if process.poll() is not None:  # Process has finished
                    break
                stdout_line = process.stdout.readline()
                if stdout_line:
                    yield f"data: {stdout_line.strip()}\n\n"
            process.stdout.close()
            process.wait()

    return Response(generate(), mimetype='text/event-stream')

@app.route('/list_files', methods=['GET'])
def list_files():
    output_folder = 'output'  # Specify your output folder here
    try:
        files = os.listdir(output_folder)
        return jsonify(files)  # Return the list of files as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/output/<path:filename>', methods=['GET'])
def serve_file(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
    app.run(debug=True)
