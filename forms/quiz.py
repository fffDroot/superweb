from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class QuizForm(FlaskForm):
    head = StringField('Заголовок')
    tema = StringField('Тема')
    photo = FileField('Фото викторины', validators=[DataRequired()])
    submit = SubmitField('Добавить вопросы')

