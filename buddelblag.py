#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import debug, HTTPError, redirect, request, route, run, static_file, view, get
from functools import partial, wraps
from urllib2 import unquote
from model import Post, Repository
from ConfigParser import RawConfigParser
from os import path, walk

import locale
locale.setlocale(locale.LC_ALL, '')  # use system default locale

import helpers

def get_config(filename):
    config = RawConfigParser()
    config.optionxform = str  # case sensitivity
    config.read(filename)
    return config

config = get_config('./buddelblag.config')
directories = [
    d for d in walk('.').next()[1] \
        if '.git' in walk(d).next()[1]
]

view = partial(
    view,
    helpers=helpers,
    repositories=[Repository(d) for d in directories],
    tagline=config.get('blog', 'tagline'),
    title=config.get('blog', 'title')
)

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
            config.get('blog', 'title')})

def auth_required():
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
@view('index')
def index():
    return {
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

@route('/logout')
def deauth():
    return access_denied()

@route('/:category')
@view('category')
def view_category(category):
    return {
        'repository': Repository(unquote(category)),
        'username': username(request.auth)
    }

@route('/:category/:title')
@view('post')
def view_page(category, title):
    return {
        'post': Post(unquote(category), unquote(title)),
        'username': username(request.auth)
    }

@route('/:category/:title/raw')
def raw_page(category, title):
    return static_file(
        unquote(title),
        root=unquote(category)
    )

debug(True)
run(host='localhost', port=8080, reloader=True)
