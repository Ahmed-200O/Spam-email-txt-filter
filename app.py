# app.py
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from spam_filter import SpamFilter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Spam Filter
spam_filter = SpamFilter()
spam_filter.train("Get rich quick! Buy now!", True)
spam_filter.train("Hello, how are you?", False)
spam_filter.train("Claim your prize money now!", True)
spam_filter.train("Meeting at 3 PM tomorrow", False)


@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Read the content of the file
    with open(file_path, 'r') as f:
        content = f.read()

    # Classify each line
    results = spam_filter.classify_file(file_path)

    # Return both content and results
    return jsonify({"content": content, "results": results})


if __name__ == '__main__':
    app.run(debug=True)

