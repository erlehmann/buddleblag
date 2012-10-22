from git import Blob, Repo, IndexEntry
from StringIO import StringIO
from gitdb import IStream

import magic

from datetime import datetime

class Post(object):
    def __init__(self, section, title):
        self.section = section
        self.repo = Repo(self.section)
        self.title = title.decode('UTF-8')

        try:
            blob = self.repo.heads.master.commit.tree[self.title]
            self.content = blob.data_stream.read()
        except KeyError:
            self.content = ''

    def __str__(self):
        return self.title

    def _get_authors(self):
        authors = set(
            [c.author for c in self.repo.iter_commits(paths=self.title)]
        )
        return [{'name': a.name, 'email': a.email} for a in authors]

    authors = property(_get_authors)

    def _get_commits(self):
        return [c for c in self.repo.iter_commits(paths=self.title)]

    commits = property(_get_commits)

    def _get_creation_datetime(self):
        timestamp = self.commits[-1].committed_date
        return datetime.fromtimestamp(timestamp)

    created = property(_get_creation_datetime)

    def _get_update_datetime(self):
        timestamp = self.commits[0].committed_date
        return datetime.fromtimestamp(timestamp)

    updated = property(_get_update_datetime)

    def get_content(self):
        return self.content

    def get_mime_type(self):
        ms = magic.Magic(magic.MAGIC_MIME)
        return ms.from_buffer(self.get_content())

    mime_type = property(get_mime_type)

    def get_title(self):
        return self.title

    def update_content(self, content, author, email, message):
        config = self.repo.config_writer()
        config.set_value("user", "name", author.encode('UTF-8'));
        config.set_value("user", "email", email.encode('UTF-8'));

        content = content.encode('UTF-8')
        message = message.encode('UTF-8')

        filename = self.title

        istream = IStream("blob", len(content), StringIO(content))
        self.repo.odb.store(istream)
        blob = Blob(self.repo, istream.binsha, 0100644, filename)
        self.repo.index.add([IndexEntry.from_blob(blob)])
        self.repo.index.commit(message)

    def update_title(self, new_title):
        pass

class PostList(object):
    """
    Returns a list of posts, sorted by date (newest first).
    """
    def __init__(self, section):
        self.section = section
        self.repo = Repo(self.section)
        self.tree = self.repo.heads.master.commit.tree

    def __iter__(self):
        return iter(self.posts)

    def _create_archive(self):
        f = StringIO()
        self.repo.archive(f)
        return f.getvalue()

    archive = property(_create_archive)

    def _get_creation_datetime(self):
        return self.posts[-1].created

    created = property(_get_creation_datetime)

    def _get_posts(self):
        posts = [Post(self.section, b.path) for b in self.tree.blobs]
        posts.sort(key=lambda p: p.created, reverse=True)
        return posts

    posts = property(_get_posts)

    def _get_update_datetime(self):
        return self.posts[0].created

    updated = property(_get_update_datetime)
