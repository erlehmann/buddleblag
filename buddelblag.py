#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import debug, functools, HTTPError, redirect, request, route, run, static_file, view
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

view = functools.partial(
    view,
    directories=directories,
    helpers=helpers,
    title=config.get('blog', 'title')
)

@route('/static/:filename')
def send_static(filename):
    return static_file(filename, root='./static/')

@route('/')
@view('index')
def index():
    return {
        'repositories': [Repository(d) for d in directories]
    }

@route('/:category')
@view('category')
def view_category(category):
    return {
        'repository': Repository(unquote(category))
    }

@route('/:category/:title')
@view('post')
def view_page(category, title):
    return {
        'post': Post(unquote(category), unquote(title))
    }

@route('/:category/:title/raw')
def raw_page(category, title):
    return static_file(
        unquote(title),
        root=unquote(category)
    )

debug(True)
run(host='localhost', port=8080, reloader=True)
