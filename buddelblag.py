#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import debug, HTTPError, HTTPResponse, redirect, request, response, route, run, static_file, view, get, post, url
from datetime import datetime
from functools import partial, wraps
from itertools import count
from urllib2 import unquote, quote
from urlparse import urljoin, urlsplit
from model import Post, Repository
from ConfigParser import RawConfigParser

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
host = config.get('server', 'host')
port = config.get('server', 'port')
repository_path = 'posts'
repository = Repository(repository_path)

print 'Caching post metadata …'
for p in repository.posts:
    print p.creation_datetime, p.title

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
            repository.description})

def forbidden():
    return HTTPError(403, 'Forbidden!')

def auth_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if logged_in(request.auth):
            return view(*args, **kwargs)
        return access_denied()
    return wrapper

def referer_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        referer = request.headers.get('referer')
        if referer is not None:
            if urlsplit(referer).netloc == urlsplit(request.url).netloc:
                return view(*args, **kwargs)
        return forbidden()
    return wrapper

def etag(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        etag = repository.repo.heads.master.commit.hexsha + \
            username(request.auth)
        if request.headers.get('If-None-Match') == etag:
                return HTTPResponse('Not Modified', 304)
        else:
            response.headers['ETag'] = etag
            return view(*args, **kwargs)
    return wrapper

@route('/static/:filename')
def send_static(filename):
    return static_file(filename, root='./static/')

@route('/')
def redirect_index():
    return redirect('/posts')

@get('/posts')
@etag
@view('category')
def index():
    response = {
        'username': username(request.auth),
        'title': repository.description,
        'posts': [
            {
                'title': post.title or helpers.get_first_sentence_from_html(post.content) + ' …',
                'created': post.creation_datetime,
                'url': urljoin(
                    '//%s:%s' % (host, port),
                    url('post', slug=quote(post.filename.encode('utf-8')))
                ),
            } for post in sorted(repository.posts, key=lambda p: \
                                     p.creation_datetime, reverse=True)
        ]
    }
    return response

@post('/posts')
@auth_required
@referer_required
def create_page():
    content = request.POST['content']
    filename = helpers.generate_slug(content)

    post = Post(repository_path, filename)
    if post.exists:
        for i in count(start=2):
            alternate_filename = '%s-%s' % (filename, i)
            post = Post(repository_path, alternate_filename)
            print i, alternate_filename
            if not post.exists:
                break
        filename = alternate_filename

    message = "%s created via web interface" % unquote(filename)
    name = request.auth[0]
    email = config.get('emails', name)
    post.update_content(content, name, email, message)
    redirect(url('/posts/:slug', slug=filename))

@get('/login')
def auth():
    if logged_in(request.auth):
        referer = request.headers.get('referer')
        if referer:
            redirect(referer)
        redirect('/')
    return access_denied()

@get('/logout')
@referer_required
def deauth():
    return access_denied()

@get('/archive')
def get_archive():
    response.headers['Content-Type'] = 'application/x-tar'
    response.headers['Content-Disposition'] = 'attachment; filename=posts.tar'
    return repository.archive

@get('/feed')
@etag
@view('feed')
def get_feed():
    created = repository.creation_datetime
    updated = repository.update_datetime
    feed = {
        'id': helpers.tag_uri(host, created, repository_path),
        'self': request.url,
        'title': repository.description,
        'updated': updated,
        'entries': [
            {
                'authors': post.authors,
                'content': post.content,
                'id': helpers.tag_uri(host, post.creation_datetime, post.path.encode('utf-8')),
                'title': post.title or helpers.get_first_sentence_from_html(post.content) + ' …',
                'updated': post.update_datetime,
                'url': urljoin(
                    'http://%s:%s' % (host, port),
                    url('post', slug=quote(post.filename.encode('utf-8')))
                ),
            } for post in sorted(repository.posts, key=lambda p: \
                                     p.update_datetime, reverse=True)
        ]
    }
    response.headers['Content-Type'] = 'application/atom+xml'
    return feed

@get('/posts/:slug', name='post')
@etag
@view('post')
def view_page(slug):
    return {
        'post': Post(repository_path, unquote(slug)),
        'username': username(request.auth)
    }

@post('/posts/:slug')
@auth_required
@referer_required
def commit_page(slug):
    content = request.POST['content']
    message = "%s changed via web interface" % unquote(slug)
    name = request.auth[0]
    email = config.get('emails', name)

    post = Post(repository_path, unquote(slug))
    if post.content != content:
        post.update_content(content, name, email, message)
    redirect(url('post', slug=slug))

@route('/posts/:title/edit')
@auth_required
@view('edit')
def edit_page(title):
    return {
        'post': Post(repository_path, unquote(title)),
    }

debug(True)
run(host=host, port=port, reloader=True)
