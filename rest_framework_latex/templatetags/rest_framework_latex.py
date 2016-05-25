from django import template
from django.utils.safestring import mark_safe

from ..utils import escape_latex

register = template.Library()


@register.filter(name='latex_safe', is_safe=True)
def latex_safe(value):
    # http://www.cespedes.org/blog/85/how-to-escape-latex-special-characters
    value = escape_latex(value)
    return mark_safe(value)
