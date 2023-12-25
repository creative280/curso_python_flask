from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, FileField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message='Este campo no puede estar vacio'), 
                                                   Length(min=4, max=16, message='El nombre de usuario debe de tener entre %(min)d y %(max)d caracteres')])
    password = PasswordField('password', validators=[InputRequired(message='Este campo no puede estar vacio'),
                                                    Length(min=6, max=16, message='La contraseña tiene que tener entre %(min)d y %(max)d caracteres')])
    remember = BooleanField('remember me')
    enviar = SubmitField('Inicia Sesión')
    
class resetPasswordForm(FlaskForm):
    email = StringField('Escribe el correo', validators=[InputRequired(), Email(message="Esto no es un email valido."), Length(max=60)])
    enviar = SubmitField('Restablecer Contraseña')

class RequestedResetPasswordForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[InputRequired(message='Este campo no puede estar vacio'),
                                                    Length(min=6, max=16, message='La contraseña tiene que tener entre %(min)d y %(max)d caracteres')])
    password2 = PasswordField('Repite la Contraseña', validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')])
    enviar = SubmitField('Cambiar Contraseña')

class CreateUserForm(FlaskForm):
    email = StringField('Escribe el correo', validators=[InputRequired(), Email(message="Esto no es un email valido."), Length(max=60)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=16)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=16)])
    enviar = SubmitField('Registrarse')
    
class CompleteUserForm(CreateUserForm):
    firstname = StringField('Nombre Completo', validators=[Length(min=4, max=50)])
    lastname = StringField('Apellidos', validators=[Length(min=4, max=50)])
    birth = DateField('Fecha Nacimiento', format='%Y-%m-%d')
    address = StringField('Dirección', validators=[Length(min=4, max=90)])
    number = StringField('Numero Telefono', validators=[Length(min=4, max=13)])
    city = StringField('Ciudad', validators=[Length(min=4, max=13)])
    update = SubmitField('Actualizar Información')
    
class CreateNewPost(FlaskForm):
    title = StringField('Titulo del Post', validators=[InputRequired(), Length(min=4, max=180)])
    body = CKEditorField('Escribe el contenido', validators=[InputRequired(), Length(min=4, max=800)])
    thumb = FileField()
    enviar = SubmitField('Publicar')