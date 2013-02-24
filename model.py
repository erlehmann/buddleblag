from git import Blob, Repo, IndexEntry
from StringIO import StringIO
from gitdb import IStream
from sys import stderr

from datetime import datetime
from hashlib import md5
from html5lib import parseFragment
from os import path

from functools import wraps

def memoize(function):
    """
    Decorator that caches a functions return value forever.
    """
    cache = {}
    @wraps(function)
    def wrapper(*args, **kwargs):
        key = (function, args, tuple(kwargs))
        try:
            result = cache[key]
        except KeyError:
            result = function(*args, **kwargs)
            cache[key] = result
        return result
    return wrapper

class Post(object):
    def __init__(self, directory, filename):
        self.filename = filename.decode('utf-8')
        self.root = directory
        self.repo = Repo(self.root)
        self.path = path.join(self.root, self.filename)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return int(md5(str(self)).hexdigest(), 16)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.path.encode('utf-8')

    def _get_authors(self):
        authors = set(
            [c.author for c in self.repo.iter_commits(paths=self.filename.encode('utf-8'))]
        )
        return [{'name': a.name, 'email': a.email} for a in authors]

    authors = property(_get_authors)

    def _get_content(self):
        try:
            blob = self.repo.heads.master.commit.tree[self.filename]
            return blob.data_stream.read()
        except KeyError:
            return None

    content = property(_get_content)

    def _get_commits(self):
        commits = list(self.repo.iter_commits(paths=self.filename.encode('utf-8')))
        return commits

    commits = property(_get_commits)

    @memoize
    def _get_creation_datetime(self):
        timestamp = self.commits[-1].authored_date
        return datetime.fromtimestamp(timestamp)

    creation_datetime = property(_get_creation_datetime)

    def _get_update_datetime(self):
        last_commit = self.repo.iter_commits(paths=self.filename.encode('utf-8')).next()
        return datetime.fromtimestamp(last_commit.authored_date)

    update_datetime = property(_get_update_datetime)

    def _exists(self):
        return bool(self.commits)

    exists = property(_exists)

    def get_content(self):
        return self.content

    def get_title(self):
        document = parseFragment(self.content, treebuilder='etree', \
            namespaceHTMLElements=False, encoding='utf-8')
        try:
            text = \
                ' '.join([w for w in document.find('.//h1').itertext()])
            return text.encode('utf-8')
        except AttributeError:
            return None

    title = property(get_title)

    def update_content(self, content, author, email, message):
        config = self.repo.config_writer()
        config.set_value("user", "name", author);
        config.set_value("user", "email", email);

        istream = IStream("blob", len(content), StringIO(content))
        self.repo.odb.store(istream)
        blob = Blob(self.repo, istream.binsha, 0100644, self.filename.encode('utf-8'))
        self.repo.index.add([IndexEntry.from_blob(blob)])
        self.repo.index.commit(message)

class Repository(object):
    def __init__(self, directory):
        self.root = directory
        self.repo = Repo(self.root)
        self.tree = self.repo.heads.master.commit.tree
        self.description = self.repo.description

    def _get_creation_datetime(self):
        return commits[-1].creation_datetime

    creation_datetime = property(_get_creation_datetime)

    def _get_commits(self):
        return list(self.iter_commits())

    commits = property(_get_commits)

    def _get_posts(self):
        """Returns a list of posts, sorted by date (newest first)."""
        posts = [Post(self.root, b.path.encode('utf-8')) for b in self.tree.blobs]
        posts.sort(key=lambda p: p.creation_datetime, reverse=True)
        return posts

    posts = property(_get_posts)

    def _get_update_datetime(self):
        return commits[0].creation_datetime

    update_datetime = property(_get_update_datetime)

    def _get_archive(self):
        """Returns all posts in a POSIX tar archive."""
        f = StringIO()
        self.repo.archive(f)
        return f.getvalue()

    archive = property(_get_archive)
