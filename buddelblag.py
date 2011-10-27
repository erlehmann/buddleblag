#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import debug, functools, HTTPError, redirect, request, route, run, static_file, view
from model import Article, ArticleList
from ConfigParser import RawConfigParser

import helpers

config = RawConfigParser()
config.optionxform = str
config.read('./buddelblag.config')

view = functools.partial(view, config=config, helpers=helpers) 


def logged_in(auth):
    try:
        (username, password) = auth
    except TypeError:  # no username or password supplied
        return False

    for user in config.items('users'):
        if (username, password) == (user[0], user[1]):
            return True
    return False

def logged_in_user(auth):
    if logged_in(auth):
        return auth[0]

@route('/')
@view('index')
def index():
    articles = []

    list = ArticleList()
    titles = list.get_article_titles()
    articles = [Article(title) for title in titles]

    return {'articles': articles, 'auth': request.auth}


@route('/login')
def auth():
    referer = request.headers.get('referer')
    if logged_in(request.auth):
        if referer:
            redirect(referer)
        redirect ('/')

    return HTTPError(401, 'Access denied!', header={ \
        'WWW-Authenticate': 'Basic realm="%s"' % \
            config.get('blog', 'title')})


@route('/static/:filename')
def send_static(filename):
    ## FIXME: paranoia
    return static_file(filename, root='./static/')


@route('/:title')
def single_page(title):
    ## FIXME: paranoia
    article = Article(title)
    c.title = article.get_title()
    c.content = article.get_content()
    return render('article')

debug(True)
run(host='localhost', port=8080, reloader=True)
