#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from app.views import Answer
from config import URL_API_GMAPS

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


app.config.from_object('config')


@app.route('/')
@app.route('/index')
def index():
    return render_template('pages/home.html', urlapimap=URL_API_GMAPS)


@app.route('/error')
def error():
    return render_template('errors/404.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/_answer', methods=['POST'])
def answer():
    bot_answer = Answer(request.form['user_post'])
    #print(bot_answer.user_post)
    wiki_reply = bot_answer.answer_wiki
    map_reply = bot_answer.answer_map
    #print(bot_answer.answer_wiki)
    print(bot_answer.answer_map)

    return jsonify(wiki_reply=wiki_reply, map_reply=map_reply)
