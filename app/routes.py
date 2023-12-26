from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename
from app.forms import LoginForm, CreateUserForm, resetPasswordForm, RequestedResetPasswordForm
from app.models import db, User, Post
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import  Message
from . import app, mail
from .email import envia_pass_correo


@app.route('/mail')
def send_mail():
    sender = app.config['MAIL_USERNAME'][0]
    msg = Message('Correo desde la aplicacion flask', sender=sender, recipients=["alejandro.taborda280@gmail.com"])
    msg.body = 'Estoy enviadno un correo de purbea con el bodu de ejemplo desde mi aplicacion Flask'
    mail.send(msg)
    return '<h1>Correo enviado</h1>'

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=6)
    
    return render_template('index.html', posts=posts)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_pass():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dash'))
    form= resetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user:
            envia_pass_correo(user)
            flash('Revisa el correo electronico para restablecer tu contraseña.')
            return redirect(url_for('auth.home'))
    return render_template('reset_password.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('auth.dash'))
    user = User.verify_reset_token(token)
    if not user:
        return redirect(url_for('auth.home'))
    form = RequestedResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Has cambiado la contraseña')
        return redirect(url_for('auth.home'))
    return render_template('set_new_password.html', user=user, form=form)

#Pasar variables por una URL
@app.route('/texto/<string:name>')
def texto(name):
    return f"hola {name}, Bienvenido a una prueba de variables por URL"

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/dinamic', methods=['GET', 'POST'])
def dinamic():

    #Validacion del metodo para recibir los parametros
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                urls = json.load(url_file)
        
        """
        En esta parte valido si existe una llave (Key) con el mismo valor que estoy ingresando
        con flash, se crea un mensaje de error donde le indica que ese valor ya se encuentra asignado
        luego en el HTML se renderiza por medio de JINJA

        {% with messages = get_flashed_messages() %}
            {% for message in messages %}
                {{ message }}
            {% endfor %}
        {% endwith %}
        """

        if request.form['code'] in urls.keys():
            flash('Ese nombre ya se encuentra en uso.')
            return redirect(url_for('form'))
        
        if 'url' in request.form.keys():
            urls = {request.form['code']: request.form['url']}

        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('static/uploads/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            flash("Se ha guardado correctamente", "success")
        return render_template('dinamic.html', nombre=request.form['code'])
    else:
        return redirect(url_for('home'))
    
@app.route('/<string:code>')
def redirect_to(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_file:
            try:
                urls = json.load(url_file)
                if code in urls:
                    file_path = urls[code].get('file')
                    if file_path:
                        return redirect(url_for('static', filename='uploads/' + file_path))
                    else:
                        # El código está en el archivo JSON, pero el campo 'file' no está presente
                        return render_template('error.html', error_message='URL no válida')
                else:
                    # El código no se encuentra en el archivo JSON
                    return render_template('error.html', error_message='Código no encontrado')
            except json.JSONDecodeError:
                # El archivo JSON no está en el formato esperado
                return render_template('error.html', error_message='Error en el formato del archivo JSON')
    else:
        # El archivo JSON no existe
        return render_template('error.html', error_message='Archivo de URL no encontrado')


