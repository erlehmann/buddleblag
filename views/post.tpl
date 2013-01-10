% title=''
% rebase base **locals()

<article>
    <header>
        <h1>{{post.title}}</h1>
        <time datetime="{{post.creation_date.isoformat()}}" pubdate>{{post.creation_date.strftime("%A, %x")}}</time>
    </header>
%   if username:
    <div contenteditable>
%   else:
    <div>
%   end
    % include post-content post=post, helpers=helpers
    </div>
    <footer>
        <a href="/{{post.root}}/{{post.title}}/raw">Raw</a>
    </footer>
</article>
