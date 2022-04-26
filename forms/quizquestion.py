from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class QuizquestionForm(FlaskForm):
    right = StringField("Выберите правильный ответ")
    submit = SubmitField('Добавить')
