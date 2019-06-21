#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for

app = Flask(__name__)


app.config.from_object('config')


@app.route('/')
@app.route('/index/')
def index():
    return render_template('pages/home.html')


@app.route('/error')
def error():
    return render_template('errors/404.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')
