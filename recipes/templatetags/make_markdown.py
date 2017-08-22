import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

import sys

register = template.Library()

@register.filter(is_safe=True, name='make_markdown')
@stringfilter
def make_markdown(value):
    extensions = ["nl2br",
                  'markdown.extensions.footnotes',
                  'markdown.extensions.fenced_code',
                  'markdown.extensions.tables',
                  'markdown.extensions.codehilite']

    return mark_safe(markdown.markdown(force_unicode(value),
                                       extensions,
                                       safe_mode=True,
                                       enable_attributes=False))