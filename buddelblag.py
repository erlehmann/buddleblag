#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import debug, functools, redirect, request, route, run, static_file, view
from model import Article, ArticleList
from ConfigParser import RawConfigParser

import helpers


config = RawConfigParser()
config.optionxform = str
config.read('./buddelblag.config')

view = functools.partial(view, config=config, helpers=helpers) 

@route('/')
@view('index')
def index():
    articles = []

    list = ArticleList()
    titles = list.get_article_titles()
    articles = [Article(title) for title in titles]

    return {'articles': articles}

@route('/static/:filename')
def send_static(filename):
    return static_file(filename, root='./static/')

@route('/:title')
def index(title):
    article = Article(title)
    c.title = article.get_title()
    c.content = article.get_content()
    return render('article')

debug(True)
run(host='localhost', port=8080, reloader=True)
