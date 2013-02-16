% title=post.title
% rebase base **locals()

{{! helpers.sanitize_html(post.content)}}

<footer>
% if username:
  <a href="{{post.filename}}/edit">edit</a>
% else:
  <a href="mailto:{{post.authors[0]['email']}}?subject={{helpers.quote('Re: ' + post.filename)}}">comment</a>
% end
</footer>