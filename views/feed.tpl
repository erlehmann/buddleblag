<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
 <title>{{title}}</title>
 <id>{{id}}</id>
 <link rel="self" href="{{self}}"/>
 <updated>{{updated.isoformat()}}Z</updated>
% for entry in entries:
 <entry>
  <title>{{entry['title']}}</title>
  <id>{{entry['id']}}</id>
  <updated>{{entry['updated'].isoformat()}}Z</updated>
  % for author in entry['authors']:
  <author>
   <name>{{author['name']}}</name>
   <email>{{author['email']}}</email>
  </author>
  % end
  <link rel="alternate" type="text/html" href="{{entry['url']}}"/>
  <content type="html">
<![CDATA[
{{! helpers.sanitize_html(entry['content'])}}
]]>
  </content>
 </entry>
% end
</feed>