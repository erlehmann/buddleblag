% if post.mime_type.startswith('text/'):
<header>
    <h1>{{post.title}}</h1>
    <!--
    <a href="/{{helpers.quote(post.title)}}" class=permalink>❖</a>
    <a href="/{{helpers.quote(post.title)}}/edit" class=editlink>✎</a>
    -->
</header>
<div class=editable>
    {{! helpers.sanitize_html(post.content)}}
</div>
%end

% if post.mime_type.startswith('image/'):
<figure>
    <img src="/{{helpers.quote(post.title)}}/raw">
    <figcaption>
        {{post.title}}
    </figcaption>
<figure>
% end
