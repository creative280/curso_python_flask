from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename
from forms import LoginForm, CreateUserForm
from wtforms.validators import DataRequired, InputRequired, Email, Length
from models import db, User
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.secret_key = '4l3j0T190516'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/flask_project"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
bootstrap = Bootstrap(app)
db.init_app(app)


@app.route('/home', methods=['GET', 'POST'])
@app.route('/')
def home():
    login = LoginForm()

    if login.validate_on_submit():
        user = User.query.filter_by(username=login.username.data).first()
        if user:
            if user.password == login.password.data:
                return '<h2>Login Correcto</h2>'
            
        return '<h2>Usuario o contraseña invalido</h2>'

    #renderizar un template y enviarle una variable a mi HTML
    return render_template('form2.html', formi=login)


@app.route('/users')
def users():
    title = 'Lista de usuarios'
    users = User.query.order_by(User.username.desc())
    return render_template('/users.html', title=title, users=users)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user_updt = User.query.get_or_404(id)
    if request.method == 'POST':
        user_updt.username = request.form['name']
        try:
            db.session.commit()
            return redirect('/users')
        except:
            return 'No ha funcionado la actualizacion'
    else:
        return render_template('update.html', user_updt=user_updt)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delte(id):
    user_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_delete)
        db.session.commit()
        return redirect('/users')
    except:
        return 'No ha funcionado la actualizacion'


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    registro = CreateUserForm()

    if registro.validate_on_submit():
        
        new_user = User(username=registro.username.data, email=registro.email.data, password=registro.password.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>Nuevo Usuario Creado en BD</h1>'
        
        #return '<h1>' + registro.email.data + ' ' + registro.username.data + ' ' + registro.password.data + '</h1>'
    
    return render_template('register.html', regis=registro)




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
                urls = json.load(url_file)
                if code in urls.keys():
                    return redirect(url_for('static', filename='uploads/' + urls[code]['file']))    





# Iniciar la aplicación de Flask con DEBUG True
if __name__ == '__main__':
    app.run(debug=True)


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