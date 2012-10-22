% rebase base auth=auth, footer=footer, helpers=helpers, sections=sections

% if auth is not None:
<form method="post">
   <textarea name=content></textarea>
   <input type=submit>
</form>
% end

% for post in posts:
<article>
%     include post-content post=post, helpers=helpers
</article>
% end
