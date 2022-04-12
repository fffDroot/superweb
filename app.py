from flask import Flask, render_template, redirect, request
from data import db_session
import json
from forms.user import RegisterForm, LoginForm
from forms.news import NewsForm
from data.users import User
from data.news import News
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_uploads import configure_uploads, IMAGES, UploadSet, patch_request_class
from random import randint
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')
db_session.global_init("db/database.db")
login_manager = LoginManager()
login_manager.init_app(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/quizzes')
def quizzes():
    return render_template('quizzes.html')

@app.route('/groups')
def groups():
    return render_template('groups.html')

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/addnews', methods=['GET', 'POST'])
def addnews():
    form = NewsForm()
    if form.validate_on_submit():
        if form.head.data == '':
            return render_template('makenews.html', title='Регистрация',
                                   form=form,
                                   message="Пустой заголовок")
        if form.text.data == '':
            return render_template('makenews.html', title='Регистрация',
                                   form=form,
                                   message="Пустое поле текста")

        if form.tema.data == '':
            return render_template('makenews.html', title='Регистрация',
                                   form=form,
                                   message="Нет темы")
        if form.photo.data == '':
            return render_template('makenews.html', title='Регистрация',
                                   form=form,
                                   message="Нет ФОТО")
        db_sess = db_session.create_session()
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        news = News(
            title=form.head.data,
            content=form.text.data,
            tema=form.tema.data,
            img_news=filename,
        )
        db_sess.add(news)
        db_sess.commit()
        return redirect('/news')
    return render_template('makenews.html', title='Регистрация', form=form)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
