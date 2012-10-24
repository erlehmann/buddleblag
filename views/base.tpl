<!DOCTYPE html>
<meta charset=utf-8>
<title>{{title}}</title>

% for s in sections:
    <link rel="alternate" href="/feed/{{s['name']}}" type="application/atom+xml" title="Feed: {{s['title']}}">
    <link rel="alternate" href="/archive/{{s['name']}}" type="application/x-tar" title="Archiv: {{s['title']}}">
% end

<style>
  body { line-height: 1.5; margin: auto; max-width: 33em; }
  article, form, header, p { margin: 1.5em 0; }
  form > * { display: block; min-height: 3em; width: 100%; }
</style>

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
