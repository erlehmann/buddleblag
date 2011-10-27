<!DOCTYPE html>
<meta charset="utf-8">
<title>{{config.get('blog', 'title')}}</title>
<link rel="stylesheet" href="/static/base.css">
<link rel="stylesheet" href="/static/layout.css">
<link rel="stylesheet" href="/static/decor.css">

<hgroup>
    <h1 class=editable>{{config.get('blog', 'title')}}</h1>
    <h2 class=editable>{{config.get('blog', 'subtitle')}}</h2>
</hgroup>

<header id=top>
    % try:
    %   auth[0]
        <button id=edit>Editieren</button>
        <button id=save disabled>Speichern</button>
        <button id=abort disabled>Verwerfen</button>
    % except TypeError:
        <a href="/login">Login</a>
    %end
</header>

<div id=main>
% include
</div>

<aside id=sidebar>
    <section>
        <h1>Hallo</h1>
        <p>
            Blindtext, Blindtext, Blindtext.
        </p>
    </section>
    <section>
        <h1>Blogroll</h1>
        <ul id=blogroll>
        % for blog in config.items('blogroll'):
            <li>
                % favicon = helpers.braveicon.get_favicon(blog[1],
                %     use_data_uri=True)
                <img src="{{favicon}}" alt="" height=16 width=16>
                <a href="{{blog[1]}}">{{blog[0]}}
            </a>
        % end
        </ul>
    </section>
</aside>

<footer>
    <p>
        {{config.get('blog', 'footer')}}
    </p>
</footer>

% try:
%   auth[0]
<script src="/static/domready.js"></script>
<script src="/static/buddleblag.js"></script>
% except TypeError:
%   pass
% end
