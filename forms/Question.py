from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    head = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField('Контент', validators=[DataRequired()])
    tema = StringField('Тема', validators=[DataRequired()])
    photo = FileField('Фото Вопроса')
    submit = SubmitField('Добавить')
