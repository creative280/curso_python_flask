from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename
from app.forms import LoginForm, CreateUserForm
from wtforms.validators import DataRequired, InputRequired, Email, Length
from app.models import db, User
from flask_bootstrap import Bootstrap4
from flask_login import LoginManager, login_user, login_required, logout_user
from dotenv import load_dotenv
from flask_ckeditor import CKEditor
from flask_mail import Mail

load_dotenv('../.flaskenv')

app = Flask(__name__)

app.secret_key = '4l3j0T190516'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/flask_project"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
bootstrap = Bootstrap4(app)
loginMgr = LoginManager(app)


app.config['CKEDITOR_FILE_UPLOADER'] = 'auth.upload'
ckeditor = CKEditor(app)

#Config de libreria Mail para enviar correos
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Puerto para TLS
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'devats0516@gmail.com'
app.config['MAIL_PASSWORD'] = 'qvog cdfj biwo katk'

mail = Mail(app)


@loginMgr.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))

db.init_app(app)

# Iniciar la aplicación de Flask con DEBUG True
if __name__ == '__main__':
    app.run(debug=True)

from .auth import auth

app.register_blueprint(auth)

from . import routes


"""
hacer consultas en el interprete interactivo de python

from app import app, db
from models import User

# Establece el contexto de la aplicación
app.app_context().push()

# Ahora puedes realizar operaciones dentro del contexto de la aplicación
current = User.query.all()
print(current)

"""