% if post.mime_type.startswith('text/'):
{{! helpers.sanitize_html(post.content)}}
% end