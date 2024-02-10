from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)
CORS(app ,supports_credentials=True)

UPLOAD_FOLDER = 'savedVedio'
ALLOWED_EXTENSIONS = {'webm'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COUNT'] = 1  # Initialize the counter for filenames

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)



with app.app_context():
    db.create_all()

# db.init_app(app)
   
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

app.app_context().push()


from ticare import routes