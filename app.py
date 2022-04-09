from flask import Flask, render_template, redirect, request
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return 'Hello, World!'



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
