% if post.mime_type.startswith('text/'):
<header>
    <h1>{{post.title}}</h1>
    <!--
    <a href="/{{helpers.quote(post.title)}}" class=permalink>❖</a>
    <a href="/{{helpers.quote(post.title)}}/edit" class=editlink>✎</a>
    -->
    <time datetime="{{post.creation_date.isoformat()}}" pubdate>{{post.creation_date.strftime("%A, %x")}}</time>
</header>
{{! helpers.sanitize_html(post.content)}}
%end

% if post.mime_type.startswith('image/'):
<figure>
    <img src="/{{helpers.quote(post.title)}}/raw">
    <figcaption>
        {{post.title}}
    </figcaption>
<figure>
% end
