%rebase base config=config, helpers=helpers

<section>
    % for a in articles:
        <article>
            <h1>{{a.title}}</h1>
            {{! helpers.sanitize_html(a.content)}}
        </article>
    % end
</section>
