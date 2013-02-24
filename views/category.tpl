% title = repository.description
% rebase base **locals()
<link rel=alternate href="/feed" type="application/atom+xml" title="Feed">
<link rel=alternate href="/archive" type="application/x-tar" title="Archive">

<h1>{{repository.description}}</h1>

% if username:
<style>form { height: 12em; }</style>
% include editor action="/posts", content=''
% end

<table class=posts>
% for post in repository.posts_sorted_by_creation:
  <tr>
%   if post.title is None:
    <td><a href="{{post.path}}">{{helpers.get_first_sentence_from_html(post.content)}} …</a></td>
%   else:
    <td><a href="{{post.path}}">{{post.title}}</a></td>
%   end
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