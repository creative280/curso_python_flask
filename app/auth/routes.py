from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename
from app.forms import LoginForm, CreateUserForm
from app.models import db, User, Post
from flask_login import LoginManager, login_user, login_required, logout_user
from . import auth


@auth.route('/', methods=['GET', 'POST'])
def home():
    login = LoginForm()

    if login.validate_on_submit():
        user = User.query.filter_by(username=login.username.data).first()
        if user:
            if user.check_password(login.password.data):
                login_user(user, remember=login.remember.data)
                return '<h2>Login Correcto</h2>'
            
        return '<h2>Usuario o contraseña invalido</h2>'

    #renderizar un template y enviarle una variable a mi HTML
    return render_template('form2.html', formi=login)

@auth.route('/dashboard')
def dash():
    users = User.query.order_by(User.username.asc())
    posts = Post.query.order_by(Post.id.asc())
    
    return render_template('dashboard.html', users=users, posts=posts)

@auth.route('/post')
def post():
    
    
    return render_template('post.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.home'))

@auth.route('/users')
@login_required
def users():
    title = 'Lista de usuarios'
    users = User.query.order_by(User.username.desc())
    return render_template('/users.html', title=title, users=users)


@auth.route('/update/<int:id>', methods=['GET', 'POST'])
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


@auth.route('/delete/<int:id>', methods=['GET', 'POST'])
def delte(id):
    user_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_delete)
        db.session.commit()
        return redirect('/users')
    except:
        return 'No ha funcionado la actualizacion'


@auth.route('/registro', methods=['GET', 'POST'])
def register():
    registro = CreateUserForm()

    if registro.validate_on_submit():
        
        new_user = User(username=registro.username.data, email=registro.email.data)
        new_user.set_password(registro.password.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>Nuevo Usuario Creado en BD</h1>'
        
        #return '<h1>' + registro.email.data + ' ' + registro.username.data + ' ' + registro.password.data + '</h1>'
    
    return render_template('register.html', regis=registro)