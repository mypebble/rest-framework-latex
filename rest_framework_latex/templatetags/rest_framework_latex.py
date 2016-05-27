from django import template
from django.utils.safestring import mark_safe
from django.core.exceptions import ImproperlyConfigured

try:
    from CommonMark import Parser
    from ..markdown import LatexRenderer
    has_markdown = True
except ImportError:
    has_markdown = False

from ..utils import escape_latex

register = template.Library()


@register.filter(name='latex_safe', is_safe=True)
def latex_safe(value):
    """Escapes text for Latex
    """
    # http://www.cespedes.org/blog/85/how-to-escape-latex-special-characters
    value = escape_latex(value)
    return mark_safe(value)


@register.filter(name='latex_markdown', is_safe=True)
def latex_markdown(value):
    """Turns markdown into LaTeX and returns it
    """
    if not has_markdown:
        raise ImproperlyConfigured('CommonMark needs to be installed')
    parser = Parser()
    ast = parser.parse(value)
    lr = LatexRenderer()
    latex = lr.render(ast)
    return mark_safe(latex)
