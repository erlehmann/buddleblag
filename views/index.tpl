% rebase base **locals()

<a href="{{r.root}}"><h1>{{r.description}}</h1></a>
<ol>
    % for post in r.posts:
    <li><a href="{{post.path}}">{{post.title}}</a>
    % end
</ol>