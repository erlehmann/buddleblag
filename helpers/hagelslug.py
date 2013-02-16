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
    text = get_first_sentence(text)
    text = unidecode(text).lower()
    allowed = \
        'abcdefghijklmnopqrstuvwxyz' + \
        '1234567890+- '
    text = ''.join([c for c in text if c in allowed])
    text = '-'.join(text.split())
    return text.encode('utf-8')

def get_first_sentence(text):
    """Returns the first sentence of a text."""
    for character in '.!?':
        text = text.split(character)[0]
    return text

def get_first_sentence_from_html(html):
    document = parseFragment(html, treebuilder='etree', \
        namespaceHTMLElements=False, encoding='utf-8')
    text = ' '.join([t for t in document.itertext()])
    text = get_first_sentence(text)
    return text.encode('utf-8')
