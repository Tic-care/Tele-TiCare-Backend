from ticare import db ,login_manager
from ticare import bcrypt
from flask_login import  UserMixin
# from flask_sqlalchemy import SQLAlchemy



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    firstName = db.Column(db.String(length=30), nullable=False, )
    lastName = db.Column(db.String(length=30), nullable=False,)
    age = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash= db.Column(db.String(length=60), nullable=False)
    sessions = db.relationship('Session', backref='owned_user', lazy=True)

    # @property
    # def password(self):
    #     return self.password

    # @password.setter
    # def password(self, plain_text_password):
    #     self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # def check_password_correction(self, attempted_password):
    #     return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Session(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date_time = db.Column(db.String(length=24), nullable=False, unique=True)    
    # report = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self):
        return f'Item {self.date_time}'