from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message='Este campo no puede estar vacio'), 
                                                   Length(min=4, max=16, message='El nombre de usuario debe de tener entre %(min)d y %(max)d caracteres')])
    password = PasswordField('password', validators=[InputRequired(message='Este campo no puede estar vacio'),
                                                    Length(min=8, max=16, message='La contraseña tiene que tener entre %(min)d y %(max)d caracteres')])
    remember = BooleanField('remember me')

class CreateUserForm(FlaskForm):
    email = StringField('Escribe el correo', validators=[InputRequired(), Email(message="Esto no es un email valido."), Length(max=60)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=16)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=16)])

    