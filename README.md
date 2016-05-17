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
