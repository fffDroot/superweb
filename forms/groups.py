from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired
from data import db_session
from data.directions import Directs

db_session.global_init("db/database.db")

class GroupsForm(FlaskForm):
    db_sess = db_session.create_session()
    dirs = db_sess.query(Directs).all()
    sp = []
    for i in dirs:
        sp.append((i.id, i.title))
    head = StringField('Заголовок', validators=[DataRequired()])
    tema = SelectField('Тема', choices=sp)
    photo = FileField('Фото новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')
