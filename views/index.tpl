% rebase base title=title, helpers=helpers

% for r in repositories:
<section>
    <a href="{{r.root}}"><h1>{{r.description}}</a></h1></a>
    <ul>
        % for p in r.posts:
        <li><a href="{{r.root}}/{{p.title}}">{{p.title}}</a>
        % end
    </ul>
</section>
% end