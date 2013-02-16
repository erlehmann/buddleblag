% title = post.title
% rebase base **locals()

% include editor action="/posts/%s" % helpers.quote(post.filename.encode('utf-8')), content=helpers.sanitize_html(post.content)