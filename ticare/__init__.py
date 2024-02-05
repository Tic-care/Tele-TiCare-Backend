from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)
CORS(app)

UPLOAD_FOLDER = 'savedVedio'
ALLOWED_EXTENSIONS = {'webm'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COUNT'] = 1  # Initialize the counter for filenames

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
app.app_context().push()


from ticare import routes