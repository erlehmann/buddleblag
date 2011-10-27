%rebase base config=config, helpers=helpers, auth=auth

<section>
    % for a in articles:
        <article>
            <h1 class=editable>{{a.title}}</h1>
            <div class=editable>
                {{! helpers.sanitize_html(a.content)}}
            </div>
        </article>
    % end
</section>
