import flask
from flask import Flask, render_template, redirect, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'rating_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/rating')
def get_news():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    spo = []
    for i in users:
        spo.append([i.name, i.rating, i.img_user])

    spv = sorted(spo, key=lambda x: x[1], reverse=True)
    c = 0
    for i in spv:
        c += 1
        i.append(c)
    return render_template('rat.html', quiz=spv)
    #return render_template('rat.html')