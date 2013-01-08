% rebase base **locals()

% for r in repositories:
<section>
    <a href="{{r.root}}"><h1>{{r.description}}</h1></a>
    <ol>
        % for post in r.posts:
        <li><a href="{{r.root}}/{{post.title}}">{{post.title}}</a>
        % end
    </ol>
</section>
% end