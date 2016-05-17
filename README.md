# REST Framework LaTeX Plugin

A simple plug-n-play LaTeX renderer for Django REST Framework.

## Dependencies

Currently the LaTeX plugin requires `lualatex` - to install this on Ubuntu:

```bash
sudo aptitude install texlive-latex-extra texlive-xetex
```

## Using the Renderer

You can then configure the renderer in your settings or on each view:

```python
REST_FRAMEWORK = {
  'DEFAULT_RENDERER_CLASSES': [
    'rest_framework_latex.renderers.LatexRenderer',
  ]
}
```

### `LATEX_RESOURCES` Setting

The `LATEX_RESOURCES` directory contains the base template environment e.g.
any images or static resources to include in your template. This must be set for
the renderer to work:

```python
LATEX_RESOURCES = '/home/user/path_to_resources'
```

This works just like `TemplateHTMLRenderer` but by setting a `latex_name` on
your view:

```python
from rest_framework import viewsets

from rest_framework_latex import renderers


class SomeViewSet(viewsets.ViewSet):
  """
  """
  renderer_classes = [
    renderers.LatexRenderer,
  ]

  latex_name = 'directory/latexfile.tex'
```

### Using the Template Tags

To use the template tags, add `rest_framework_latex` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
  ...
  'rest_framework_latex',
  ...
]
```

Then load in your tags in your template:


```latex
\documentclass{article}
{% load rest_framework_latex %}

{{ user_entered_text | latex_safe }}

{% latex_resources %}
```

|        Tag        | Tag/Filter  |                    Purpose                      |
|-------------------|-------------|-------------------------------------------------|
|    `latex_safe`   |    Filter   | Escape all user-entered content for LaTeX rules |
| `latex_resources` |      Tag    |  Print the value of `settings.LATEX_RESOURCES`  |


## Django Compatibility

The REST Framework LaTeX plugin is compatible with Django 1.9 and up and
Django REST Framework 3.3 and up.
