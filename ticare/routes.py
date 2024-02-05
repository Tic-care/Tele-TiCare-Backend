from flask import request, jsonify
from ticare import app, ALLOWED_EXTENSIONS
from functions import preprocesss
import os



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'})

    video_file = request.files['video']

    if video_file.filename == '':
        return jsonify({'error': 'No selected file'})

    if video_file and allowed_file(video_file.filename):
        filename = f'recorded{app.config["COUNT"]}.webm'
        app.config['COUNT'] += 1  # Increment the counter for the next file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(filepath)
        preprocesss(filepath)

        return jsonify({'message': 'Video uploaded successfully'})

    return jsonify({'error': 'Invalid file format'})
