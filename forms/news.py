from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired
from data import db_session
from data.directions import Directs
from data.groups import Groups
db_session.global_init("db/database.db")


class NewsForm(FlaskForm):
    db_sess = db_session.create_session()
    db_sess.flush()
    db_sess.commit()
    dirs = db_sess.query(Directs).all()
    soob = db_sess.query(Groups).all()
    sp = []
    sps = []
    for i in dirs:
        sp.append((i.id, i.title))
    for j in soob:
        sps.append((j.id, j.title))
    print(sps)
    head = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField('Контент', validators=[DataRequired()])
    tema = SelectField('Тема', choices=sp)
    # soob = SelectField('В какую группу хотите добавить?', choices=sps)
    photo = FileField('Фото новости')
    submit = SubmitField('Добавить')
