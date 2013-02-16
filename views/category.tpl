% title = repository.description
% rebase base **locals()

<h1>{{repository.description}}</h1>
<table class=posts>
% for post in repository.posts:
  <tr>
    <td><a href="/posts/{{post.filename}}">{{post.title}}</a></td>
    <td>{{post.creation_datetime.strftime('%d %b %Y ')}}</td>
  </tr>
% end
</table>
<footer>
% if not username:
  <a href="/login">login</a>
% end
</footer>