<header>
    <h1>{{post.title}}</h1>
    <time datetime="{{post.creation_date.isoformat()}}" pubdate>{{post.creation_date.strftime("%A, %x")}}</time>
</header>

% if post.mime_type.startswith('text/'):
{{! helpers.sanitize_html(post.content)}}
%end

% if post.mime_type.startswith('image/'):
<figure>
    <img src="/{{post.root}}/{{post.title}}/raw">
    <figcaption>
        {{post.title}}
    </figcaption>
<figure>
% end

<footer>
    <a href="/{{post.root}}/{{post.title}}/raw">Raw</a>
</footer>