#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import debug, HTTPError, redirect, request, route, run, static_file, view, get, post
from functools import partial, wraps
from urllib2 import unquote
from model import Post, Repository
from ConfigParser import RawConfigParser
from os import path, walk

import locale
locale.setlocale(locale.LC_ALL, '')  # use system default locale

import helpers

with open('static/wysihtml5-parser-rules.js', 'w') as f:
    f.write(helpers.generate_wysihtml5_parser_rules())

def get_config(filename):
    config = RawConfigParser()
    config.optionxform = str  # case sensitivity
    config.read(filename)
    return config

config = get_config('./buddelblag.config')
repository_path = 'posts'

view = partial(view, helpers=helpers)

def username(auth):
    try:
        return request.auth[0]
    except TypeError:
        return ''

def logged_in(auth):
    try:
        (username, password) = auth
    except TypeError:  # no username or password
        return False

    for user in config.items('users'):
        if (username, password) == (user[0], user[1]):
            return True
    return False

def access_denied():
    return HTTPError(401, 'Access denied!',
        header={'WWW-Authenticate': 'Basic realm="%s"' % \
            Repository(repository_path).description})

def auth_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if logged_in(request.auth):
            return view(*args, **kwargs)
        return access_denied()
    return wrapper

@route('/static/:filename')
def send_static(filename):
    return static_file(filename, root='./static/')

@route('/')
@view('category')
def index():
    return {
        'repository': Repository(repository_path),
        'username': username(request.auth)
    }

@route('/login')
def auth():
    referer = request.headers.get('referer')
    if logged_in(request.auth):
        if referer:
            redirect(referer)
        redirect('/')
    return access_denied()

@get('/posts/:title')
@view('post')
def view_page(title):
    return {
        'post': Post(repository_path, unquote(title)),
        'username': username(request.auth)
    }

@post('/posts/:title')
@auth_required
def commit_page(title):
    content = request.POST['content']
    message = "%s changed via web interface" % unquote(title)
    name = request.auth[0]
    email = config.get('emails', name)

    post = Post(repository_path, unquote(title))
    if post.content != content:
        post.update_content(content, name, email, message)
    else:
        return HTTPError(400, 'Bad Request. Resource was not changed.')
    redirect(title)

@route('/posts/:title/edit')
@auth_required
@view('edit')
def edit_page(title):
    return {
        'post': Post(repository_path, unquote(title)),
    }

debug(True)
run(host='localhost', port=8080, reloader=True)
