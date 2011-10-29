<a href="/post/{{helpers.quote(post.title)}}" class=permalink>#</a>

% if post.mime_type.startswith('text/'):
<h1 class=editable>{{post.title}}</h1>
<div class=editable>
    {{! helpers.sanitize_html(post.content)}}
</div>
%end

% if post.mime_type.startswith('image/'):
<figure>
    <img src="/raw/{{helpers.quote(post.title)}}">
    <figcaption>
        {{post.title}}
    </figcaption>
<figure>
% end
