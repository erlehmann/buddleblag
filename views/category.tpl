% title = repository.description
% rebase base **locals()

% inlist = False
% year = None
% for post in repository.posts:
%     if (post.creation_date.year != year):
%         if inlist:
  </ol>
</section id={{post.creation_date.year}}>
%             inlist = False
%         end
%     year = post.creation_date.year
<section>
  <header>
    <a href=#{{post.creation_date.year}}><h1>{{post.creation_date.year}}</h1></a>
  </header>
  <ol>
%        inlist = True
%     end
    <li><a href="{{repository.root}}/{{post.title}}">{{post.title}}</a>
% end
%     if inlist:
</ol>
</section>
% end