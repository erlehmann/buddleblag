<!DOCTYPE html>
<meta charset="utf-8">
<title>{{config.get('blog', 'title')}}</title>
<link rel="stylesheet" href="/static/base.css">
<link rel="stylesheet" href="/static/layout.css">
<link rel="stylesheet" href="/static/decor.css">
<link rel="stylesheet" href="/static/hallo.css">
<link rel="stylesheet" href="/static/font-awesome.css">
<link rel="stylesheet" href="/static/jquery-ui-1.8.16.custom.css">

<header>
    <hgroup>
        <h1 id=blog-title>{{config.get('blog', 'title')}}</h1>
        <h2 id=blog-subtitle>{{config.get('blog', 'subtitle')}}</h2>
    </hgroup>
</header>

<aside>
    <section>
    </section>
</aside>

% include

<aside>
    % for section in config.sidebar.sections():
    <section>
        <h1>{{section}}</h1>
        <ul>
        % for (title, url) in config.sidebar.items(section):
            <li>
                % favicon = helpers.braveicon.get_favicon(url,
                %     use_data_uri=True)
                % if favicon:
                <img src="{{favicon}}" alt="" height=16 width=16>
                % end
                <a href="{{url}}">{{title}}
            </a>
        % end
        </ul>
    </section>
    % end
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
