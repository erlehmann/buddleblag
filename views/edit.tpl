% rebase base config=config, helpers=helpers, auth=auth

<h1>{{post.title}}</h1>

<form method=post action="/{{post.title}}">
    <textarea name="content" height=60>{{post.content}}</textarea>

    <label for="message">Commit Message</label>
    <input id="message" type="text" required name="message">

    <input type=submit>
</form>

