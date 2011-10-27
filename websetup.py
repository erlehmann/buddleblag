#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import mkdir
from time import time

from dulwich.repo import Repo
from dulwich.objects import Blob, Tree, Commit, parse_timezone

# create repository directory
try:
    mkdir("articles")
except OSError:
    pass

# create repository
try:
    repo = Repo.init("articles")
except OSError:
    repo = Repo("articles")

# create blob
blob = Blob.from_string("""
<!DOCTYPE html>
<meta charset="utf-8">
<title>The first entry in your buddelblag</title>
buddelblag is a simple blog engine.\n
""")

# add blob to tree
tree = Tree()
tree.add("The first entry in your buddelblag", 0100644, blob.id)

# commit
commit = Commit()
commit.tree = tree.id
author = "Anonymous <anonymous@example.invalid>"
commit.author = commit.committer = author
commit.commit_time = commit.author_time = int(time())
tz = parse_timezone('+0100')[0]  # FIXME: get proper timezone
commit.commit_timezone = commit.author_timezone = tz
commit.encoding = "UTF-8"
commit.message = "Initial commit"

# save everything
object_store = repo.object_store
object_store.add_object(blob)
object_store.add_object(tree)
object_store.add_object(commit)

# create master branch, set it as current
repo.refs.add_if_new('refs/heads/master', commit.id)
repo.refs.set_symbolic_ref('HEAD', 'refs/heads/master')
