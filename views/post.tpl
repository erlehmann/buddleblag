% title=post.title
% rebase base **locals()

<article>
    <header>
        <h1>{{post.title}}</h1>
        <time datetime="{{post.creation_date.isoformat()}}" pubdate>{{post.creation_date.strftime("%A, %x")}}</time>
    </header>
    % include post-content post=post, helpers=helpers
    <footer>
        <a href="/{{post.root}}/{{post.title}}/raw">Raw</a>
    </footer>
</article>
