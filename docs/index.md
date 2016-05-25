# Django Rest Framework LaTeX Renderer

This is a [Django Rest Framework] renderer which produces LaTeX
PDFs.

It's maintained by [Pebble] (S/F Software) and is used in production
in our software.

[Django Rest Framework]: http://www.django-rest-framework.org/
[Pebble]: http://mypebble.co.uk/

## Getting Started

### Dependencies

We use `lualtex` to render your documents. To get this on Ubuntu:

```
sudo aptitude install texlive-latex-extra texlive-xetex
```

**Note:** This will probably take some time due to the size of
LaTeX (around 1GB)

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

## Django Compatibility

The REST Framework LaTeX plugin is compatible with Django 1.9 and up and
Django REST Framework 3.3 and up.
