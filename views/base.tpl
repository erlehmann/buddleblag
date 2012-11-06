<!DOCTYPE html>
<meta charset=utf-8>
<title>{{title}}</title>
<link rel=stylesheet href=/static/base.css type=text/css>
<link rel=stylesheet href=/static/decor.css type=text/css>

% for s in sections:
    <link rel=alternate href="/feed/{{s['name']}}" type=application/atom+xml title="Feed: {{s['title']}}">
    <link rel=alternate href="/archive/{{s['name']}}" type=application/x-tar title="Archiv: {{s['title']}}">
% end

<header>
    <h1 id=blog-title>{{title}}</h1>
% try:
    <h2 id=section-title>{{section}}</h2>
% except NameError:
%     pass
% end
</header>

<nav>
    <ul>
% for section in sections:
        <li><a class="{{section['name']}}" href="/{{section['name']}}">{{section['title']}}</a>
% end
 </nav>

% include

<footer>
    <small>
        {{footer}}
    </small>
</footer>
