#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import debug, functools, HTTPError, redirect, request, response, route, run, static_file, view
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
view = functools.partial(view, footer=footer, helpers=helpers, sections=sections)

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

@route('/')
@view('main')
def index():
    return { 'auth': request.auth, 'sections': sections }

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

@route('/archive/<section>', methode='GET')
def get_section_archive(section):
    posts = PostList(unquote(section))
    response.headers['Content-Type'] = 'application/x-tar'
    return posts.archive

@route('/feed/<section>', method='GET')
@view('feed')
def get_section_feed(section):
    posts = PostList(unquote(section))
    hostname = request.urlparts.netloc.split(':')[0]
    created = posts.created
    updated = posts.updated
    feed = {
        'id': tag_uri(hostname, created, unquote(section)),
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
                'updated': post.updated,
            } for post in posts
        ]
    }
    response.headers['Content-Type'] = 'application/atom+xml'
    return feed

@route('/<section>', method='GET')
@view('index')
def get_section(section):
    posts = PostList(unquote(section))
    return {
        'auth': request.auth,
        'posts': [
            {
                'authors': post.authors,
                'content': post.content,
                'mime_type': post.mime_type,
                'title': post.title,
                'created': post.created,
            } for post in posts
        ],
        'section': unquote(section)
    }

@route('/<section>', method='POST')
@auth_required()
def post_section(section):
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

@route('/<section>/<title>', method='GET')
def get_content(section, title):
    post = Post(unquote(section), unquote(title))
    return post.content

@route('/<section>/<title>', method='PUT')
def put_content(section, title):
    content = request.POST['content']
    title = ''

@route('/<section>/<title>', method='PUT')
@auth_required()
def put_content(section, title):
    pass

debug(True)
run(host='localhost', port=8080, reloader=True)
