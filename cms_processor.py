import itertools
import re
from models import ContentType, Content
from pyquery import PyQuery as pq
from jinja2 import Template

def add_cms_contain(user, page=None):
    """
    Add the CMS content to the page if the content_selector is in the page.
    """
    d = pq(page)
    for content_type in ContentType.objects.filter(user=user):
        selector = d(str(content_type.selector))
        if selector:
            contents = [c.content for c in Content.objects.filter(user=user, type=content_type.type)]
            if content_type.unique and contents:
                formatted_content = apply_layout(content_type.layout, content=contents[0])
            else:
                formatted_content = apply_layout(content_type.layout, contents=contents)
            selector.append(formatted_content)
    return unicode(d)

def add_content_type(type, user, layout, selector, unique=False):
    if not validate_layout(layout):
        raise ValueError("The layout is invalid.")
    ContentType.objects.create(type=type, user=user, layout=layout, selector=selector, unique=unique)

def add_content(type, user, content=None, contents=None):
    content = Content.objects.create(type=type, user=user, content=content)

ALLOWED_VAR = ['contents', "content"]
def validate_layout(layout):
    validator = re.compile("{{\s*([a-zA-Z1-9]*)\s*}}|{%\s*for\s+\w+\s+in\s+(\w+)\s*%}")
    matches = itertools.chain.from_iterable(validator.findall(layout)) # flatten the list of matches
    matches = filter(lambda var: var not in ALLOWED_VAR, matches) # remove valid tag
    matches = filter(lambda var: var, matches) # remove empty string
    return not bool(matches)

def apply_layout(layout, content=None, contents=None):
    template = Template(layout)
    return template.render(contents=contents, content=content)