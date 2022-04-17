from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    head = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField('Контент', validators=[DataRequired()])
    text1 = StringField('1', validators=[DataRequired()])
    text2 = StringField('2', validators=[DataRequired()])
    text3 = StringField('3', validators=[DataRequired()])
    text4 = StringField('4', validators=[DataRequired()])
    tema = StringField('Тема', validators=[DataRequired()])
    photo = FileField('Фото Вопроса')
    submit = SubmitField('Добавить')
