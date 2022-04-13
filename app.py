from flask import Flask, render_template, redirect, request
from data import db_session
import json
from forms.user import RegisterForm, LoginForm, ChangeForm
from forms.news import NewsForm
from forms.question import QuestionForm
from forms.quiz import QuizForm
from data.users import User
from data.news import News
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_uploads import configure_uploads, IMAGES, UploadSet, patch_request_class
from random import randint
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static', 'img')
db_session.global_init("db/database.db")
login_manager = LoginManager()
login_manager.init_app(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    a = 1
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/news')
def news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    news = news[::-1]
    print(news)
    return render_template('news.html', news=news)


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


@app.route('/addquestion', methods=['GET', 'POST'])
def addquestion():
    form = QuestionForm()
    if form.validate_on_submit():
        if form.head.data == '':
            return render_template('makequestions.html',
                                   form=form,
                                   message="Пустой заголовок")
        if form.tema.data == '':
            return render_template('makequestions.html',
                                   form=form,
                                   message="Нет темы")
        if form.photo.data == '':
            return render_template('makequestions.html',
                                   form=form,
                                   message="Нет ФОТО")
        db_sess = db_session.create_session()
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        quest = QuestionForm(
            title=form.head.data,
            content=form.text.data,
            tema=form.tema.data,
            img_news='static/img/' + filename,
        )
        db_sess.add(quest)
        db_sess.commit()
        return redirect('/quizzes')
    return render_template('makequestions.html', title='Регистрация', form=form)


@app.route('/addquiz', methods=['GET', 'POST'])
def addquiz():
    form = QuizForm()
    if form.validate_on_submit():
        if form.head.data == '':
            return render_template('makequizzes.html',
                                   form=form,
                                   message="Пустой заголовок")
        if form.tema.data == '':
            return render_template('makequizzes.html',
                                   form=form,
                                   message="Нет темы")
        if form.photo.data == '':
            return render_template('makequizzes.html',
                                   form=form,
                                   message="Нет ФОТО")
        db_sess = db_session.create_session()
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        quest = News(
            title=form.head.data,
            content=form.text.data,
            tema=form.tema.data,
            img_news='static/img/' + filename,
        )
        db_sess.add(quest)
        db_sess.commit()
        return redirect('/quizzes')
    que = ['sadds', 'sdsdsa', 'sdsdsd']
    return render_template('makequizzes.html', title='Регистрация', quetions=que, form=form)


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
            img_news='static/img/' + filename,
        )
        db_sess.add(news)
        db_sess.commit()
        return redirect('/news')
    return render_template('makenews.html', title='Регистрация', form=form)


@app.route('/profile')
@login_required
def profile():
    user = load_user(current_user.id)
    if user.img_user is None:
        im = 'static/img/Noneph.jpg'
    else:
        im = 'static/img/' + user.img_user
    return render_template('profile.html', user=user, im=im)


# @app.route('/Quiz/<id>')
# def onequiz(id):
#    print(id)
#    db_sess = db_session.create_session()
#    news = db_sess.query(Quest).get(id)
#    im = quest.img_news
#    return render_template('onenews.html', news=news, im=im)

@app.route('/news/<id>')
def onenews(id):
    print(id)
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(id)
    im = news.img_news
    return render_template('onenews.html', news=news, im=im)


@app.route('/profchange', methods=['GET', 'POST'])
def profchange():
    form = ChangeForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    if form.validate_on_submit():
        if form.name.data != '':
            user.name = form.name.data
        if form.email.data != '':
            user.email = form.email.data
        if form.about.data != '':
            user.about = form.about.data
        if form.photo.data:
            filename = photos.save(form.photo.data)
            file_url = photos.url(filename)
            user.img_user = filename
        db_sess.commit()
        return redirect('/profile')
    return render_template('changeprof.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
