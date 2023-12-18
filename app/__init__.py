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


load_dotenv('../.flaskenv')

app = Flask(__name__)

app.secret_key = '4l3j0T190516'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/flask_project"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
bootstrap = Bootstrap4(app)
loginMgr = LoginManager(app)


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