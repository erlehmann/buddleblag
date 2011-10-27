from dulwich.repo import Repo
from dulwich.objects import Blob, Tree, Commit, parse_timezone
from time import time

class Article(object):
    def __init__(self, title):
        self.title =  title.encode('UTF-8')
        self.repo = Repo('articles')

        self.head = self.repo.get_object(self.repo.head())
        self.tree = self.repo.get_object(self.head.tree)

        try:
            sha = self.tree[self.title][1]
            self.content = self.repo[sha].data
        except KeyError:
            self.content = u'This space intentionally left blank.'

    def __str__(self):
        return self.title

    def get_content(self):
        return self.content

    def get_title(self):
        return self.title

    def update_content(self, new_content, author, email, message):
        new_content = new_content.encode('UTF-8')
        author = author.encode('UTF-8')
        message = message.encode('UTF-8')
        email = email.encode('UTF-8')

        # create blob, add to existing tree
        blob = Blob.from_string(new_content)
        self.tree[self.title] = (0100644, blob.id)

        # commit
        commit = Commit()
        commit.tree = self.tree.id
        commit.parents = [self.head.id]
        commit.author = commit.committer = "%s <%s>" % (author, email)
        commit.commit_time = commit.author_time = int(time())
        tz = parse_timezone('+0100')[0]  # FIXME: get proper timezone
        commit.commit_timezone = commit.author_timezone = tz
        commit.encoding = 'UTF-8'
        commit.message = message

        # save everything
        object_store = self.repo.object_store
        object_store.add_object(blob)
        object_store.add_object(self.tree)
        object_store.add_object(commit)

        self.repo.refs['refs/heads/master'] = commit.id

    def update_title(self, new_title):
        pass

class ArticleList(object):
    def __init__(self):
        self.repo = Repo('articles')
        self.head = self.repo.get_object(self.repo.head())
        self.tree = self.repo.get_object(self.head.tree)

    def get_article_titles(self):
        return [a for a in self.tree]
