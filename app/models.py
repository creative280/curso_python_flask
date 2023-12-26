from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
import urllib, hashlib
import jwt
from time import time
import secrets, string

db = SQLAlchemy()

alphabet = string.ascii_letters + string.digits + string.punctuation
password = ''.join(secrets.choice(alphabet) for i in range(64))
 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    birth = db.Column(db.DateTime)
    address = db.Column(db.String(120))
    number = db.Column(db.String(80))
    city = db.Column(db.String(120))
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, default = 0)
    post = db.relationship('Post', backref ='author', lazy='dynamic')

    def gravatar(self, size):
        digest = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{ digest }?s={size}'

    def __repr__(self):
        return f'{self.id, self.username, self.email, self.is_admin}'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_reset_token(self, expira=180):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expira}, password, algorithm='HS256')
    
    @staticmethod
    def verify_reset_token(token):
        try:
            id = jwt.decode(token, password, algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.now())
    thumb = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.title, self.timestamp}'