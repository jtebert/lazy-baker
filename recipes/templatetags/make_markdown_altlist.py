import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True, name='make_markdown_altlist')
@stringfilter
def make_markdown_altlist(value):
    extensions = ["nl2br",
                  'markdown.extensions.footnotes',
                  'markdown.extensions.fenced_code',
                  'markdown.extensions.tables',
                  'markdown.extensions.codehilite']
    x = markdown.markdown(force_text(value),
                          extensions,
                          safe_mode=False,
                          enable_attributes=False)
    x = x.replace('<ul>', '<ul class="alt">')
    return mark_safe(x)
