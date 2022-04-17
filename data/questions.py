import sqlalchemy
from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    topic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img_question = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    right = sqlalchemy.Column(sqlalchemy.Integer)
    one = sqlalchemy.Column(sqlalchemy.String)
    two = sqlalchemy.Column(sqlalchemy.String)
    three = sqlalchemy.Column(sqlalchemy.String)
    four = sqlalchemy.Column(sqlalchemy.String)
    quiz_id = sqlalchemy.Column(sqlalchemy.Integer)
