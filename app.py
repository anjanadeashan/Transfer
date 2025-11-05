import os
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return 'No file part', 400

    files = request.files.getlist('files')
    for file in files:
        if file.filename != '':
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return 'Files uploaded successfully', 200

@app.route('/api/files', methods=['GET'])
def list_files():
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(path):
            files.append({
                'name': filename,
                'size': os.path.getsize(path),
                'modified': datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M'),
                'type': filename.split('.')[-1].lower()
            })
    return jsonify(files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
