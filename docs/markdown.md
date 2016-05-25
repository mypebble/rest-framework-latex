# Markdown

Included in DRF LaTeX is a renderer for [CommonMark] which
produces LaTeX instead of HTML.

To use it, do something like the following:

```python
from rest_framework_latex.markdown import LatexRenderer

from CommonMark import Parser

parser = Parser()
ast = parser.parse(case)
lr = LatexRenderer()
latex = lr.render(ast)
```

It currently supports the following Markdown elements:

* Lists
* **Bold** and _italics_
* Headings
* Paragraphs

Other items are simply ignored due to the way CommonMark works.

All user supplied text is escaped by the escaping utility provided.

[CommonMark]: https://github.com/rtfd/CommonMark-py
