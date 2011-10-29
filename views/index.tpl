%rebase base config=config, helpers=helpers, auth=auth

<section>

    % for p in posts:
    <article>
        <a href="/{{helpers.quote(p.title)}}" class=permalink>#</a>

        % if p.mime_type.startswith('text/'):
        <h1 class=editable>{{p.title}}</h1>
        <div class=editable>
            {{! helpers.sanitize_html(p.content)}}
        </div>
        %end

        % if p.mime_type.startswith('image/'):
        <figure>
            <img src="/raw/{{helpers.quote(p.title)}}">
            <figcaption>
                {{p.title}}
            </figcaption>
        <figure>
        % end

    </article>
    % end

</section>
