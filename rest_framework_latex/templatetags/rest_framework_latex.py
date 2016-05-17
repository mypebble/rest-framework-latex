from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
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


@register.simple_tag
def latex_resources():
    """Return the LATEX_RESOURCES setting with a trailing /
    """
    resources = getattr(settings, 'LATEX_RESOURCES', None)
    if resources is None:
        raise ImproperlyConfigured(
            'LATEX_RESOURCES is not defined in settings')
    if not resources.endswith('/'):
        resources = u'{}/'.format(resources)
    return resources
