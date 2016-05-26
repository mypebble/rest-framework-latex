from django import template
from django.utils.safestring import mark_safe

try:
    from CommonMark import Parser
    has_markdown = True
except ImportError:
    has_markdown = False

from ..markdown import LatexRenderer
from ..utils import escape_latex

register = template.Library()


@register.filter(name='latex_safe', is_safe=True)
def latex_safe(value):
    # http://www.cespedes.org/blog/85/how-to-escape-latex-special-characters
    value = escape_latex(value)
    return mark_safe(value)


@register.filter(name='latex_markdown', is_safe=True)
def latex_markdown(value):
    if not has_markdown:
        raise RuntimeError('CommonMark needs to be installed')
    parser = Parser()
    ast = parser.parse(value)
    lr = LatexRenderer()
    latex = lr.render(ast)
    return mark_safe(latex)
