% title = repository.description
% rebase base **locals()

<h1>{{repository.description}}</h1>

% if username:
<style>form { height: 12em; }</style>
% include editor action="/posts", content=''
% end

<table class=posts>
% for post in repository.posts:
  <tr>
    <td><a href="/posts/{{post.filename}}">{{post.title}}</a></td>
    <td>{{post.creation_datetime.strftime('%d %b %Y ')}}</td>
  </tr>
% end
</table>

<nav>
  <ul>
% if not username:
    <li><a href="/login">🔓 Login</a>
% else:
    <li><a href="/logout">🔒 Logout</a>
  </ul>
</nav>