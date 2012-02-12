#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import debug, functools, HTTPError, redirect, request, route, run, static_file, view
from urllib2 import unquote
from model import Post, PostList
from ConfigParser import RawConfigParser

import locale
locale.setlocale(locale.LC_ALL, '')  # use system default locale

import helpers

def get_config(filename):
    config = RawConfigParser()
    config.optionxform = str  # case sensitivity
    config.read(filename)
    return config

config = get_config('./buddelblag.config')
config.sidebar = get_config('./sidebar.config')

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


def auth_required():
    def decorator(view):
        def wrapper(*args, **kwargs):
            if logged_in(request.auth):
                return view(*args, **kwargs)
            return HTTPError(401, 'Access denied!', 
                header={'WWW-Authenticate': 'Basic realm="%s"' % \
                    config.get('blog', 'title')})
        return wrapper
    return decorator


@route('/static/:filename')
def send_static(filename):
    return static_file(filename, root='./static/')

@route('/')
@view('index')
def index():
    return {'posts': PostList().posts, 'auth': request.auth}

@route('/:title', method='GET')
@view('post')
def view_page(title):
    post = Post(unquote(title))
    return {'post': post, 'auth': request.auth}

@route('/:title', method='POST')
@auth_required()
@view('post')
def commit_page(title):
    content = request.POST['content']
    if content[-1] != '\n':
        content += '\n'

    name = request.auth[0]
    email = config.get('emails', request.auth[0])
    message = request.POST['message']

    post = Post(title)
    post.update_content(content, name, email, message)
    redirect('/' + title)

@route('/:title/edit')
@auth_required()
@view('edit')
def edit_page(title):
    post = Post(unquote(title))
    return {'post': post, 'auth': request.auth}


@route('/:title/raw')
def send_post(title):
    title = unquote(title)
    return static_file(title, root='./posts/')

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


debug(True)
run(host='localhost', port=8080, reloader=True)
