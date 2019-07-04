#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from app.views import Answer

app = Flask(__name__)


app.config.from_object('config')


@app.route('/')
@app.route('/index')
def index():
    return render_template('pages/home.html')


@app.route('/error')
def error():
    return render_template('errors/404.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/_answer', methods=['post'])
def answer():
    bot_answer = Answer(request.form['user_post'])
    print(bot_answer.user_post)

