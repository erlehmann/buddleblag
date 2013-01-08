<!DOCTYPE html>
<meta charset=utf-8>
<title>{{title}}</title>
<link rel=stylesheet href=/static/base.css>

<header>
    % if title:
    <h1>{{title}}</h1>
    % end
</header>

% include

<aside>
    <section>
        {{tagline}}
    </section>
    <section>
    <h1>Categories</h1>
    <ul>
        % for repository in repositories:
        <li><a href="/{{repository.root}}">{{repository.description}}</a>
        % end
    </ul>
    </section>
</aside>
