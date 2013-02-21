#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from git import Repo
from os import environ, path
from sys import argv
from xml.etree.cElementTree import ElementTree

from model import Post

filename = argv[1]
repository_path = './posts'
repository = Repo.init(repository_path)
repository.index.commit('Import from Wordpress')  # Commit is unnecessary.

tree = ElementTree(file=filename)

description = tree.find('.//channel/description').text
repository.description = description

author_emails = {}
for author in tree.iterfind('.//{http://wordpress.org/export/1.2/}author'):
    author_name = author.find('{http://wordpress.org/export/1.2/}author_display_name').text
    author_email = author.find('{http://wordpress.org/export/1.2/}author_email').text
    author_emails[author_name] = author_email

for item in tree.iterfind('.//item'):
    post_type = item.find('{http://wordpress.org/export/1.2/}post_type').text
    status = item.find('{http://wordpress.org/export/1.2/}status').text
    if post_type == 'post' and status == 'publish':
        title = item.find('title').text
        pubdate = item.find('pubDate').text
        creator = item.find('{http://purl.org/dc/elements/1.1/}creator').text
        email = author_emails[creator]
        content = item.find('{http://purl.org/rss/1.0/modules/content/}encoded').text
        html = "<h1>%s</h1>\n%s" % (title, content)
        #comments = [c for c in item.iterfind('{http://wordpress.org/export/1.2/}comment')]
        filename = item.find('{http://wordpress.org/export/1.2/}post_name').text
        environ['GIT_AUTHOR_DATE'] = pubdate
        post = Post(repository_path, filename.encode('utf-8'))
        post.update_content(html.encode('utf-8'), creator.encode('utf-8'), \
                email.encode('utf-8'), title.encode('utf-8'))
