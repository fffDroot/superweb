from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField


class QuizForm(FlaskForm):
    head = StringField('Заголовок')
    text = TextAreaField('Контент')
    tema = StringField('Тема')
    photo = FileField('Фото викторины')
    submit = SubmitField('Добавить')
    addquestion = SubmitField('Добавить вопрос')
