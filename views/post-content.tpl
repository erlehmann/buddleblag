% setdefault('header_link', False)
<header>
    <a href="{{post['url']}}"><time datetime="{{post['created'].isoformat()}}" pubdate>{{(post['created'].strftime("%c")).strip()}}</time></a>
    % for a in post['authors']:
    <a href="mailto:{{a['email']}}">{{a['name']}}</a>
    % end
</header>
% if post['mime_type'] == 'text/html':
{{! helpers.sanitize_html(post['content'])}}
% elif post['mime_type'] == 'text/plain':
{{! helpers.sanitize_text(post['content'])}}
% end