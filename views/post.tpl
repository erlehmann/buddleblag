% title=post.title
% rebase base **locals()

% if username:
<form method=post>
  <div id=editor>
  <textarea name=content id=content>{{helpers.sanitize_html(post.content)}}</textarea>
  </div>
  <div id=toolbar>
    <button data-wysihtml5-action="change_view">HTML</button>
    <input type=submit>
  </div>
</form>
<script src="/static/wysihtml5-parser-rules.js"></script>
<script src="/static/wysihtml5-0.3.0.js"></script>
<script>
  var editor = new wysihtml5.Editor("content", {
    stylesheets: ['/static/base.css'],
    toolbar: "toolbar",
    parserRules: wysihtml5ParserRules,
    useLineBreaks: false
  });
</script>
% else:
{{! helpers.sanitize_html(post.content)}}
% end
