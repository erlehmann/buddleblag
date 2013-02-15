% title = repository.description
% rebase base **locals()

<h1>{{repository.description}}</h1>
<table class=posts>
% for post in repository.posts:
  <tr>
    <td>{{post.creation_date.strftime('%Y-%m-%d')}}</td>
    <td><a href="{{post.filename}}">{{post.title}}</a></td>
  </tr>
% end
</table>
<footer>
% if not username:
  <a href="/login">login</a>
% end
</footer>