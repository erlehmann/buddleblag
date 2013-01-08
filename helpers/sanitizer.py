# adapted from http://code.google.com/p/soclone/source/browse/trunk/soclone/utils/html.py

import html5lib
from html5lib import sanitizer, serializer, tokenizer, treebuilders, treewalkers

class HTMLSanitizerMixin(sanitizer.HTMLSanitizerMixin):
    acceptable_elements = (
        'section', 'article', 'aside', 'h1', 'h2',      # sectioning
        'h3', 'h4', 'h5', 'h6', 'hgroup',
        'p', 'pre', 'hr', 'blockquote', 'ol', 'ul',     # grouping
        'li', 'dl', 'dt', 'dd', 'figure', 'figcaption',
        'a', 'em', 'strong', 'small', 's', 'cite',      # text-level semantics
        'q', 'dfn', 'abbr', 'time', 'code', 'var',
        'samp', 'kbd', 'sup', 'sup', 'i', 'b',
        'img', 'video', 'audio', 'source',              # embedded content
        'table', 'caption', 'colgroup', 'col', 'col',   # tabular content
        'tbody', 'thead', 'tfoot', 'tr', 'td', 'th'
    )

    acceptable_attributes = (
        'id', 'title', 'lang',              # global
        'href', 'rel',                      # hyperlinks
        'datetime', 'pubdate',              # date
        'alt', 'src', 'controls',           # embedded content
        'colspan', 'rowspan', 'headers'     # tabular content
        )

    allowed_elements = acceptable_elements
    allowed_attributes = acceptable_attributes
    allowed_css_properties = ()
    allowed_css_keywords = ()
    allowed_svg_properties = ()

class HTMLSanitizer(tokenizer.HTMLTokenizer, HTMLSanitizerMixin):
    def __init__(self, stream, encoding=None, parseMeta=True, useChardet=True,
                 lowercaseElementName=True, lowercaseAttrName=True, parser=None):
        tokenizer.HTMLTokenizer.__init__(self, stream, encoding, parseMeta,
                                         useChardet, lowercaseElementName,
                                         lowercaseAttrName)

    def __iter__(self):
        for token in tokenizer.HTMLTokenizer.__iter__(self):
            token = self.sanitize_token(token)
            if token:
                yield token

def sanitize_html(html):
    """Sanitizes an HTML fragment."""
    p = html5lib.HTMLParser(tokenizer=HTMLSanitizer,
                            tree=treebuilders.getTreeBuilder("dom"))
    dom_tree = p.parseFragment(html, encoding='utf-8')
    walker = treewalkers.getTreeWalker("dom")
    stream = walker(dom_tree)
    s = serializer.HTMLSerializer(omit_optional_tags=False,
                                  quote_attr_values=True)
    output_generator = s.serialize(stream)
    return u''.join(output_generator)
