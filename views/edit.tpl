% title = post.title
% rebase base **locals()

<form method=post action="/{{post.root}}/{{post.title}}">
  <textarea name="content" autofocus required>{{! post.content}}</textarea>
  <input type=reset value="Reset">
  <input type=submit value="Save">
</form>
