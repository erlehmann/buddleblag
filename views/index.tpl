% rebase base config=config, helpers=helpers, auth=auth

<section>
    % try:
    %   auth[0]
    <article id=new>
        <header>
            <h1 id=new-headline class=editable>Neuer Artikel</h1>
        </header>
        <div id=new-content class=editable>
            Lorem Ipsum.
        </div>
    </article>
    % except TypeError:
    %   pass
    % end

    % for post in posts:
    <article>
        % include post-content post=post, helpers=helpers, header_link=True
    </article>
    % end

</section>
