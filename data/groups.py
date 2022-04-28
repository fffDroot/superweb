import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Groups(SqlAlchemyBase):
    __tablename__ = 'groups'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    img_group = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    tema_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

