<!DOCTYPE html>
<meta charset=utf-8>
<title>{{title}}</title>
<link rel=stylesheet href=/static/base.css>

<header>
    <h1>{{title}}</h1>
</header>

% include

<aside>
    <section>
        {{tagline}}
    </section>
    <section>
    <h1>Categories</h1>
    <ul>
        % for directory in directories:
        <li><a href="/{{directory}}">{{directory}}</a>
        % end
    </ul>
    </section>
</aside>
