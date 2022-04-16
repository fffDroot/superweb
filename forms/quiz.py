from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField


class QuizForm(FlaskForm):
    head = StringField('Заголовок')
    tema = StringField('Тема')
    photo = FileField('Фото викторины')
    submit = SubmitField('Добавить вопросы')

