from html5lib import parseFragment
from unidecode import unidecode

def generate_slug(html):
    """Generates a URL slug for a HTML fragment."""
    document = parseFragment(html, treebuilder='etree', \
        namespaceHTMLElements=False, encoding='utf-8')
    try:
        text = ' '.join([t for t in document.find('.//h1').itertext()])
    except AttributeError:
        text = ' '.join([t for t in document.itertext()])
    for character in '.!?':
        # only use first sentence
        text = text.split(character)[0]
    text = unidecode(text).lower()
    allowed = \
        'abcdefghijklmnopqrstuvwxyz' + \
        '1234567890+- '
    text = ''.join([c for c in text if c in allowed])
    text = '-'.join(text.split())
    return text.encode('utf-8')
