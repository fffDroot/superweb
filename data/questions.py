#import sqlalchemy
#from .db_session import SqlAlchemyBase
#from sqlalchemy import orm
#
#
#class Question(SqlAlchemyBase):
#    __tablename__ = 'users'
#
#    id = sqlalchemy.Column(sqlalchemy.Integer,
#                           primary_key=True, autoincrement=True)
#    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
#    topic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
#    img_quiz = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
#    right = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True)
#    One = sqlalchemy.Column(sqlalchemy.String, nullable=False)
#    Two = sqlalchemy.Column(sqlalchemy.String, nullable=False)
#    Three = sqlalchemy.Column(sqlalchemy.String, nullable=False)
#    Four = sqlalchemy.Column(sqlalchemy.String, nullable=False)
#    quiz_id = sqlalchemy.Column(sqlalchemy.Integer,
#                                sqlalchemy.ForeignKey("quizes.id"))
#    quiz = orm.relation('Quiz')
