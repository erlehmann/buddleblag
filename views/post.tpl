% title=post.title
% rebase base **locals()
<link rel=up href="/posts" title="{{post.repo.description}}">
<article>
{{! helpers.sanitize_html(post.content)}}
</article>
<nav>
  <ul>
    <li><a href="{{post.filename}}/edit">📝 Edit</a>
    <li><a href="mailto:{{post.authors[0]['email']}}?subject={{helpers.quote('Re: ' + post.filename.encode('utf-8'))}}">📩 Comment</a>
  </ul>
</nav>