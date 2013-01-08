% title = repository.description
% rebase base **locals()

<ol>
    % for p in repository.posts:
    <li><a href="{{repository.root}}/{{p.title}}">{{p.title}}</a>
    % end
</ol>
