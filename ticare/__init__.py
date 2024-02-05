from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'savedVedio'
ALLOWED_EXTENSIONS = {'webm'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COUNT'] = 1  # Initialize the counter for filenames
