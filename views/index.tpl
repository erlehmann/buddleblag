% rebase base config=config, helpers=helpers, auth=auth

<section>

    % for post in posts:
    <article>
        % include post-content post=post, helpers=helpers
    </article>
    % end

</section>
