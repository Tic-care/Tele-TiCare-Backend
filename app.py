from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'savedVideo'
ALLOWED_EXTENSIONS = {'webm'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
count = 1  # Initialize count

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    global count  # Use the global count variable

    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'})

    video_file = request.files['video']

    if video_file.filename == '':
        return jsonify({'error': 'No selected file'})

    if video_file and allowed_file(video_file.filename):
        filename = f'recorded{count}.webm'
        count += 1  # Increment count for the next video
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(filepath)

        return jsonify({'message': f'Video uploaded successfully as {filename}'})

    return jsonify({'error': 'Invalid file format'})

if __name__ == '__main__':
    app.run(debug=True)
