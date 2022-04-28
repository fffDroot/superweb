from flask import Flask, render_template, redirect, request
from data import db_session, rating_api
import json
from forms.user import RegisterForm, LoginForm, ChangeForm
from forms.news import NewsForm
from forms.groups import GroupsForm
from forms.question import QuestionForm
from forms.quiz import QuizForm
from forms.quizquestion import QuizquestionForm
from data.users import User
from data.groups import Groups
from data.directions import Directs
from data.news import News
from data.questions import Question
from data.quizzes import Quiz
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_uploads import configure_uploads, IMAGES, UploadSet
from random import randint
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static', 'img')
app.register_blueprint(rating_api.blueprint)
db_session.global_init("db/database.db")
login_manager = LoginManager()
login_manager.init_app(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    a = 1
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    news = news[::-1]
    quiz = db_sess.query(Quiz).all()
    spo = []
    for i in quiz:
        spo.append(i)
    spo = spo[::-1]

    if len(spo) >= 3:
        spo1 = spo[0]
        spo2 = spo[1]
        spo3 = spo[2]


    elif len(spo) == 2:
        spo1 = spo[0]
        spo2 = spo[1]
        spo3 = {
            'name': 'Викторины нет',
            'id': 'no',
        }


    elif len(spo) == 1:
        spo1 = spo[0]
        spo2 = {
            'name': 'Викторины нет',
            'id': 'no',
        }
        spo3 = {
            'name': 'Викторины нет',
            'id': 'no',
        }


    else:
        spo1 = {
            'name': 'Викторины нет',
            'id': 'no',
        }
        spo2 = {
            'name': 'Викторины нет',
            'id': 'no',
        }
        spo3 = {
            'name': 'Викторины нет',
            'id': 'no',
        }

    if len(news) >= 3:
        news1 = news[0]
        news2 = news[1]
        news3 = news[2]
        return render_template('index.html', n1=news1, n2=news2, n3=news3, v1=spo1, v2=spo2, v3=spo3)

    elif len(news) == 2:
        news1 = news[0]
        news2 = news[1]
        news3 = {
            'title': 'Новостей нет',
            'id': 'no',
        }
        return render_template('index.html', n1=news1, n2=news2, n3=news3, v1=spo1, v2=spo2, v3=spo3)
    elif len(news) == 1:
        news1 = news[0]
        news2 = {
            'title': 'Новостей нет',
            'id': 'no',
        }
        news3 = {
            'title': 'Новостей нет',
            'id': 'no',
        }
        return render_template('index.html', n1=news1, n2=news2, n3=news3, v1=spo1, v2=spo2, v3=spo3)
    else:
        news1 = {
            'title': 'Новостей нет',
            'id': 'no',
        }
        news2 = {
            'title': 'Новостей нет',
            'id': 'no',
        }
        news3 = {
            'title': 'Новостей нет',
            'id': 'no',
        }
        return render_template('index.html', n1=news1, n2=news2, n3=news3, v1=spo1, v2=spo2, v3=spo3)

@app.route('/news')
def news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    news = news[::-1]
    spo = []
    db_sess1 = db_session.create_session()
    user = db_sess1.query(User).all()
    user = user[::-1]
    db_sess2 = db_session.create_session()
    direct = db_sess2.query(Directs).all()
    direct = direct[::-1]
    for i in news:
        id = i.id
        title = i.title
        dt = i.created_date
        im = i.img_news
        tema = 'Не выбрана'
        nick = 'Anonymous'
        for j in user:
            if i.user_id == j.id:
                nick = j.name
        for g in direct:
            if i.tema_id == g.id:
                tema = g.title
        spo.append([id, title, dt, im, nick, tema])
    return render_template('news.html', news=spo)

@app.route('/groups')
def groups():
    db_sess = db_session.create_session()
    groups = db_sess.query(Groups).all()
    dirs = db_sess.query(Directs).all()
    groups = groups[::-1]
    spg = []
    for i in groups:
        id = i.id
        title = i.title
        im = i.img_group
        tema = i.tema_id
        tn = ''
        for j in dirs:
            if j.id == tema:
                tn = j.title
        spg.append([id, title, im, tn])

    return render_template('groups.html', groups=spg)

@app.route('/quizzes')
def quizzes():
    db_sess = db_session.create_session()
    quiz = db_sess.query(Quiz).all()
    spo = []
    for i in quiz:
        spo.append([i.id, i.name, i.img_quiz, i.topic])
    return render_template('quizzes.html', quiz=spo)


@app.route('/news/no')
def nonews():
    return "Написано же, что новости нет!!!"

@app.route('/quizz/no')
def novic():
    return "Написано же, что викторины нет!!!"





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


@app.route('/addquestion/<int:id>', methods=['GET', 'POST'])
@login_required
def addquestion(id):
    form = QuestionForm()
    if form.validate_on_submit():
        if form.head.data == '':
            return render_template('makequestions.html',
                                   form=form,
                                   message="Пустой заголовок")
        if form.text.data == '':
            return render_template('makequizzes.html',
                                   form=form,
                                   message="Нет темы")

        if form.photo.data == '':
            return render_template('makequestions.html',
                                   form=form,
                                   message="Нет ФОТО")
        db_sess = db_session.create_session()
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        quest = Question(
            name=form.head.data,
            topic=form.text.data,
            img_question='static/img/' + filename,
            right=int(request.form['right']),
            one=form.text1.data,
            two=form.text2.data,
            three=form.text3.data,
            four=form.text4.data,
            quiz_id=id)
        db_sess.add(quest)
        db_sess.commit()
        for i in form:
            i.data = None
    return render_template('makequestions.html', title='Регистрация', form=form)


@app.route('/addquiz', methods=['GET', 'POST'])
@login_required
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
        quiz = Quiz(
            name=form.head.data,
            topic=form.tema.data,
            img_quiz='static/img/' + filename,
        )
        db_sess.add(quiz)
        quiz = db_sess.query(Quiz).all()
        id = quiz[-1].id
        db_sess.commit()
        return redirect(f'/addquestion/{id}')
    return render_template('makequizzes.html', title='Регистрация', form=form)


@app.route('/addnews', methods=['GET', 'POST'])
@login_required
def addnews():
    form = NewsForm()
    ds = db_session.create_session()
    grops = ds.query(Groups).all()
    spds = []
    for i in grops:
        spds.append(i.id)
    if current_user.id not in spds:
        return "Создайте сообщество перед тем как добавлять новости"
    if form.validate_on_submit():
        if form.head.data == '':
            return render_template('makenews.html', title='Регистрация',
                                   form=form,
                                   message="Пустой заголовок")
        if form.text.data == '':
            return render_template('makenews.html', title='Регистрация',
                                   form=form,
                                   message="Пустое поле текста")
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
            img_news='static/img/' + filename,
            tema_id=form.tema.data,
            user_id=current_user.id,
            groups_id=form.soob.data
        )
        db_sess.add(news)
        db_sess.commit()
        return redirect('/news')
    return render_template('makenews.html', title='Регистрация', form=form)

