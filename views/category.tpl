% rebase base **locals()
<link rel=alternate href="/feed" type="application/atom+xml" title="Feed">
<link rel=alternate href="/archive" type="application/x-tar" title="Archive">

<h1>{{title}}</h1>

% if username:
<style>form { height: 12em; }</style>
% include editor action="/posts", content=''
% end

<table class=posts>
% for post in posts:
  <tr>
    <td><a href="{{post['url']}}">{{post['title']}}</a>
    <td>{{post['created'].strftime('%d %b %Y ')}}
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