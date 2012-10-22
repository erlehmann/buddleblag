% setdefault('header_link', False)
% if post['mime_type'].startswith('text/'):
<header>
    <time datetime="{{post['created'].isoformat()}}" pubdate>{{(post['created'].strftime("%c")).strip()}}</time>
    % for a in post['authors']:
    <a href="mailto:{{a['email']}}">{{a['name']}}</a>
    % end
</header>
{{! helpers.sanitize_html(post['content'])}}
%end