% title=post.title
% rebase base **locals()

{{! helpers.sanitize_html(post.content)}}

<footer>
% if not username:
  <a href="mailto:{{post.authors[0]['email']}}?subject={{helpers.quote('Re: ' + post.filename.encode('utf-8'))}}">comment</a>
% end
  <a href="{{post.filename}}/edit">edit</a>
</footer>