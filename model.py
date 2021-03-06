from git import Blob, Repo, IndexEntry
from StringIO import StringIO
from gitdb import IStream
from sys import stderr

from datetime import datetime
from functools import wraps
from hashlib import md5
from html5lib import parseFragment
from os import path

def memoize(function):
    """
    Decorator that caches a function's return value forever.
    """
    cache = {}
    @wraps(function)
    def wrapper(*args, **kwargs):
        key = (function.func_name, args, tuple(kwargs))
        try:
            result = cache[key]
        except KeyError:
            result = function(*args, **kwargs)
            cache[key] = result
        return result
    return wrapper

def memoize_for_head(function):
    """
    Decorator that caches a object method's return value as long as
    the repository HEAD of the objects repo property stays the same.
    """
    cache = {}
    @wraps(function)
    def wrapper(caller, *args, **kwargs):
        head = caller.repo.heads.master.commit.hexsha
        key = (head, function.func_name, caller, args, tuple(kwargs))
        try:
            result = cache[key]
        except KeyError:
            result = function(caller, *args, **kwargs)
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

    @memoize_for_head
    def _get_authors(self):
        authors = set(
            [c.author for c in self.repo.iter_commits(\
                    paths=self.filename.encode('utf-8'))]
        )
        return [{'name': a.name, 'email': a.email} for a in authors]

    authors = property(_get_authors)

    @memoize_for_head
    def _get_content(self):
        try:
            blob = self.repo.heads.master.commit.tree[self.filename]
            return blob.data_stream.read()
        except KeyError:
            return None

    content = property(_get_content)

    @memoize_for_head
    def _get_commits(self):
        commits = list(self.repo.iter_commits(\
                paths=self.filename.encode('utf-8')))
        return commits

    commits = property(_get_commits)

    @memoize
    def _get_creation_datetime(self):
        timestamp = self.commits[-1].authored_date
        return datetime.fromtimestamp(timestamp)

    creation_datetime = property(_get_creation_datetime)

    @memoize_for_head
    def _get_update_datetime(self):
        timestamp = self.repo.iter_commits(\
            paths=self.filename.encode('utf-8')).next().authored_date
        return datetime.fromtimestamp(timestamp)

    update_datetime = property(_get_update_datetime)

    @memoize_for_head
    def _exists(self):
        return bool(self.commits)

    exists = property(_exists)

    def get_content(self):
        return self.content

    @memoize_for_head
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

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return int(md5(str(self)).hexdigest(), 16)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.root.encode('utf-8')

    @memoize
    def _get_creation_datetime(self):
        timestamp = self.commits[-1].authored_date
        return datetime.fromtimestamp(timestamp)

    creation_datetime = property(_get_creation_datetime)

    @memoize_for_head
    def _get_commits(self):
        return list(self.repo.iter_commits())

    commits = property(_get_commits)

    @memoize_for_head
    def _get_posts(self):
        """
        Returns a list of posts, unsorted.
        """
        posts = [Post(self.root, b.path.encode('utf-8')) for b in \
                     self.tree.blobs]
        return posts

    posts = property(_get_posts)

    @memoize_for_head
    def _get_update_datetime(self):
        timestamp = self.commits[0].authored_date
        return datetime.fromtimestamp(timestamp)

    update_datetime = property(_get_update_datetime)

    @memoize_for_head
    def _get_archive(self):
        """Returns all posts in a POSIX tar archive."""
        f = StringIO()
        self.repo.archive(f)
        return f.getvalue()

    archive = property(_get_archive)