@app.route('/addgroups', methods=['GET', 'POST'])
@login_required
def addgroups():
    form = GroupsForm()
    if form.validate_on_submit():
        if form.head.data == '':
            return render_template('makegroups.html', title='Регистрация',
                                   form=form,
                                   message="Пустой заголовок")
        if form.photo.data == '':
            return render_template('makegroups.html', title='Регистрация',
                                   form=form,
                                   message="Нет ФОТО")
        db_sess = db_session.create_session()
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        groups = Groups(
            title=form.head.data,
            img_group='static/img/' + filename,
            tema_id=form.tema.data,
            user_id=current_user.id,
        )
        db_sess.add(groups)
        db_sess.commit()
        return redirect('/groups')
    return render_template('makegroups.html', title='Регистрация', form=form)



@app.route('/profile')
@login_required
def profile():
    user = load_user(current_user.id)
    if user.img_user is None:
        im = 'static/img/Noneph.jpg'
    else:
        im = 'static/img/' + user.img_user
    return render_template('profile.html', user=user, im=im)


@app.route('/quizz/<int:id>')
def onequiz(id):
    db_sess = db_session.create_session()
    quiz = db_sess.query(Quiz).get(id)
    spo = [id, quiz.name, quiz.img_quiz, quiz.topic]
    return render_template('onequiz.html', quiz=spo)


@app.route('/quizzquestions/<int:quiz_id>', methods=['POST', 'GET'])
def questions(quiz_id):
    form = QuizquestionForm()
    db_sess = db_session.create_session()
    question = db_sess.query(Question).filter(Question.quiz_id == quiz_id)
    spo = []
    k = 0
    for i in question:
        k += 1
        spo.append([i.name, i.topic, i.img_question, i.right, i.one, i.two, i.three, i.four, k])
    answered = 0
    if form.is_submitted():
        for i in spo:
            if request.form['right' + str(i[-1])] == str(i[3]):
                answered += 1
        result = round(answered / len(spo) * 100)
        return redirect(f'/quizzquestions/result{result}')
    return render_template('question.html', questions=spo, form=form)


@app.route('/quizzquestions/result<result>')
def result(result):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).all()
    print(user)
    res = int(result) // 10 + 1
    user[0].rating += res
    db_sess.commit()
    return render_template('result.html', result=result)


@app.route('/news/<id>')
def onenews(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(id)
    spo = []
    db_sess1 = db_session.create_session()
    user = db_sess1.query(User).all()
    user = user[::-1]
    db_sess2 = db_session.create_session()
    direct = db_sess2.query(Directs).all()
    direct = direct[::-1]
    id = news.id
    content = news.content
    title = news.title
    dt = news.created_date
    im = news.img_news
    for j in user:
        if news.user_id == j.id:
            nick = j.name
    for g in direct:
        if news.tema_id == g.id:
            tema = g.title
    spo.append(id)
    spo.append(title)
    spo.append(dt)
    spo.append(im)
    spo.append(nick)
    spo.append(tema)
    spo.append(content)
    return render_template('onenews.html', news=spo)

@app.route('/groups/<int:id>')
def onegroup(id):
    db_sess = db_session.create_session()
    group = db_sess.query(Groups).get(id)
    users = db_sess.query(User).all()
    news = db_sess.query(News).all()
    news = news[::-1]
    dirs = db_sess.query(Directs).all()
    usid = group.user_id
    tmid = group.tema_id
    nick = ''
    tema = ''
    for i in users:
        if i.id == usid:
            nick = i.name
    for j in dirs:
        if j.id == tmid:
            tema = j.title

    spn = []
    for g in news:
        print(g.groups_id)
        print(id)
        if g.groups_id == id:
            spn.append([g.id, g.title, g.created_date, g.img_news])
            print(222)
        #spn.append([g.id, g.title, g.created_date, g.img_news])
    print(spn)

    return render_template('onegroup.html', group=group, nick=nick, tema=tema, news=spn)


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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
