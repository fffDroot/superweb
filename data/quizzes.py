import sqlalchemy
from .db_session import SqlAlchemyBase


class Quiz(SqlAlchemyBase):
    __tablename__ = 'quizzes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    topic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img_quiz = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
