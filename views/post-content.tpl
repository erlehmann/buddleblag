% setdefault('header_link', False)
% if post.mime_type.startswith('text/'):
<header>
    % if header_link:
        <h1><a href="/{{helpers.quote(post.title)}}">{{post.title}}</a></h1>
    % else:
        <h1>{{post.title}}</h1>
    % end
    <!--
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
