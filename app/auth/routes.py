from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import json
import os.path
from werkzeug.utils import secure_filename
from app.forms import LoginForm, CreateUserForm, CreateNewPost, CompleteUserForm
from app.models import db, User, Post
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from . import auth
from flask_ckeditor import upload_fail, upload_success


basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    with app.app_context():
        p = app.config['UPLOADED_PATH'] = os.path.join(basedir, 'uploads')
        return p


@auth.route('/info')
def get_info():
    x = create_app()
    return x


@auth.route('/files/<path:filename>')
def uploaded_files(filename):
    path = create_app()
    return send_from_directory(path, filename)


@auth.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(create_app(), f.filename))
    url = url_for('auth.uploaded_files', filename=f.filename)
    return upload_success(url, filename=f.filename)  # return upload_success call


@auth.route('/', methods=['GET', 'POST'])
def home():
    login = LoginForm()

    if login.validate_on_submit():
        user = User.query.filter_by(username=login.username.data).first()
        if user:
            if user.check_password(login.password.data):
                login_user(user, remember=login.remember.data)
                return redirect('/dashboard')
            
        return '<h2>Usuario o contraseña invalido</h2>'

    #renderizar un template y enviarle una variable a mi HTML
    return render_template('form2.html', formi=login)


@auth.route('/dashboard')
def dash():
    users = User.query.order_by(User.username.asc())
    posts = Post.query.order_by(Post.id.asc())
    
    return render_template('dashboard.html', users=users, posts=posts)


@auth.route('/show')
def show_post():
    post3 = Post.query.filter_by(id=16).first()
    return render_template('showpost.html', post3=post3)   


@auth.route('/media/post/<filename>')
def media_post(filename):
    app = Flask(__name__)
    dir_path = os.path.join(create_app(), filename)
    return send_from_directory(create_dir(), filename)
        

@auth.route('/post', methods=['GET', 'POST'])
def post():
    postform = CreateNewPost()
    if postform.validate_on_submit():
        newpost = Post(title=postform.title.data, body=postform.body.data)
        newpost.user_id = current_user.id
        file = request.files['thumb']
        if not file:
            try:
                db.session.add(newpost)  
                db.session.commit()
                flash('Post Publicado')
            except:
                'No se ha guardado'
        else:
            img_name = secure_filename(file.filename).lower()
            img_dir = create_dir()
            file_path = os.path.join(img_dir, img_name)
            file_extension = os.path.splitext(file_path)[1]
            file_allow = ['.jpg','.jpeg', '.png', '.gif', '.svg']
            if file_extension not in file_allow:
                return "NO SE PUEDE CARGAR ESA IMAGEN"
            else:
                file.save(file_path)
                newpost.thumb = img_name
                try:
                    db.session.add(newpost)  
                    db.session.commit()
                    flash('Post Publicado')
                except:
                    'No se ha guardado'
    return render_template('post.html', post = postform)

def create_dir():
    app = Flask(__name__)
    with app.app_context():
        p = app.config['UPLOADED_PATH'] = os.path.join(basedir, 'static/uploads')
        up = app.config['UPLOAD_FOLDER'] = p
        return up


@auth.route('/post-table')
def tablepost():
    posts = Post.query.all()
    # posts = Post.query.order_by(Post.id.desc()). limit(2).all()
    return render_template('post-table.html', posts=posts)


@auth.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def updatepost(id):
    post_update = Post.query.get_or_404(id)
    if request.method == 'POST':
        post_update.title = request.form['title']
        post_update.body = request.form['body']    
        try:
            db.session.commit()
            return redirect('/post-table')
        except:
            return "No ha funcionado la actualizacion"
    else:
        return render_template('post-edit.html', post_update=post_update)


@auth.route('/post/delete/<int:id>', methods=['GET', 'POST'])
def deletepost(id):
    post_delete = Post.query.get_or_404(id)
    
    try:
        db.session.delete(post_delete)
        db.session.commit()
        return redirect('/post-table')
    except:
        return "NO ha funcionado el borrado"


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


@auth.route('/post/<username>')
@login_required
def post_by_user(username):
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author=user).all()
    return render_template('user-post.html', user=user, posts=posts)

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


@auth.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).all()
    form = CompleteUserForm(obj=user)
    
    if request.method == 'POST':
        form.populate_obj(user)
        if user == current_user:
            db.session.add(user)
            db.session.commit()
        else:
            return f'NO puedes modificar este usuario: {user.username}'
        return redirect(url_for('auth.profile', username=user.username))
    
        
    return render_template('profile.html', user=user, posts=posts, form=form)