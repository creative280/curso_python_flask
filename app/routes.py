from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename
from app.forms import LoginForm, CreateUserForm
from app.models import db, User
from flask_login import LoginManager, login_user, login_required, logout_user
from . import app


@app.route('/home', methods=['GET', 'POST'])


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


