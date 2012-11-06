from braveicon import get_favicon
from sanitizer import sanitize_html
from sanitizer import sanitize_text
from unidecode import unidecode
from urllib2 import quote

def slugify(text):
    allowed = \
        'abcdefghijklmnopqrstuvwxyz' + \
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + \
        '123456789+- '

    text = unidecode(text).lower().strip()
    text = ''.join([c for c in text if c in allowed])
    text = text.replace(' ', '-')
    return text

def tag_uri(prefix, timestamp, suffix):
    return 'tag:' + prefix + ',' + timestamp.strftime("%F") + ':' + suffix
