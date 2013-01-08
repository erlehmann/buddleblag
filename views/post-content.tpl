% if post.mime_type.startswith('text/'):
{{! helpers.sanitize_html(post.content)}}
% end

% if post.mime_type.startswith('image/'):
<figure>
    <img src="/{{post.root}}/{{post.title}}/raw">
    <figcaption>
        {{post.title}}
    </figcaption>
<figure>
% end