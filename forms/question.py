from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    head = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField('Контент', validators=[DataRequired()])
    text1 = StringField('1')
    text2 = StringField('2')
    text3 = StringField('3')
    text4 = StringField('4')
    right = StringField("Выберите правильный ответ")
    photo = FileField('Фото Вопроса')
    submit = SubmitField('Добавить')
