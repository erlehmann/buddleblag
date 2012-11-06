#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import debug, functools, HTTPError, redirect, request, response, route, run, static_file, url, view
from datetime import datetime
from urllib2 import unquote
from model import Post, PostList
from ConfigParser import RawConfigParser

import locale
locale.setlocale(locale.LC_ALL, '')  # use system default locale

import helpers
from helpers import tag_uri

def get_config(filename):
    config = RawConfigParser()
    config.optionxform = str  # case sensitivity
    config.read(filename)
    return config

config = get_config('./buddelblag.config')
config.sidebar = get_config('./sidebar.config')

footer = config.get('blog', 'footer')
sections = [
    {
       'name': section[0],
       'title': section[1]
    } for section in config.items('sections')
]
title = config.get('blog', 'title')

view = functools.partial(view, footer=footer, helpers=helpers, sections=sections, title=title)

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
                header={'WWW-Authenticate': 'Basic realm="%s"' % title})
        return wrapper
    return decorator

@route('/')
@view('main')
def index():
    return {
        'auth': request.auth,
        'content': 'Dieses Programm hat das Ziel, die Medienkompetenz der Leser zu steigern. Gelegentlich packe ich sogar einen handfesten Buffer Overflow oder eine Format String Vulnerability zwischen die anderen Codezeilen und schreibe das auch nicht dran.',
        'sections': sections,
        'title': title
    }

@route('/static/:filename')
def send_static(filename):
    return static_file(filename, root='./static/')

@route('/login')
def auth():
    referer = request.headers.get('referer')
    if logged_in(request.auth):
        if referer:
            print referer
            redirect(referer)
        redirect ('/')

    return HTTPError(401, 'Access denied!', header={ \
        'WWW-Authenticate': 'Basic realm="%s"' % \
            config.get('blog', 'title')})

@route('/archive/<section>', methode='GET')
def get_section_archive(section):
    section = unquote(section)
    posts = PostList(section)
    response.headers['Content-Type'] = 'application/x-tar'
    return posts.archive

@route('/feed/<section>', method='GET')
@view('feed')
def get_section_feed(section):
    section = unquote(section)
    posts = PostList(section)
    hostname = request.urlparts.netloc.split(':')[0]
    created = posts.created
    updated = posts.updated
    feed = {
        'id': tag_uri(hostname, created, section),
        'self': request.url,
        'title': unquote(section),
        'updated': updated,
        'entries': [
            {
                'authors': post.authors,
                'content': post.content,
                'id': tag_uri(hostname, datetime.now(), post.title),
                'mime_type': post.mime_type,
                'title': post.title,
                'url': url('post', section=section, title=post.title),
                'updated': post.updated,
            } for post in posts
        ]
    }
    response.headers['Content-Type'] = 'application/atom+xml'
    return feed

@route('/<section>', method='GET')
@view('index')
def get_section(section):
    section=unquote(section)
    posts = PostList(section)
    return {
        'auth': request.auth,
        'posts': [
            {
                'authors': post.authors,
                'content': post.content,
                'created': post.created,
                'mime_type': post.mime_type,
                'title': post.title,
                'url': url('post', section=section, title=post.title)
            } for post in posts
        ],
        'section': unquote(section)
    }

@route('/<section>', method='POST')
@auth_required()
def post_section(section):
    section = unquote(section)
    content = request.POST['content']
    title = datetime.now().strftime('%s')

    name = request.auth[0]
    email = config.get('emails', name)
    message = '+ ' + request.POST['content']

    post = Post(section, title)
    post.update_content(content, name, email, message)
    response.status = 201  # Created
    location = request.url + '/' + title
    response.headers['Location'] = location
    return location

@route('/<section>/<title>', method='GET', name='post')
def get_content(section, title):
    section, title = unquote(section), unquote(title)
    post = Post(section, title)
    print post.exists
    return post.content

@route('/<section>/<title>', method='PUT')
def put_content(section, title):
    raise NotImplementedError

@route('/<section>/<title>', method='PUT')
@auth_required()
def put_content(section, title):
    pass

debug(True)
run(host='localhost', port=8080, reloader=True)
