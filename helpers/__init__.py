from hagelslug import generate_slug, get_first_sentence_from_html
from sanitizer import sanitize_html, generate_wysihtml5_parser_rules
from urllib2 import quote

def tag_uri(prefix, timestamp, suffix):
    return 'tag:' + prefix + ',' + timestamp.strftime("%F") + ':' + quote(suffix)
