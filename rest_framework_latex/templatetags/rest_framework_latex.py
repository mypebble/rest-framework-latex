from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='latex_safe', is_safe=True)
def latex_safe(value):
    # http://www.cespedes.org/blog/85/how-to-escape-latex-special-characters
    value = value.replace('\\', '\\textbackslash{}')
    value = value.replace('{', '\\{')
    value = value.replace('}', '\\}')
    value = value.replace('#', '\\#')
    value = value.replace('$', '\\$')
    value = value.replace('%', '\\%')
    value = value.replace('^', '\\^')
    value = value.replace('_', '\\_')
    value = value.replace('~', '\\textasciitidle{}')
    value = value.replace('\\textbackslash\\{\\}', '\\textbackslash{}')
    return mark_safe(value)
