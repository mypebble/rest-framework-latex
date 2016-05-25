# Utilities

The following utilities for dealing with LaTeX are provided:

## escape_latex

Escapes user supplied text so it is displayed as the user entered it.

```python
from rest_framework_latex.utils import escape_latex

print escape_latex('\\begin{document}attempt to break document')
# \\textbackslash{}begin\{document\}attempt to break document
```
