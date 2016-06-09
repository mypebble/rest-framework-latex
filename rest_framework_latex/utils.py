def escape_latex(value):
    """Escape a value for Latex
    """
    value = value.replace('\\', '\\textbackslash{}')
    value = value.replace('{', '\\{')
    value = value.replace('}', '\\}')
    value = value.replace('#', '\\#')
    value = value.replace('$', '\\$')
    value = value.replace('%', '\\%')
    value = value.replace('&', '\\&')
    value = value.replace('^', '\\^{}')
    value = value.replace('_', '\\_')
    value = value.replace('~', '\\textasciitidle{}')
    value = value.replace('\\textbackslash\\{\\}', '\\textbackslash{}')
    return value
