#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncore

from email import message_from_string
from smtpd import SMTPChannel, SMTPServer
from ConfigParser import RawConfigParser

from model import Post, Repository

def get_config(filename):
    config = RawConfigParser()
    config.optionxform = str  # case sensitivity
    config.read(filename)
    return config

config = get_config('./buddelblag.config')
hostname = config.get('server', 'host')
repository_path = 'posts'
repository = Repository(repository_path)

class BuddelblagSMTPChannel(SMTPChannel):
    def smtp_RCPT(self, arg):
        address = self._SMTPChannel__getaddr('TO:', arg) if arg else None
        slug = address.split('@')[0]
        slugs = [post.filename for post in repository.posts]
        if not slug in slugs:
            self.push('553 Post does not exist')
            return
        SMTPChannel.smtp_RCPT(self, arg)

class BuddelblagSMTPServer(SMTPServer):
    def __init__(*args, **kwargs):
        SMTPServer.__init__(*args, **kwargs)

    def process_message(self, peer, mailfrom, rcpttos, data):
        slug = rcpttos[0].split('@')[0]
        message = message_from_string(data)

        subject = message['Subject']
        post = Post(repository_path, slug)
        if not post.title.endswith(subject):
            return '554 Subject wrong or missing.\r\n'

        in_reply_to = message['In-Reply-To']
        message_ids = ['%s@%s' % (commit.hexsha, hostname) \
                           for commit in post.commits]
        print message_ids, dict(message)
        if not in_reply_to in message_ids:
            return '554 In-Reply-To wrong or missing.\r\n'

        content = ''
        def get_message_text(message):
            charset = message.get_content_charset()
            if part.get_content_type() in ('text/plain', 'text/html'):
                return part.get_payload(decode=True)

        if message.is_multipart():
            for part in message.get_payload():
                content = get_message_text(message)
        else:
            content = get_message_text(message)
        print content

    def handle_accept(self):
        conn, addr = self.accept()
        channel = BuddelblagSMTPChannel(self, conn, addr)

if __name__ == '__main__':
    smtp_server = BuddelblagSMTPServer(('localhost', 2525), None)
    try:
        asyncore.loop()
    except:
        smtp_server.close()
