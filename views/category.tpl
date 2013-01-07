% rebase base title=title+' / '+repository.root, helpers=helpers

<section>
    <h1>{{repository.description}}</a></h1>
    <ul>
        % for p in repository.posts:
        <li><a href="{{repository.root}}/{{p.title}}">{{p.title}}</a>
        % end
    </ul>
</section>