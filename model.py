from git import Blob, Repo, IndexEntry
from StringIO import StringIO
from gitdb import IStream
from sys import stderr

import magic

from datetime import datetime

class Post(object):
    def __init__(self, directory, title):
        self.title = title.decode('utf-8')
        self.root = directory
        self.repo = Repo(self.root)

        try:
            blob = self.repo.heads.master.commit.tree[self.title]
            self.content = blob.data_stream.read()
        except KeyError:
            self.content = u'This space intentionally left blank.'

    def __str__(self):
        return self.title

    def get_creation_date(self):
        commits = [
            c for c in \
                self.repo.iter_commits(paths=self.title.encode('utf-8'))
        ]
        timestamp = commits[-1].committed_date
        return datetime.fromtimestamp(timestamp)

    creation_date = property(get_creation_date)

    def get_content(self):
        return self.content

    def get_mime_type(self):
        ms = magic.Magic(magic.MAGIC_MIME)
        return ms.from_buffer(self.get_content())

    mime_type = property(get_mime_type)

    def get_title(self):
        return self.title.encode('utf-8')

    def update_content(self, content, author, email, message):
        config = self.repo.config_writer()
        config.set_value("user", "name", author);
        config.set_value("user", "email", email);

        filename = self.title

        istream = IStream("blob", len(content), StringIO(content))
        self.repo.odb.store(istream)
        blob = Blob(self.repo, istream.binsha, 0100644, filename)
        self.repo.index.add([IndexEntry.from_blob(blob)])
        self.repo.index.commit(message)

    def update_title(self, new_title):
        pass

class Repository(object):
    def __init__(self, directory):
        self.root = directory
        self.repo = Repo(self.root)
        self.tree = self.repo.heads.master.commit.tree
        self.description = self.repo.description

    def get_posts(self):
        """
        Returns a list of posts, sorted by date (newest first).
        """
        posts = [Post(self.root, b.path.encode('utf-8')) for b in self.tree.blobs]
        posts.sort(key=lambda p: p.creation_date, reverse=True)
        return posts

    posts = property(get_posts)
